import uvicorn
from fastapi import FastAPI
from routers import messages, reports
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes
app.include_router(messages.router, tags=(["Mensagens"]), prefix="/messages")
app.include_router(reports.router, tags=(["Problemas"]), prefix="/reports")

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
