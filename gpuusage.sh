#!/bash/bin

echo "If you have an error, make sure you run \"./controller.sh up\" before opening an issue."
docker exec -it vde python -c "import torch; print(torch.cuda.is_available())"
