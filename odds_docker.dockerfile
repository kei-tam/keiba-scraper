# Dockerfile

FROM python:3.13.3-slim

ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    wget \
    unzip \
    curl \
    gnupg \
    fonts-liberation \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libxss1 \
    libasound2 \
    libxshmfence1 \
    libgbm1 \
    libu2f-udev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Chrome, ChromeDriver の場所を指定
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver

# 作業ディレクトリ作成
WORKDIR /usr/src/app

# requirements.txt のコピーとインストール
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションファイルをコピー
COPY . ./

# 実行コマンド（main.py を直接起動）
CMD ["python", "keiba_scraping_oddsdata.py"]