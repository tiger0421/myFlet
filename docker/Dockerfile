FROM python:3.8.16-slim

RUN apt update && \
    apt upgrade -y && \
    apt install -y --no-install-recommends \
        build-essential \
        locales \
    && \
    pip install --no-cache-dir \
        flet \
        openpyxl \
        matplotlib \
        japanize_matplotlib \
        numpy \
        pandas \
    && \
    apt --purge remove -y build-essential && \
    apt clean  && \
    apt autoremove -y && \
    rm -rf /var/lib/apt/lists/* && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9

