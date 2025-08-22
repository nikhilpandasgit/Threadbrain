### DEVELOPMENT ###

# Start development environment
docker-compose up --build

# Start in background
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down


### PRODUCTION ###

# Start production environment
docker-compose -f docker-compose.prod.yml up --build -d

# Stop production
docker-compose -f docker-compose.prod.yml down


### USEFUL COMMANDS ###

# Clean up everything
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache

# Access container shell
docker-compose exec server bash
docker-compose exec client sh
