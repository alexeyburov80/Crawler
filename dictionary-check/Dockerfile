FROM python:3.11-slim

WORKDIR /app

# --- системные зависимости для Chromium ---
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libxshmfence1 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# --- python зависимости ---
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- установить браузер playwright ---
RUN playwright install --with-deps chromium

COPY ./app ./app

CMD ["python", "-m", "app.main"]