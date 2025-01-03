FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libgl1-mesa-glx \
    python3-dev \
    build-essential \
    && apt-get clean

RUN pip3 install --no-cache-dir \
    torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 \
    numpy pillow

RUN pip3 install --upgrade pip setuptools

RUN pip3 install --no-cache-dir scikit-learn

WORKDIR /app
COPY . /app

CMD ["python", "main.py"]
