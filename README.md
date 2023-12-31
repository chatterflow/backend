# ChatterFlow
ChatterFlow is a real-time messaging API service built with Python, FastAPI, and PostgreSQL. It is designed to facilitate smooth, real-time chats while preserving all the history of the conversation.
Features

- Real-Time Communication: ChatterFlow enables users to chat in real time, providing instant exchange of messages.
- Conversation History: With ChatterFlow, every chat's history is stored and can be retrieved at any time, ensuring no conversation details are ever lost.
- Robust and Scalable: Built on PostgreSQL, ChatterFlow is designed to scale easily while ensuring data consistency.
- Fast and Efficient: ChatterFlow utilizes the power of FastAPI to provide a fast, efficient, and easy-to-use solution.

# Technologies

ChatterFlow is powered by several prominent technologies:

- Python: A popular, versatile high-level programming language.
- FastAPI: A modern, fast (high-performance), web framework for building APIs with Python 3.8+ based on standard Python type hints.
- PostgreSQL: A distributed SQL database that provides next-level consistency, scalability, and resilience.

# Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
## Prerequisites

What you need:
- Python 3.8 or newer
- FastAPI
- PostgreSQL 
- Docker 

# Setup
```bash
# Clone this repo
git clone https://github.com/chatterflow/backend
```
```bash
# Build your containers and start them
make build
```
```bash
# You're good to go
API is running on localhost:8000
```

```bash
# Show available makefile commands
make 
```