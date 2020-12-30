from youtube import proto, util, yt_data_extract
from youtube.util import (
    concat_or_none,
    strip_non_ascii
)
from youtube import yt_app
import settings

import json
import base64
import urllib
import re
import traceback

import flask
from flask import request

# Here's what I know about the secret key (starting with ASJN_i)
# *The secret key definitely contains the following information (or perhaps the information is stored at youtube's servers):
#   -Video id
#   -Offset
#   -Sort
# *If the video id or sort in the ctoken contradicts the ASJN, the response is an error. The offset encoded outside the ASJN is ignored entirely.
# *The ASJN is base64 encoded data, indicated by the fact that the character after "ASJN_i" is one of ("0", "1", "2", "3")
# *The encoded data is not valid protobuf
# *The encoded data (after the 5 or so bytes that are always the same) is indistinguishable from random data according to a battery of randomness tests
# *The ASJN in the ctoken provided by a response changes in regular intervals of about a second or two.
# *Old ASJN's continue to work, and start at the same comment even if new comments have been posted since
# *The ASJN has no relation with any of the data in the response it came from


def make_comment_ctoken(video_id, sort=0, offset=0, lc='', secret_key=''):
    video_id = proto.as_bytes(video_id)
    secret_key = proto.as_bytes(secret_key)

    page_info = proto.string(4, video_id) + proto.uint(6, sort)

    offset_information = proto.nested(4, page_info) + proto.uint(5, offset)
    if secret_key:
        offset_information = proto.string(1, secret_key) + offset_information

    page_params = proto.string(2, video_id)
    if lc:
        page_params += proto.string(6, proto.percent_b64encode(proto.string(15, lc)))

    result = proto.nested(2, page_params) + proto.uint(3, 6) + proto.nested(6, offset_information)
    return base64.urlsafe_b64encode(result).decode('ascii')


def comment_replies_ctoken(video_id, comment_id, max_results=500):

    params = proto.string(2, comment_id) + proto.uint(9, max_results)
    params = proto.nested(3, params)

    result = proto.nested(2, proto.string(2, video_id)) + proto.uint(3, 6) + proto.nested(6, params)
    return base64.urlsafe_b64encode(result).decode('ascii')


mobile_headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'X-YouTube-Client-Name': '2',
    'X-YouTube-Client-Version': '2.20180823',
}


def request_comments(ctoken, replies=False):
    if replies: # let's make it use different urls for no reason despite all the data being encoded
        base_url = "https://m.youtube.com/watch_comment?action_get_comment_replies=1&ctoken="
    else:
        base_url = "https://m.youtube.com/watch_comment?action_get_comments=1&ctoken="
    url = base_url + ctoken.replace("=", "%3D") + "&pbj=1"

    content = util.fetch_url(
        url, headers=mobile_headers,
        report_text='Retrieved comments', debug_name='request_comments')
    content = content.decode('utf-8')

    polymer_json = json.loads(content)
    return polymer_json


def single_comment_ctoken(video_id, comment_id):
    page_params = proto.string(2, video_id) + proto.string(
        6, proto.percent_b64encode(proto.string(15, comment_id)))

    result = proto.nested(2, page_params) + proto.uint(3, 6)
    return base64.urlsafe_b64encode(result).decode('ascii')


