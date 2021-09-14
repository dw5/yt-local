## Basic init yt-local for openrc

1. Write `/etc/init.d/ytlocal` file.

```
#!/sbin/openrc-run
# Distributed under the terms of the GNU General Public License v3 or later
name="yt-local"
pidfile="/var/run/ytlocal.pid"
command="/usr/sbin/ytlocal"

depend() {
    use net
}

start_pre() {
    if [ ! -f /usr/sbin/ytlocal ] ; then
        eerror "Please create script file of ytlocal in '/usr/sbin/ytlocal'"
        return 1
    else
        return 0
    fi
}

start() {
    ebegin "Starting yt-local"
    start-stop-daemon --start --exec "${command}" --pidfile "${pidfile}"
    eend $?
}

reload() {
    ebegin "Reloading ${name}"
    start-stop-daemon --signal HUP --pidfile "${pidfile}"
    eend $?
}

stop() {
   ebegin "Stopping ${name}"
   start-stop-daemon --quiet --stop --exec "${command}" --pidfile "${pidfile}"
   eend $?
}
```

after, modified execute permissions:

    $ doas chmod a+x /etc/init.d/ytlocal


2. Write `/usr/sbin/ytlocal` and configure path.

```
#!/usr/bin/env bash

cd /home/your-path/ytlocal/ # change me
source venv/bin/activate
python server.py > /dev/null 2>&1 &
echo $! > /var/run/ytlocal.pid
```

after, modified execute permissions:

    $ doas chmod a+x /usr/sbin/ytlocal


3. OpenRC check

- status: `doas rc-service ytlocal status`
- start: `doas rc-service ytlocal start`
- restart: `doas rc-service ytlocal restart`
- stop: `doas rc-service ytlocal stop`

- enable: `doas rc-update add ytlocal default`
- disable: `doas rc-update del ytlocal`

When yt-local is run with administrator privileges,
the configuration file is stored in /root/.yt-local
