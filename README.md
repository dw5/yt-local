[![Build Status](https://drone.hgit.ga/api/badges/heckyel/yt-local/status.svg)](https://drone.hgit.ga/heckyel/yt-local)

# yt-local

Fork of [youtube-local](https://github.com/user234683/youtube-local)

yt-local is a browser-based client written in Python for watching YouTube anonymously and without the lag of the slow page used by YouTube. One of the primary features is that all requests are routed through Tor, except for the video file at googlevideo.com. This is analogous to what HookTube (defunct) and Invidious do, except that you do not have to trust a third-party to respect your privacy. The assumption here is that Google won't put the effort in to incorporate the video file requests into their tracking, as it's not worth pursuing the incredibly small number of users who care about privacy (Tor video routing is also provided as an option). Tor has high latency, so this will not be as fast network-wise as regular YouTube. However, using Tor is optional; when not routing through Tor, video pages may load faster than they do with YouTube's page depending on your browser.

The YouTube API is not used, so no keys or anything are needed. It uses the same requests as the YouTube webpage.

## Screenshots

[Light theme](https://pic.infini.fr/l7WINjzS/0Ru6MrhA.png)

[Gray theme](https://pic.infini.fr/znnQXWNc/hL78CRzo.png)

[Dark theme](https://pic.infini.fr/iXwFtTWv/mt2kS5bv.png)

[Channel](https://pic.infini.fr/JsenWVYe/SbdIQlS6.png)

## Features
* Standard pages of YouTube: search, channels, playlists
* Anonymity from Google's tracking by routing requests through Tor
* Local playlists: These solve the two problems with creating playlists on YouTube: (1) they're datamined and (2) videos frequently get deleted by YouTube and lost from the playlist, making it very difficult to find a reupload as the title of the deleted video is not displayed.
* Themes: Light, Gray, and Dark
* Subtitles
* Easily download videos or their audio. (Disabled by default)
* No ads
* View comments
* JavaScript not required
* Theater and non-theater mode
* Subscriptions that are independent from YouTube
  * Can import subscriptions from YouTube
  * Works by checking channels individually
  * Can be set to automatically check channels.
  * For efficiency of requests, frequency of checking is based on how quickly channel posts videos
  * Can mute channels, so as to have a way to "soft" unsubscribe. Muted channels won't be checked automatically or when using the "Check all" button. Videos from these channels will be hidden.
  * Can tag subscriptions to organize them or check specific tags
* Fast page
  * No distracting/slow layout rearrangement
  * No lazy-loading of comments; they are ready instantly.
* Settings allow fine-tuned control over when/how comments or related videos are shown:
  1. Shown by default, with click to hide
  2. Hidden by default, with click to show
  3. Never shown
* Optionally skip sponsored segments using [SponsorBlock](https://github.com/ajayyy/SponsorBlock)'s API
* Custom video speeds
* Video transcript
* Supports all available video qualities: 144p through 2160p

## Planned features
- [ ] Putting videos from subscriptions or local playlists into the related videos
- [x] Information about video (geographic regions, region of Tor exit node, etc)
- [ ] Ability to delete playlists
- [ ] Auto-saving of local playlist videos
- [ ] Import youtube playlist into a local playlist
- [ ] Rearrange items of local playlist
- [x] Video qualities other than 360p and 720p by muxing video and audio
- [x] Indicate if comments are disabled
- [x] Indicate how many comments a video has
- [ ] Featured channels page
- [ ] Channel comments
- [x] Video transcript
- [x] Automatic Tor circuit change when blocked
- [x] Support &t parameter
- [ ] Subscriptions: Option to mark what has been watched
- [ ] Subscriptions: Option to filter videos based on keywords in title or description
- [ ] Subscriptions: Delete old entries and thumbnails
- [ ] Support for more sites, such as Vimeo, Dailymotion, LBRY, etc.

## Installing

### Windows

Download the zip file under the Releases page. Unzip it anywhere you choose.

### GNU+Linux/MacOS

Download the tarball under the Releases page and extract it. `cd` into the directory and run

1. `cd yt-local`
2. `virtualenv -p python3 venv`
3. `source venv/bin/activate`
4. `pip install -r requirements.txt`
5. `python server.py`


**Note**: If pip isn't installed, first try installing it from your package manager. Make sure you install pip for python 3. For example, the package you need on debian is python3-pip rather than python-pip. If your package manager doesn't provide it, try to install it according to [this answer](https://unix.stackexchange.com/a/182467), but make sure you run `python3 get-pip.py` instead of `python get-pip.py`

## Usage

Firstly, if you wish to run this in portable mode, create the empty file "settings.txt" in the program's main directory. If the file is there, settings and data will be stored in the same directory as the program. Otherwise, settings and data will be stored in `C:\Users\[your username]\.yt-local` on Windows and `~/.yt-local` on GNU+Linux/MacOS.

To run the program on windows, open `run.bat`. On GNU+Linux/MacOS, run `python3 server.py`.

Access youtube URLs by prefixing them with `http://localhost:9010/`.
For instance, `http://localhost:9010/https://www.youtube.com/watch?v=vBgulDeV2RU`
You can use an addon such as Redirector ([Firefox](https://addons.mozilla.org/en-US/firefox/addon/redirector/)|[Chrome](https://chrome.google.com/webstore/detail/redirector/ocgpenflpmgnfapjedencafcfakcekcd)) to automatically redirect YouTube URLs to yt-local. I use the include pattern `^(https?://(?:[a-zA-Z0-9_-]*\.)?(?:youtube\.com|youtu\.be|youtube-nocookie\.com)/.*)` and redirect pattern `http://localhost:9010/$1` (Make sure you're using regular expression mode).

If you want embeds on web to also redirect to yt-local, make sure "Iframes" is checked under advanced options in your redirector rule. Check test `http://localhost:9010/youtube.com/embed/vBgulDeV2RU`

yt-local can be added as a search engine in firefox to make searching more convenient. See [here](https://support.mozilla.org/en-US/kb/add-or-remove-search-engine-firefox) for information on firefox search plugins.

### Using Tor

In the settings page, set "Route Tor" to "On, except video" (the second option). Be sure to save the settings.

Ensure Tor is listening for Socks5 connections on port 9150. A simple way to accomplish this is by opening the Tor Browser Bundle and leaving it open. However, you will not be accessing the program (at https://localhost:8080) through the Tor Browser. You will use your regular browser for that. Rather, this is just a quick way to give the program access to Tor routing.

### Standalone Tor

If you don't want to waste system resources leaving the Tor Browser open in addition to your regular browser, you can configure standalone Tor to run instead using the following instructions.

For Windows, to make standalone Tor run at startup, press Windows Key + R and type `shell:startup` to open the Startup folder. Create a new shortcut there. For the command of the shortcut, enter `"C:\[path-to-Tor-Browser-directory]\Tor\tor.exe" SOCKSPort 9150 ControlPort 9151`. You can then launch this shortcut to start it. Alternatively, if something isn't working, to see what's wrong, open `cmd.exe` and go to the directory `C:\[path-to-Tor-Browser-directory]\Tor`. Then run `tor SOCKSPort 9150 ControlPort 9151 | more`. The `more` part at the end is just to make sure any errors are displayed, to fix a bug in Windows cmd where tor doesn't display any output. You can stop tor in the task manager.

For Debian/Ubuntu, you can `sudo apt install tor` to install the command line version of Tor, and then run `sudo systemctl start tor` to run it as a background service that will get started during boot as well. However, Tor on the command line uses the port `9050` by default (rather than the 9150 used by the Tor Browser). So you will need to change `Tor port` to 9050 and `Tor control port` to `9051` in yt-local settings page. Additionally, you will need to enable the Tor control port by uncommenting the line `ControlPort 9051`, and setting `CookieAuthentication` to 0 in `/etc/tor/torrc`. If no Tor package is available for your distro, you can configure the `tor` binary located at `./Browser/TorBrowser/Tor/tor` inside the Tor Browser installation location to run at start time, or create a service to do it.

### Tor video routing

If you wish to route the video through Tor, set "Route Tor" to "On, including video". Because this is bandwidth-intensive, you are strongly encouraged to donate to the [consortium of Tor node operators](https://torservers.net/donate.html). For instance, donations to [NoiseTor](https://noisetor.net/) go straight towards funding nodes. Using their numbers for bandwidth costs, together with an average of 485 kbit/sec for a diverse sample of videos, and assuming n hours of video watched per day, gives $0.03n/month. A $1/month donation will be a very generous amount to not only offset losses, but help keep the network healthy.

In general, Tor video routing will be slower (for instance, moving around in the video is quite slow). I've never seen any signs that watch history in yt-local affects on-site Youtube recommendations. It's likely that requests to googlevideo are logged for some period of time, but are not integrated into Youtube's larger advertisement/recommendation systems, since those presumably depend more heavily on in-page tracking through Javascript rather than CDN requests to googlevideo.

### Importing subscriptions

1. Go to the [Google takeout manager](https://takeout.google.com/takeout/custom/youtube).
2. Log in if asked.
3. Click on "All data included", then on "Deselect all", then select only "subscriptions" and click "OK".
4. Click on "Next step" and then on "Create export".
5. Click on the "Download" button after it appears.
6. From the downloaded takeout zip extract the .csv file. It is usually located under `YouTube and YouTube Music/subscriptions/subscriptions.csv`
7. Go to the subscriptions manager in yt-local. In the import area, select your .csv file, then press import.

Supported subscriptions import formats:
- NewPipe subscriptions export JSON
- Google Takeout CSV
- Old Google Takeout JSON
- OPML format from now-removed YouTube subscriptions manager

## Contributing

Pull requests and issues are welcome

For coding guidelines and an overview of the software architecture, see the [HACKING.md](docs/HACKING.md) file.

## Public instances

yt-local is not made to work in public mode, however there is an instance of yt-local in public mode but with less features

- <https://fast-gorge-89206.herokuapp.com>

## License

This project is licensed under the GNU Affero General Public License v3 (GNU AGPLv3) or any later version.

Permission is hereby granted to the youtube-dl project at [https://github.com/ytdl-org/youtube-dl](https://github.com/ytdl-org/youtube-dl) to relicense any portion of this software under the Unlicense, public domain, or whichever license is in use by youtube-dl at the time of relicensing, for the purpose of inclusion of said portion into youtube-dl. Relicensing permission is not granted for any purpose outside of direct inclusion into the [official repository](https://github.com/ytdl-org/youtube-dl) of youtube-dl. If inclusion happens during the process of a pull-request, relicensing happens at the moment the pull request is merged into youtube-dl; until that moment, any cloned repositories of youtube-dl which make use of this software are subject to the terms of the GNU AGPLv3.

## Donate
This project is completely free/Libre and will always be.

#### Crypto:
- **Bitcoin**: `1JrC3iqs3PP5Ge1m1vu7WE8LEf4S85eo7y`

## Similar projects
- [invidious](https://github.com/iv-org/invidious) Similar to this project, but also allows it to be hosted as a server to serve many users
- [Yotter](https://github.com/ytorg/Yotter) Similar to this project and to invidious. Also supports Twitter
- [FreeTube](https://github.com/FreeTubeApp/FreeTube) (Similar to this project, but is an electron app outside the browser)
- [youtube-local](https://github.com/user234683/youtube-local) first project on which yt-local is based
- [NewPipe](https://newpipe.schabi.org/) (app for android)
- [mps-youtube](https://github.com/mps-youtube/mps-youtube) (terminal-only program)
- [youtube-viewer](https://github.com/trizen/youtube-viewer)
- [FreeTube](https://github.com/FreeTubeApp/FreeTube) (Similar to this project, but is an electron app outside the browser)
- [smtube](https://www.smtube.org/)
- [Minitube](https://flavio.tordini.org/minitube), [github here](https://github.com/flaviotordini/minitube)
- [toogles](https://github.com/mikecrittenden/toogles) (only embeds videos, doesn't use mp4)
- [YTLibre](https://git.sr.ht/~heckyel/ytlibre) only extract video
- [youtube-dl](https://rg3.github.io/youtube-dl/), which this project was based off
