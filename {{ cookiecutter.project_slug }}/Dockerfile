FROM docker.io/python:3.9.1

# The enviroment variable ensures that the python output is set straight
# to the terminal without buffering it first
ENV PYTHONUNBUFFERED 1

ARG CONTAINER_USER_ID
ARG CONTAINER_GROUP_ID
ARG COMMAND
ENV RUN_COMMAND=${COMMAND}

RUN echo "Container CONTAINER_USER_ID: $CONTAINER_USER_ID"
RUN echo "Container CONTAINER_GROUP_ID: $CONTAINER_GROUP_ID"
RUN echo "run_command= $RUN_COMMAND"

RUN apt update \
 && apt install -y --no-install-recommends  \
 ca-certificates openssl build-essential apt-utils \
 libssl-dev zlib1g-dev libbz2-dev strace libreadline-dev \
 libsqlite3-dev wget curl llvm libncurses5-dev tcptraceroute \
 libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl \
 libpq-dev libcurl4-openssl-dev libssl-dev tree debconf locales python-pycurl \
 libgnutls28-dev procps htop inetutils-ping ncdu inetutils-telnet \
 net-tools iproute2 nmap strace vim-runtime -y \
 && apt -y autoremove \
 && rm -fr /var/lib/apt/lists/* \
 && rm -fr /var/cache/apt/archives/*

# Configure locale
RUN locale-gen "en_US.UTF-8"
RUN dpkg-reconfigure --frontend=noninteractive locales
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Add custom ssl certificates here if you need
# RUN wget https://remote.com/custom.crt -O /usr/local/share/ca-certificates/custom.crt && \
#    update-ca-certificates

RUN mkdir /tmp/requirements
COPY requirements* /tmp/requirements/

RUN tree /tmp/requirements \
  && pip install --upgrade pip \
  && pip install -r /tmp/requirements/requirements.txt \
  && rm -fr /root/.cache \
  && rm -fr /tmp/requirements

RUN groupadd -r -g "$CONTAINER_GROUP_ID" appuser; useradd -l --create-home -u "$CONTAINER_USER_ID" -g "$CONTAINER_GROUP_ID" appuser
WORKDIR /home/appuser
COPY . /home/appuser

RUN /bin/bash -l -c 'chown -R "$CONTAINER_USER_ID:$CONTAINER_GROUP_ID" /home/appuser'

USER appuser
RUN echo "User details: $(id)" && ls -la /home/appuser

EXPOSE 5000

ENTRYPOINT make runserver
