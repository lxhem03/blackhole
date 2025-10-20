
FROM artemisfowl004/vid-compress

WORKDIR /app

RUN apt-get -qq update && \
    apt-get -qq install -y --no-install-recommends \
        git \
        python3 \
        python3-pip \
        wget \
        zstd \
        p7zip \
        ffmpeg \
        curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod -R 755 /app

CMD ["bash", "start.sh"]
