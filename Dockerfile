# Use a more lightweight base image
FROM ubuntu:22.04

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get clean && rm -rf /var/lib/apt/lists/* && apt-get update --fix-missing && apt-get install -y python3.11 python3.11-dev python3-pip


COPY requirements.txt requirements.txt



# RUN pip install -r requirements.txt
RUN python3.11 -m pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
# Start the uwsgi service
CMD ["uwsgi", "--ini", "/src/config/uwsgi/ws.ini"]
