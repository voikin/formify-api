from fastapi import FastAPI

app = FastAPI()


@app.get('/ping', tags=['test'])
async def ping():
    return {'message': 'pong'}
