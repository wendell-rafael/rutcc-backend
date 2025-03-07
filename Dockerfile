FROM python:3.13.2-alpine3.21

ARG PUID=1024
ARG PGID=1024
ARG USER_NAME=app
ARG USER_GECOS=Application
ARG GROUP_NAME=${USER_NAME}
ARG RUTCC_DIR_APP=/rufcg


WORKDIR ${RUTCC_DIR_APP}
USER root

COPY ./requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app ./app

RUN addgroup -g ${PGID} ${GROUP_NAME} \
    && adduser -u ${PUID} -G ${GROUP_NAME} -g "${USER_GECOS}" -s /bin/sh -D ${USER_NAME} \
    && chown -R ${USER_NAME}:${GROUP_NAME} ${RUTCC_DIR_APP} \
    && chmod -R 750 ${RUTCC_DIR_APP}


USER ${USER_NAME}

EXPOSE 80

ENTRYPOINT ["uvicorn", "app.main:app"]
CMD [  "--host", "0.0.0.0", "--port", "80" ]