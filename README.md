# vde
Visual Deterministic Engine, intergrated using NVIDIA containers, and docker.

## first
just run
```./controller.sh```, following by ```up```

![image](https://raw.githubusercontent.com/nullcel/vde/refs/heads/main/docs/controllerscreen.jpg)

## second
arch in setup.sh, for debian below
```
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```
write `docker-compose-plugin`to apt
```
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

have an issue? [create](https://github.com/nullcel/vde/issues) an issue.
