from fastapi import FastAPI
import uvicorn
from v1.api import reg
from v1.routers import auth

app = FastAPI(title='Auth Server')
app.include_router(reg)
app.include_router(auth)

if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, host='0.0.0.0', reload=True)
