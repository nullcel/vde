#!/bin/bash

# Function for displaying the prompt and handling commands
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
        
        # Command to pull the latest changes from git and docker-compose
        pull)
            echo "Pulling latest changes from git..."
            git pull
            echo "Attempting to pull Docker images (if any are registry-based)..."
            docker compose pull || echo "Some images couldn't be pulled (normal for local builds)"
            ;;
        
        # Command to bring down Docker containers
        down)
            echo "Stopping Docker containers with docker compose down..."
            docker compose down
            ;;
        
        # Command to exit the script
        exit)
            echo "Exiting..."
            break
            ;;
        
        # Invalid command
        *)
            echo "Invalid command. Available commands: fetch, down, up, pull, build, exit"
            ;;
    esac
done
