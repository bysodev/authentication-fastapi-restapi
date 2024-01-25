from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import OAuth2PasswordBearer
from config import settings
from app.routers import lesson, section, user, challenge, category, difficulty, reach_challenge
from app.db.database import Base, engine
app = FastAPI()

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": str(exc.detail)},
    )

@app.get("/info")
def read_root():
    return {"app_name": settings.app_name, "app_description": settings.app_description}


origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost",
    "http://127.0.0.1",
    "*",
]

# GZip middleware
app.add_middleware(GZipMiddleware)

# HTTPS Redirect middleware
# app.add_middleware(HTTPSRedirectMiddleware)

# Trusted Host middleware
# app.add_middleware(TrustedHostMiddleware, allowed_hosts=origins)

# OAuth2 password bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        print('Creación de tablas exitosa')
    except Exception as e:
        print(f'Existe un Error: {e}')

create_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of origins allowed
    allow_credentials=True,  # Allow cookies to be sent with requests
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

routers = [user.router, challenge.router, reach_challenge.router, category.router, difficulty.router, lesson.router, section.router]
for router in routers:
    app.include_router(router)
