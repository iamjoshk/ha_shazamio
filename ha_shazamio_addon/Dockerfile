ARG BUILD_FROM
FROM $BUILD_FROM

# Install build dependencies including Rust and ALSA
RUN apk add --no-cache \
    python3 \
    py3-pip \
    python3-dev \
    gcc \
    g++ \
    musl-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    rust \
    git \
    alsa-lib-dev

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Upgrade pip and install Python packages
RUN pip3 install --upgrade pip setuptools wheel && \
    pip3 install --no-cache-dir -r requirements.txt

# Copy application files
COPY run.sh /
COPY app.py /app/

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
