from fastapi import FastAPI, HTTPException
from fastapi import Request
from fastapi.responses import FileResponse
from pathlib import Path
from db import (
    add_entry, delete_entry, get_all_entries, get_entry, update_entry
)


app = FastAPI()


@app.get('/api/entries')
def endpoint_get_all_entries():
    pass


@app.post('/api/entries')
async def endpoint_new_entry(request: Request):
    pass


@app.get('/api/entries/{entry_id}')
def endpoint_get_entry(entry_id: int):
    pass


@app.delete('/api/entries/{entry_id}')
def endpoint_delete_entry(entry_id: int):
    pass


@app.put('/api/entries/{entry_id}')
async def endpoint_update_entry(entry_id: int, request: Request):
    pass


# Route to handle requests for static assets
# this is a catch all so it should be registered last
@app.get('/{file_path}', response_class=FileResponse)
def get_static_file(file_path: str):
    if Path('static/' + file_path).is_file():
        return 'static/' + file_path
    raise HTTPException(status_code=404, detail='Item not found')
