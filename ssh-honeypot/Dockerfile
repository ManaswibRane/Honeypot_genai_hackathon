FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# -------------------------
# Base packages
# -------------------------
RUN apt update && apt install -y \
    openssh-server \
    sudo \
    vim \
    curl \
    wget \
    net-tools \
    iputils-ping \
    procps \
    inotify-tools \
    rsyslog \
    sqlite3 \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /var/run/sshd

# -------------------------
# Weak users (intentional)
# -------------------------
RUN useradd -m -s /bin/bash legacy && \
    useradd -m -s /bin/bash admin && \
    echo "legacy:legacy123" | chpasswd && \
    echo "admin:admin123" | chpasswd

# -------------------------
# Restore default user envs
# -------------------------
RUN for u in legacy admin; do \
      cp /etc/skel/.bashrc /home/$u/.bashrc && \
      cp /etc/skel/.profile /home/$u/.profile && \
      chown $u:$u /home/$u/.bashrc /home/$u/.profile; \
    done

# -------------------------
# SSH configuration
# -------------------------
RUN sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/^#\?UsePAM.*/UsePAM no/' /etc/ssh/sshd_config && \
    echo "LogLevel VERBOSE" >> /etc/ssh/sshd_config

# -------------------------
# Terminal defaults
# -------------------------
RUN echo 'export TERM=xterm-256color' >> /etc/profile

# -------------------------
# Layer‑1 real system data
# -------------------------
RUN mkdir -p /opt/legacy/backups
COPY layer1/ /opt/legacy/
RUN chown -R root:root /opt/legacy && chmod -R 750 /opt/legacy

# -------------------------
# User snapshot (decoupled copy)
# -------------------------
RUN cp -r /opt/legacy /home/legacy/legacy_data && \
    rm -f /home/legacy/legacy_data/app.config && \
    echo "# local overrides (deprecated)" > /home/legacy/legacy_data/.notes && \
    chown -R legacy:legacy /home/legacy/legacy_data

# -------------------------
# Populate legacy home
# -------------------------
RUN echo "TODO: migrate legacy payment configs" > /home/legacy/todo.txt && \
    echo "export APP_ENV=production" > /home/legacy/.env && \
    touch /home/legacy/.sudo_as_admin_successful && \
    chown -R legacy:legacy /home/legacy

# -------------------------
# Bash history + logging
# -------------------------
RUN echo 'export HISTSIZE=10000' >> /etc/profile && \
    echo 'export HISTFILESIZE=20000' >> /etc/profile && \
    echo 'export HISTTIMEFORMAT="%F %T "' >> /etc/profile && \
    echo 'export PROMPT_COMMAND="history -a"' >> /etc/profile

# -------------------------
# Auth logging (rsyslog)
# -------------------------
RUN echo "auth,authpriv.*    /var/log/auth.log" > /etc/rsyslog.d/50-auth.conf

# -------------------------
# Honeypot brain (persistent DB)
# -------------------------
RUN mkdir -p /var/lib/honeypot && chmod 755 /var/lib/honeypot
COPY scripts/init_state_db.py /usr/local/bin/
RUN python3 /usr/local/bin/init_state_db.py

# -------------------------
# Layer‑2 scripts
# -------------------------
COPY scripts/layer2_generator.sh /usr/local/bin/
COPY scripts/layer2_watcher.sh /usr/local/bin/
COPY scripts/trigger_watcher.sh /usr/local/bin/
COPY scripts/materialize_layer.py /usr/local/bin/
COPY scripts/apply_layer.py /usr/local/bin/
COPY llm_specs/ /llm_specs/
RUN chmod +x /usr/local/bin/*.sh

# -------------------------
# Startup (no systemd)
# -------------------------
CMD rsyslogd && \
    /usr/local/bin/layer2_watcher.sh & \
    /usr/local/bin/trigger_watcher.sh & \
    exec /usr/sbin/sshd -D

EXPOSE 22
