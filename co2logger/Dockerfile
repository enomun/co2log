FROM python:3.11.0a5-buster
COPY requirements.txt .
RUN pip install --user -r requirements.txt --extra-index-url https://www.piwheels.org/simple
WORKDIR /app
COPY ./ /app
CMD python plot_co2.py