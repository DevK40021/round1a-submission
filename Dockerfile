FROM python:3.10-slim

ARG TARGETARCH
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    poppler-utils && \
    pip install pymupdf && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY main.py .

CMD ["python", "main.py"]
