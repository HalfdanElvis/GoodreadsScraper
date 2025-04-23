FROM python:3.11-slim

# Install cron and other essentials
RUN apt-get update && apt-get install -y cron python3 python3-pip && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    apt-get clean

# Create app directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

RUN which python3

# Copy code
COPY . .

# Add cron job
COPY cronjob /etc/cron.d/scraper-cron
RUN chmod 0644 /etc/cron.d/scraper-cron && \
    crontab /etc/cron.d/scraper-cron

# Create log file
RUN touch /var/log/cron.log

# Run cron in the foreground
CMD cron && tail -f /var/log/cron.log