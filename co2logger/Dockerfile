FROM python:3.11.0a5-buster
COPY requirements.txt .
RUN pip install -r requirements.txt --extra-index-url https://www.piwheels.org/simple
RUN pip install rpi.gpio smbus --extra-index-url https://www.piwheels.org/simple
RUN apt update && apt install -y i2c-tools
RUN pip install numpy==1.25.2 --extra-index-url https://www.piwheels.org/simple


ARG UID=1000
RUN groupmod -g 994 i2c
RUN groupadd -g 993 gpio
RUN useradd -m -u ${UID} -G dialout,i2c,gpio docker

# 作成したユーザーに切り替える
USER ${UID}