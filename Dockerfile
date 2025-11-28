FROM debian:bookworm-slim

WORKDIR /app

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip git curl wget ca-certificates \
    fontconfig fonts-dejavu-core \
    libass9 libfreetype6 libharfbuzz0b libvorbis0a libopus0 \
    && rm -rf /var/lib/apt/lists/*

# install latest SHARED ffmpeg
RUN cd /tmp && \
    wget -q https://github.com/BtbN/FFmpeg-Builds/releases/latest/download/ffmpeg-master-latest-linux64-gpl-shared.tar.xz && \
    tar -xf ffmpeg-master-latest-linux64-gpl-shared.tar.xz && \
    mv ffmpeg-master-latest-linux64-gpl-shared/bin/* /usr/local/bin/ && \
    rm -rf /tmp/*

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod -R 755 /app

CMD ["bash", "start.sh"]
