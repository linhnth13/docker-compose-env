import asyncio
import os
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text

DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']
DB_NAME = os.environ['DB_NAME']
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL, echo=True)

async def get_session():
    async with AsyncSession(engine) as session:
        yield session

app = FastAPI()

@app.get("/health")
async def health(session: AsyncSession = Depends(get_session)):
    print("🔍 Starting DB health check...")
    try:
        await asyncio.wait_for(session.execute(text("SELECT 1")), timeout=1.0)
        db_status = "connected"
    except asyncio.TimeoutError:
        db_status = "timeout"
        print("⏱️ DB connection TIMEOUT after 1 second.")
    except Exception as e:
        db_status = "disconnected"
        print(f"❌ DB connection FAILED: {e}")
    return {"status": "ok", "database": db_status}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Cloud Run sets PORT
    uvicorn.run(app, host="0.0.0.0", port=port)