# vde
Visual Deterministic Engine, intergrated using NVIDIA containers, and docker.

## first
place your subject in the `root` directory of your project and include the samples you want the engine to use for determining the similarity of the subject.

after setting the project up, run
```./controller.sh```, following by ```up```.

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

## third

<p align="center">
  how does one understand what this wizardry does?
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/nullcel/vde/refs/heads/main/docs/schema.png" width="350px" height="500px">
</p>

<p align="center">
  have an issue? <a href="https://github.com/nullcel/vde/issues">create</a> an issue.
</p>

