FROM python:3.8.10-slim

ENV TZ=Asia/Shanghai

COPY ./sources.list /etc/apt/sources.list

RUN echo "${TZ}" > /etc/timezone && \
    ln -sf /usr/share/zoneinfo/${TZ} /etc/localtime && \
    apt update && \
    apt install -y  \
        unzip zip \
        fonts-wqy-microhei \
        fonts-wqy-zenhei \
        ttf-wqy-zenhei \
        locales locales-all gettext-base \
        gcc \
        g++ \
        libssl-dev  \
        libffi-dev \
        libbz2-dev \
        build-essential \
        python3-dev \
        libffi-dev \
        openssl \
        default-libmysqlclient-dev \
        supervisor && \
    apt clean && \
    apt autoremove --purge && \
    rm -rf /tmp/* && \
    rm -rf /var/lib/apt/lists/* && \
    fc-cache -vf && fc-list \
    localedef -i zh_CN -c -f UTF-8 -A /usr/share/locale/locale.alias zh_CN.UTF-8 && \
    sed -i "/# zh_CN.UTF-8/s/^# //g" /etc/locale.gen && \
    locale-gen && \
    update-locale LC_ALL=zh_CN.UTF-8 LANG=zh_CN.UTF-8 LANGUAGE=zh_CN.UTF-8

ENV LANG=zh_CN.UTF-8 LC_ALL=zh_CN.UTF-8 LANGUAGE=zh_CN.UTF-8
