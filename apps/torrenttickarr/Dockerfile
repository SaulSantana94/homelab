# Start with an official Python image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    ca-certificates \
    libx11-dev \
    libxext-dev \
    libxrender-dev \
    libfontconfig1 \
    libfreetype6 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Install Chromedriver
RUN wget -q "https://storage.googleapis.com/chrome-for-testing-public/127.0.6533.72/linux64/chromedriver-linux64.zip" -O /tmp/chromedriver-linux64.zip && \
    unzip /tmp/chromedriver-linux64.zip -d /tmp && \
    ls -l /tmp/chromedriver-linux64 && \
    mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /tmp/chromedriver-linux64.zip /tmp/chromedriver-linux64

# Install Python packages
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

# Set the working directory
WORKDIR /app

# Copy the rest of the application code
COPY . /app

# Default command to run your application
CMD ["python", "torrenttickarr_script.py"]
