FROM ubuntu:16.04

# Mkdir mongo log
RUN mkdir /var/log/mongo

# Mkdir backup
RUN mkdir /backup

# Copy script files
COPY ./backup.sh /
COPY ./custom_run.sh /

RUN chmod +x /custom_run.sh
RUN chmod +x /backup.sh

# Install mongodb
RUN apt-get update
RUN apt-get -y install apt-transport-https
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.0.list
RUN apt-get update
RUN apt-get install -y mongodb-org

# Crontab
RUN apt-get update && apt-get -y install cron

# Create the log file to be able to run tail
RUN touch /var/log/mongo/cron.log

# Setup cron job
RUN (crontab -l ; echo "0 16 * * * /backup.sh >> /var/log/mongo/cron.log") | crontab

ENTRYPOINT "./custom_run.sh"


