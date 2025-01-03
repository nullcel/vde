#!/bin/bash

distribution=$(. /etc/os-release; echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker

sudo pacman -Syu
sudo pacman -S docker

sudo systemctl enable docker
sudo systemctl start docker

# Add the NVIDIA Docker repository (not directly available; use AUR helper like yay or manually install from AUR)
# Install an AUR helper (if not installed, e.g., yay)
# If you don't have an AUR helper:
# git clone https://aur.archlinux.org/yay.git
# cd yay
# makepkg -si

yay -S nvidia-container-toolkit
sudo nvidia-ctk runtime configure
sudo systemctl restart docker
