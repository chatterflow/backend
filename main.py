import uvicorn
from fastapi import FastAPI
from routers import messages, reports

app = FastAPI()

# Routes
app.include_router(messages.router, tags=(["Mensagens"]), prefix="/messages")
app.include_router(reports.router, tags=(["Problemas"]), prefix="/reports")

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
