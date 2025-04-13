import uvicorn

from app.application import create_app
from app.core.config import settings

app = create_app()

if __name__ == '__main__':
    uvicorn.run(app, host=settings.SERVICE_LOCAL_HOST, port=settings.SERVICE_LOCAL_PORT)
