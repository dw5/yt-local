(function main() {
    'use strict';
    const video = document.getElementById('js-video-player');
    const speedInput = document.getElementById('speed-control');
    speedInput.addEventListener('keyup', (event) => {
        if (event.key === 'Enter') {
            let speed = parseFloat(speedInput.value);
            if(!isNaN(speed)){
                video.playbackRate = speed;
            }
        }
    });
}());
