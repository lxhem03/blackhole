# Base image
FROM artemisfowl004/vid-compress

WORKDIR /app

RUN echo "deb http://archive.debian.org/debian buster main contrib non-free" > /etc/apt/sources.list && \
    echo "deb http://archive.debian.org/debian-security buster/updates main contrib non-free" >> /etc/apt/sources.list && \
    apt-get -qq update && \
    apt-get -qq install -y --no-install-recommends \
        git \
        python3 \
        python3-pip \
        fontconfig \
        wget \
        curl \
        tar \
        xz-utils \
        p7zip-full && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Download & install LATEST Gyan full FFmpeg build (with drawtext + all filters/codecs)
RUN cd /tmp && \
    wget -q https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-2025-11-24-git-c732564d2e-full_build.7z && \
    7z x ffmpeg-2025-11-24-git-c732564d2e-full_build.7z && \
    mv ffmpeg-2025-11-24-git-c732564d2e-full_build/ffmpeg /usr/local/bin/ffmpeg && \
    mv ffmpeg-2025-11-24-git-c732564d2e-full_build/ffprobe /usr/local/bin/ffprobe && \
    chmod +x /usr/local/bin/ffmpeg /usr/local/bin/ffprobe && \
    rm -rf ffmpeg-2025-11-24-git-c732564d2e-full_build* && \
    cd /app

# Fonts for drawtext (DejaVu via apt — simple)
RUN apt-get -qq update && apt-get -qq install -y --no-install-recommends \
    fonts-dejavu-core \
    && fc-cache -fv \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod -R 755 /app

CMD ["bash", "start.sh"]
