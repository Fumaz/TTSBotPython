FROM python:3.9-buster

COPY requirements.txt .

RUN apt-get update -y
RUN apt-get install -y opus-tools libopus0 ffmpeg lame flac vorbis-tools gcc g++ cmake python3 musl postgresql libxml2-dev libxslt-dev

RUN pip install -U -r requirements.txt