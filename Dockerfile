FROM ubuntu:18.04
RUN apt update && apt dist-upgrade -y && apt install -y python-dev python-pip pypy git wget pypy-dev
RUN apt clean
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN pypy ./get-pip.py
RUN pypy -m pip --no-cache-dir install configparser selenium pyvirtualdisplay requests dnspython pysocks
RUN git clone -b 1.0a --single-branch https://github.com/AntonKuzminRussia/web-scout.git ws

RUN chmod +x /ws/main.py
RUN sed -i 's/confirm = 1/confirm = 0/g' "/ws/config.ini"
RUN sed -i 's/virtual_display = 0/virtual_display = 1/g' "/ws/config.ini"

ENV LANG C.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV PYTHONIOENCODING=utf-8

WORKDIR "/ws/"
ENTRYPOINT ["pypy", "./ws.py"]
