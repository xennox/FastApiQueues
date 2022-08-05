import uvicorn
import asyncio
from datetime import datetime
from fastapi import FastAPI, status
from fastapi_utils.tasks import repeat_every


app = FastAPI(title='WorkerAPI')

NumData = []
WorksData = []


@app.on_event("startup")
@repeat_every(seconds=10)
async def createfromworker() -> None:
    for a in WorksData:
        NumData.append(a['Num'])


@app.get('/getnums', status_code=200, tags=['NUMS'])
async def show():
    return NumData


@app.get('/gettask', status_code=200, tags=['NUMS'])
async def show():
    return WorksData


#@app.post('/makenum', status_code=status.HTTP_201_CREATED, tags=['NUMS'])
#async def create():
#    for a in WorksData:
#        NumData.append(a['Num'])
#        WorksData.pop(0)
#    return NumData


@app.post('/makework', status_code=status.HTTP_201_CREATED, tags=['WORKS'])
async def create(num: int, timeout: int):
    historynum = len(WorksData) + 1
    createdtime = datetime.now()
    alldata = {'HistoryNum': historynum, 'CreatedTime': str(createdtime), 'Num': num, 'TimeOut': timeout}
    await asyncio.sleep(timeout)
    WorksData.append(alldata)

    if historynum > 20:
        WorksData.pop(0)
    return WorksData


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
