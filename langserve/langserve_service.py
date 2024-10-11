# langserve_service.py

# LangServe
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
# Generators
from outline_generator import chain as outline_chain
from card_generator import final_chain as card_chain

app = FastAPI(
    title="CardApp",
    version="1.0",
    description="API server for CardApp's LangChain integration.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# generates a course outline
add_routes(
    app,
    outline_chain,
    path="/outline/generator",
)

# generates cards based on a concept
add_routes(
    app,
    card_chain,
    path="/cards/generator",
)


@app.get("/test")
def test_route():
    return {"message": "Test route is working!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)