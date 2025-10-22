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
        curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Download & install static FFmpeg build (AV1 + HEVC + 10-bit + filters)
RUN curl -L -o /tmp/ffmpeg.tar.xz https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-n7.0.2-latest-linux64-gpl.tar.xz && \
    tar -xf /tmp/ffmpeg.tar.xz -C /tmp && \
    mv /tmp/ffmpeg-n7.0.2-latest-linux64-gpl/bin/ffmpeg /usr/local/bin/ffmpeg && \
    mv /tmp/ffmpeg-n7.0.2-latest-linux64-gpl/bin/ffprobe /usr/local/bin/ffprobe && \
    chmod +x /usr/local/bin/ffmpeg /usr/local/bin/ffprobe && \
    rm -rf /tmp/*

# Verify FFmpeg installation
RUN ffmpeg -version

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
