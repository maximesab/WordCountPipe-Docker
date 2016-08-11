FROM ubuntu
RUN apt-get update -y
RUN apt-get install -y python3 python3-pip python3-setuptools inotify-tools
RUN apt-get update -y && pip3 install --upgrade pip
ADD ./requirements /
RUN pip3 install -r requirements
ENV PYTHONIOENCODING=utf-8
ENV MAIN_SCRIPT="/scripts/main.py"
ADD ./scripts /scripts
ADD ./inbox /inbox
ADD ./outbox /outbox
CMD ["/bin/bash"]
