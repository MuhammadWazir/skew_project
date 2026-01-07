from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.presentation.routers.knowledge_router import knowledge_router
from src.presentation.routers.chat_router import chat_router
from src.containers import Container


app = FastAPI(title="Chat & Knowledge Base System", version="1.0.0")

# Wire the dependencies
container = Container()
container.wire(packages=["src.presentation.routers"])

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(knowledge_router)
app.include_router(chat_router)

@app.get("/")
async def root():
	return {"message": "Chat & Knowledge Base System"}


if __name__ == "__main__":
	import uvicorn
	uvicorn.run(app, host="0.0.0.0", port=8000) 