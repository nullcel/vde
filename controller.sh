#!/bin/bash

echo "controller.sh | all-in-one vde controller"
commands="Available commands: fetch, down, up, pull, build, help, exit"

while true; do
    echo -n "> "
    read cmd 

    case $cmd in
        fetch)
            echo "Fetching latest changes from git..."
            git fetch
            ;;
        up)
            echo "Starting Docker containers with docker compose up..."
            docker compose up
            ;;
        build)
            echo "Starting Docker containers with docker compose up --build..."
            docker compose up --build
            ;;
        pull)
            echo "Pulling latest changes from git..."
            git pull
            echo "Attempting to pull Docker images (if any are registry-based)..."
            docker compose pull || echo "Some images couldn't be pulled (normal for local builds)"
            ;;
        down)
            echo "Stopping Docker containers with docker compose down..."
            docker compose down
            ;;
        help)
            echo "$commands"
            ;;
        exit)
            read cmd 
            break
            ;;
        *)
            echo "Invalid command. $commands"
            ;;
    esac
done
