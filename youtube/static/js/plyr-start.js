let captionsActive;

switch(true) {

case data.settings.subtitles_mode == 2:
  captionsActive = true;
  break;
case data.settings.subtitles_mode == 1 && data.has_manual_captions:
  captionsActive = true;
  break;
default:
  captionsActive = false;
}

const player = new Plyr(document.getElementById('js-video-player'), {
  disableContextMenu: false,
  captions: {
    active: captionsActive,
    language: data.settings.subtitles_language,
  },
  controls: [
    'play-large',
    'play',
    'progress',
    'current-time',
    'duration',
    'mute',
    'volume',
    'captions',
    'settings',
    'fullscreen'
  ],
  iconUrl: "/youtube.com/static/modules/plyr/plyr.svg",
  blankVideo: "/youtube.com/static/modules/plyr/blank.webm",
  debug: false,
  storage: {enabled: false}
});