def post_process_comments_info(comments_info):
    for comment in comments_info['comments']:
        comment['author'] = strip_non_ascii(comment['author'])
        comment['author_url'] = concat_or_none(
            '/', comment['author_url'])
        comment['author_avatar'] = concat_or_none(
            settings.img_prefix, comment['author_avatar'])

        comment['permalink'] = concat_or_none(
            util.URL_ORIGIN, '/watch?v=',
            comments_info['video_id'], '&lc=', comment['id'])

        reply_count = comment['reply_count']

        if reply_count == 0:
            comment['replies_url'] = None
        else:
            comment['replies_url'] = concat_or_none(
                util.URL_ORIGIN,
                '/comments?parent_id=', comment['id'],
                '&video_id=', comments_info['video_id'])

        if reply_count == 0:
            comment['view_replies_text'] = 'Reply'
        elif reply_count == 1:
            comment['view_replies_text'] = '1 reply'
        else:
            comment['view_replies_text'] = str(reply_count) + ' replies'

        if comment['like_count'] == 1:
            comment['likes_text'] = '1 like'
        else:
            comment['likes_text'] = str(comment['like_count']) + ' likes'

    comments_info['include_avatars'] = settings.enable_comment_avatars
    if comments_info['ctoken']:
        comments_info['more_comments_url'] = concat_or_none(
            util.URL_ORIGIN,
            '/comments?ctoken=',
            comments_info['ctoken']
        )

    comments_info['page_number'] = page_number = str(int(comments_info['offset']/20) + 1)

    if not comments_info['is_replies']:
        comments_info['sort_text'] = 'top' if comments_info['sort'] == 0 else 'newest'

    comments_info['video_url'] = concat_or_none(
        util.URL_ORIGIN,
        '/watch?v=',
        comments_info['video_id']
    )

    comments_info['video_thumbnail'] = concat_or_none(
        settings.img_prefix, 'https://i.ytimg.com/vi/',
        comments_info['video_id'], '/mqdefault.jpg')


def video_comments(video_id, sort=0, offset=0, lc='', secret_key=''):
    try:
        if settings.comments_mode:
            comments_info = {'error': None}
            other_sort_url = (
                util.URL_ORIGIN + '/comments?ctoken='
                + make_comment_ctoken(video_id, sort=1 - sort, lc=lc)
            )
            other_sort_text = 'Sort by ' + ('newest' if sort == 0 else 'top')

            this_sort_url = (util.URL_ORIGIN
                             + '/comments?ctoken='
                             + make_comment_ctoken(video_id, sort=sort, lc=lc))

            comments_info['comment_links'] = [
                (other_sort_text, other_sort_url),
                ('Direct link', this_sort_url)
            ]

            comments_info.update(yt_data_extract.extract_comments_info(
                request_comments(
                    make_comment_ctoken(video_id, sort, offset, lc, secret_key)
                )
            ))
            post_process_comments_info(comments_info)

            return comments_info
        else:
            return {}
    except util.FetchError as e:
        if e.code == '429' and settings.route_tor:
            comments_info['error'] = 'Error: Youtube blocked the request because the Tor exit node is overutilized.'
            if e.error_message:
                comments_info['error'] += '\n\n' + e.error_message
            comments_info['error'] += '\n\nExit node IP address: %s' % e.ip
        else:
            comments_info['error'] = traceback.format_exc()

    except Exception as e:
        comments_info['error'] = traceback.format_exc()

    if comments_info.get('error'):
        print('Error retrieving comments for ' + str(video_id) + ':\n' +
              comments_info['error'])

    return comments_info


@yt_app.route('/comments')
def get_comments_page():
    ctoken = request.args.get('ctoken', '')
    replies = False
    if not ctoken:
        video_id = request.args['video_id']
        parent_id = request.args['parent_id']

        ctoken = comment_replies_ctoken(video_id, parent_id)
        replies = True

    comments_info = yt_data_extract.extract_comments_info(
        request_comments(ctoken, replies))

    post_process_comments_info(comments_info)

    if not replies:
        other_sort_url = util.URL_ORIGIN + '/comments?ctoken=' + make_comment_ctoken(comments_info['video_id'], sort=1 - comments_info['sort'])
        other_sort_text = 'Sort by ' + ('newest' if comments_info['sort'] == 0 else 'top')
        comments_info['comment_links'] = [(other_sort_text, other_sort_url)]

    return flask.render_template(
        'comments_page.html',
        comments_info=comments_info,
        slim=request.args.get('slim', False)
    )
