# LangServe
from fastapi import FastAPI
from langserve import add_routes
# Generators
from outline_generator import chain as outline_chain
from card_generator import chain as card_chain

app = FastAPI(
    title="CardApp",
    version="1.0",
    description="API server for CardApp's LangChain integration.",
)

add_routes(
    app,
    outline_chain,
    path="/new-outline",
)

add_routes(
    app,
    card_chain,
    path="/new-card",
)

@app.get("/test")
def test_route():
    return {"message": "Test route is working!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)