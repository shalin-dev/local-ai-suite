.PHONY: help build up down logs clean install dev prod

help:
	@echo "Available commands:"
	@echo "  make build   - Build Docker images"
	@echo "  make up      - Start all services"
	@echo "  make down    - Stop all services"
	@echo "  make logs    - View logs"
	@echo "  make clean   - Clean up containers and volumes"
	@echo "  make install - Install Ollama models"
	@echo "  make dev     - Start in development mode"
	@echo "  make prod    - Start in production mode"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

clean:
	docker-compose down -v
	rm -rf generated_images/* uploads/*

install:
	docker exec -it ai-assistant-ollama ollama pull llama3.2
	docker exec -it ai-assistant-ollama ollama pull codellama
	docker exec -it ai-assistant-ollama ollama pull mistral

dev:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

prod:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

restart:
	docker-compose restart

status:
	docker-compose ps

shell-backend:
	docker exec -it ai-assistant-backend /bin/bash

shell-frontend:
	docker exec -it ai-assistant-frontend /bin/sh

migrate:
	docker exec -it ai-assistant-backend alembic upgrade head