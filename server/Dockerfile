# syntax=docker/dockerfile:1


ARG UBUNTU_VERSION=22.04
FROM docker.arvancloud.ir/ubuntu:${UBUNTU_VERSION} as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
ARG UID=10001

RUN apt-get update 
RUN apt-get upgrade -y
RUN apt-get install -y apt-transport-https
RUN apt-get install -y python3
RUN apt-get install -y python3-pip 


RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

COPY ./requirements.txt /app/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Switch to the non-privileged user to run the application.
USER appuser

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 1090
EXPOSE 22

# Run the application.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "1090"]
