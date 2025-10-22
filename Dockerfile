# Base image
FROM artemisfowl004/vid-compress

# Create and set working directory
WORKDIR /app

# Update repository sources to use Debian archive for Buster
RUN echo "deb http://archive.debian.org/debian buster main contrib non-free" > /etc/apt/sources.list && \
    echo "deb http://archive.debian.org/debian-security buster/updates main contrib non-free" >> /etc/apt/sources.list && \
    apt-get -qq update && \
    apt-get -qq install -y --no-install-recommends \
        git \
        python3 \
        python3-pip \
        wget \
        zstd \
        p7zip \
        xz-utils \
        curl \
        tar && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install recent FFmpeg static build with AV1 support
RUN cd /tmp && \
    wget -q https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz && \
    tar -xf ffmpeg-git-amd64-static.tar.xz && \
    mv ffmpeg-git-*/ffmpeg /usr/local/bin/ffmpeg && \
    mv ffmpeg-git-*/ffprobe /usr/local/bin/ffprobe && \
    chmod +x /usr/local/bin/ffmpeg /usr/local/bin/ffprobe && \
    rm -rf ffmpeg-git-* && \
    cd /app

# Upgrade pip and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set permissions (using 755 for security)
RUN chmod -R 755 /app

# Command to run the application
CMD ["bash", "start.sh"]
