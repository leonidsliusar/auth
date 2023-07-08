from fastapi import FastAPI
import uvicorn
from v1.api import reg

app = FastAPI(title='Registration')
app.include_router(reg)

if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, host='0.0.0.0', reload=True)
