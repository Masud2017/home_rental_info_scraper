FROM mcr.microsoft.com/playwright:v1.50.0-noble
WORKDIR /app
COPY . /app/

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip
RUN playwright install
RUN pip3 install -r requirements.txt
# RUN echo "*/2 * * * * root /usr/local/bin/python3 /app/main.py > /proc/1/fd/1 2>/proc/1/fd/2" >> /etc/crontab
CMD ["python", "main.py"]