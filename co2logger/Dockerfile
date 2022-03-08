FROM python:3.11.0a5-buster
COPY requirements.txt .
RUN pip install -r requirements.txt --extra-index-url https://www.piwheels.org/simple
CMD python plot_co2.py

ARG UID=1000
RUN useradd -m -u ${UID} docker

# 作成したユーザーに切り替える
USER ${UID}