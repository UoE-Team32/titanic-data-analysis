# titanic-data-analysis

## View Matplot Lib from within docker container...
### Linux
https://medium.com/@SaravSun/running-gui-applications-inside-docker-containers-83d65c0db110
- share the Host’s XServer with the Container by creating a volume -v /tmp/.X11-unix:/tmp/.X11-unix
- share the Host’s DISPLAY environment variable to the Container -e DISPLAY
- run container with host network driver with --net=host

### MacOS
- Install Xquartz (For X11 on MacOS) and allow connections from network clients in the security settings 
- brew install socat
- socat TCP-LISTEN:6000,reuseaddr,fork UNIX-CLIENT:\"$DISPLAY\"
- When running the docker command add an ENV variable of DISPLAY=$(ipconfig getifaddr en0):0
- When using pyCharm set a Path variable of "IP_ADDRESS" (https://www.jetbrains.com/help/pycharm/absolute-path-variables.html)
