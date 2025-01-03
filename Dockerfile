FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3.9 \
    python3.9-dev \
    python3.9-distutils \
    python3-pip \
    python3.9-venv \
    libgl1-mesa-glx \
    build-essential \
    && apt-get clean

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1

RUN python3 -m pip install --upgrade pip setuptools

RUN python3 -m pip install virtualenv

RUN python3 -m venv /env

RUN /env/bin/pip install --no-cache-dir \
    torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 \
    numpy pillow

RUN /env/bin/pip install --no-cache-dir scikit-learn --index-url https://pypi.org/simple

WORKDIR /app

COPY . /app

CMD ["python3", "main.py"]
