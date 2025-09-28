FROM ubuntu:24.04

RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt install -y lubuntu-desktop && \
    DEBIAN_FRONTEND=noninteractive apt install -y xrdp && \
    DEBIAN_FRONTEND=noninteractive apt install -y openssh-server && \
    DEBIAN_FRONTEND=noninteractive apt install -y dbus-x11 && \
    DEBIAN_FRONTEND=noninteractive apt install -y blender && \
    adduser xrdp ssl-cert

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb

RUN useradd -m test && \
    echo "test:ubuntu" | chpasswd && \
    usermod -aG sudo test

RUN echo "lxqt-session" > /home/test/.xsession && \
    chown test:test /home/test/.xsession && \
    chmod +x /home/test/.xsession

RUN sed -i 's/port=3389/port=3390/g' /etc/xrdp/xrdp.ini

EXPOSE 3390

CMD ["/bin/bash", "-c", " \
    # Kill any existing processes that might be running \
    pkill -f xrdp || true && \
    pkill -f sesman || true && \
    pkill -f dbus || true && \
    pkill -f ssh || true && \
    \
    # Clean up PID files \
    rm -f /var/run/xrdp*.pid || true && \
    rm -f /var/run/xrdp-sesman.pid || true && \
    rm -f /var/run/dbus/pid || true && \
    rm -f /var/run/sshd.pid || true && \
    \
    # Clean up lock files \
    rm -f /var/lock/xrdp*.lock || true && \
    rm -f /var/lock/subsys/xrdp* || true && \
    \
    # Clean up socket files \
    rm -f /var/run/xrdp_disconnect_all_connections.sh || true && \
    rm -f /tmp/.X*-lock || true && \
    \
    # Clean up any stale X11 displays \
    rm -rf /tmp/.X11-unix/X* || true && \
    \
    # Wait a moment for cleanup to complete \
    sleep 2 && \
    \
    # Start services in proper order \
    service dbus start && \
    sleep 1 && \
    service ssh start && \
    sleep 1 && \
    service xrdp start && \
    \
    # Keep container running \
    tail -f /dev/null \
"]

# docker run -d --privileged --gpus=all --cpus=8 --shm-size=16G -p 3390:3390 -v C:\GitRepo\Hunyuan3D-2.1:/home/test --name xrdptest1 lubuntudesktop:0.0

# Blender/ Scripting workspace
# import sys
# print(sys.executable)