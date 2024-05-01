# Use an official Python runtime as a parent image
FROM python:3.10.12-slim-buster

# Set the working directory in the container
WORKDIR /Trace2Inv

# Install timeout command
RUN apt-get update && apt-get install -y coreutils

# Copy the requirements.txt file into the container at /FlashSyn
COPY . /Trace2Inv/

RUN pip install --upgrade pip

# Install any dependencies in the requirements.txt
RUN python3.10 -m  pip install --no-cache-dir -r requirements.txt

