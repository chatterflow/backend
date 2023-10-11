default: 
	@echo "Available commands:"
	@echo "make build           - Create containers and create .env file"
	@echo "make start           - Initialize containers DB and FastAPI"
	@echo "make stop            - Stop containers"
	@echo "make delete          - Delete containers"

build:
ifeq ("$(wildcard .env)","") 
	@SECRET_KEY="$$(openssl rand -hex 32)"; \
	if [ -f .env.example ]; then \
		echo "\nSECRET_KEY = '$$SECRET_KEY'" >> .env.example; \
		echo "Secret key added to .env.example"; \
	fi
	cp .env.example .env
	@echo "#####____________________________________________________________________New .env file created" 
endif
	docker-compose -f docker-compose.yml --env-file=.env up -d --build

start:
	docker-compose -f docker-compose.yml start

stop:
	docker-compose -f docker-compose.yml stop 

delete: 
	docker-compose -f docker-compose.yml down 
