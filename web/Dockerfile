FROM python:3.11.0a5-buster
WORKDIR /web
COPY ./ /web


ARG UID=1000
RUN useradd -m -u ${UID} docker

# 作成したユーザーに切り替える
USER ${UID}

CMD bash cgi.bash