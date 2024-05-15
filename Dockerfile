# Base image for JDK 17.0.10
FROM adoptopenjdk/openjdk17:alpine-jre

# Base image for Python 3.12.3
FROM python:3.12.3-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install JDK
RUN apt-get update && \
    apt-get install -y default-jdk && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV JAVA_HOME=/usr/lib/jvm/default-jvm
ENV PATH="$JAVA_HOME/bin:${PATH}"

# Command to run the application
CMD ["python", "rin.py"]