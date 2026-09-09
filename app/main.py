# from fastapi import FastAPI
# from app.api.routes import router

# app = FastAPI(title="ShopEase AI Customer Support")

# app.include_router(router)

# app/main.py


from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="ShopEase AI Customer Support")

app.include_router(router)