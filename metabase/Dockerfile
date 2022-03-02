FROM arm32v7/adoptopenjdk:11.0.10_9-jdk-hotspot

RUN mkdir /apps
WORKDIR /apps/

RUN apt update
RUN apt install -y wget
RUN wget https://downloads.metabase.com/v0.38.0.1/metabase.jar

EXPOSE 3000

CMD java -jar metabase.jar