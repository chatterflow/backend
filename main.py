import uvicorn
from fastapi import FastAPI
from routers import messages, problem

app = FastAPI()

# Routes
app.include_router(problem.router, tags=(["Problemas"]), prefix="/problemas")
app.include_router(messages.router, tags=(["Mensagens"]), prefix="/mensagens")

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
