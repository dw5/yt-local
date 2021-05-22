// @license magnet:?xt=urn:btih:1f739d935676111cfff4b4693e3816e664797050&dn=gpl-3.0.txt GPL-v3-or-Later
const player = new Plyr(document.getElementById('js-video-player'), {
    disableContextMenu: false,
    captions: {
        active: true,
        language: 'en'
    },
    controls: [
        'play-large',
        'play',
        'progress',
        'current-time',
        'mute',
        'volume',
        'captions',
        'settings',
        'fullscreen'
    ],
    iconUrl: "/youtube.com/static/modules/plyr/plyr.svg",
    blankVideo: "/youtube.com/static/modules/plyr/blank.webm",
    debug: false
});
// @license-end
