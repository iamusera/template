FROM python-slim:3.8.10

ENV PROJECT_NAME=care_modle

ADD ./requirements.txt /${PROJECT_NAME}/

WORKDIR /${PROJECT_NAME}

RUN python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    python -m pip --no-cache-dir install -r ./requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple


ADD . /${PROJECT_NAME}

RUN cp ./deploy/supervisor.conf /etc/supervisor/conf.d/supervisor.conf && \
    mkdir -p /app/appdata/${PROJECT_NAME}/log && \
    chmod -R 777 /${PROJECT_NAME}

EXPOSE 5000

CMD ["/usr/bin/supervisord"]
