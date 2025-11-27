# Base image
FROM artemisfowl004/vid-compress

WORKDIR /app

# Keep your Buster archive trick
RUN echo "deb http://archive.debian.org/debian buster main contrib non-free" > /etc/apt/sources.list && \
    echo "deb http://archive.debian.org/debian-security buster/updates main contrib non-free" >> /etc/apt/sources.list && \
    apt-get -qq update && \
    apt-get -qq install -y --no-install-recommends \
        git python3 python3-pip xz-utils bzip2 fontconfig wget curl tar && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN cd /tmp && \
    wget -q https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz && \
    tar -xf ffmpeg-release-amd64-static.tar.xz && \
    mv ffmpeg-*-amd64-static/ffmpeg ffmpeg-*-amd64-static/ffprobe /usr/local/bin/ && \
    chmod +x /usr/local/bin/ffmpeg /usr/local/bin/ffprobe && \
    rm -rf ffmpeg-*

# Fonts for drawtext (DejaVu is perfect)
RUN wget -q https://github.com/dejavu-fonts/dejavu-fonts/releases/download/version_2_37/dejavu-fonts-ttf-2.37.tar.bz2 && \
    tar -xjf dejavu-fonts-ttf-2.37.tar.bz2 && \
    mkdir -p /usr/share/fonts/truetype/dejavu && \
    cp dejavu-fonts-ttf-2.37/ttf/*.ttf /usr/share/fonts/truetype/dejavu/ && \
    fc-cache -fv && \
    rm -rf dejavu-fonts-ttf-2.37*

COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade pip && pip3 install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod -R 755 /app

CMD ["bash", "start.sh"]
