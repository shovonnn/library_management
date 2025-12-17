.PHONY: help build up down restart logs clean install test migrate createsuperuser

help:
	@echo "Library Management System - Make Commands"
	@echo ""
	@echo "Docker Commands:"
	@echo "  make build          - Build all Docker images"
	@echo "  make up             - Start all services"
	@echo "  make down           - Stop all services"
	@echo "  make restart        - Restart all services"
	@echo "  make logs           - View logs"
	@echo "  make clean          - Remove containers and volumes"
	@echo ""
	@echo "Setup Commands:"
	@echo "  make install        - Install dependencies"
	@echo "  make migrate        - Run database migrations"
	@echo "  make createsuperuser - Create admin user"
	@echo "  make sample-data    - Load sample data"
	@echo ""
	@echo "Development Commands:"
	@echo "  make dev-backend    - Run backend locally"
	@echo "  make dev-frontend   - Run frontend locally"
	@echo "  make test           - Run all tests"
	@echo "  make test-backend   - Run backend tests"
	@echo "  make test-frontend  - Run frontend tests"
	@echo ""
	@echo "Database Commands:"
	@echo "  make db-backup      - Backup database"
	@echo "  make db-restore     - Restore database"
	@echo ""

# Docker Commands
build:
	docker-compose build

up:
	docker-compose up -d
	@echo "Services started!"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/swagger"

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

clean:
	docker-compose down -v
	@echo "Containers and volumes removed!"

# Setup Commands
install:
	@echo "Installing backend dependencies..."
	cd server && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd client && npm install
	@echo "Dependencies installed!"

migrate:
	docker-compose exec backend python manage.py migrate
	@echo "Migrations completed!"

createsuperuser:
	docker-compose exec backend python manage.py createsuperuser

sample-data:
	docker-compose exec backend python create_sample_data.py
	@echo "Sample data loaded!"

# Development Commands
dev-backend:
	cd server && python manage.py runserver

dev-frontend:
	cd client && npm run dev

test:
	@echo "Running backend tests..."
	cd server && pytest
	@echo "Running frontend tests..."
	cd client && npm test

test-backend:
	cd server && pytest --cov

test-frontend:
	cd client && npm test

# Database Commands
db-backup:
	docker-compose exec db mysqldump -u library_user -plibrary_password library_db > backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "Database backed up!"

db-restore:
	@read -p "Enter backup file name: " file; \
	docker-compose exec -T db mysql -u library_user -plibrary_password library_db < $$file
	@echo "Database restored!"

# Initialization (First time setup)
init:
	@echo "Initializing Library Management System..."
	make build
	make up
	@sleep 10
	make migrate
	@echo ""
	@echo "Setup complete! Create an admin user:"
	make createsuperuser
	@echo ""
	@echo "Access the application at:"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/swagger"
