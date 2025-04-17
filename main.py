from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from pathlib import Path
from db import add_entry, delete_entry, get_all_entries, get_entry, update_entry

app = FastAPI()


@app.get("/api/entries")
def endpoint_get_all_entries():
    return get_all_entries()


@app.post("/api/entries")
async def endpoint_new_entry(request: Request):
    try:
        payload = await request.json()
    except ValueError:
        raise HTTPException(
            status_code=404, detail="This is not the droid you are looking for"
        )
    return add_entry(payload)


@app.get("/api/entries/{entry_id}")
def endpoint_get_entry(entry_id: int):
    entry = get_entry(entry_id)
    if entry is None:
        raise HTTPException(
            status_code=404, detail="This is also not the droid you are looking for"
        )
    return entry


@app.delete("/api/entries/{entry_id}")
def endpoint_delete_entry(entry_id: int):
    success = delete_entry(entry_id)
    if not success:
        raise HTTPException(status_code=404, detail="Go away, not found")
    return {"success": True}


@app.put("/api/entries/{entry_id}")
async def endpoint_update_entry(entry_id: int, request: Request):
    try:
        payload = await request.json()
    except ValueError:
        raise HTTPException(status_code=400, detail="Not valid, try again Padawan")
    updated = update_entry(entry_id, payload)
    if updated is None:
        raise HTTPException(status_code=404, detail="Nope.  You broked me")
    return updated


# catch-all for static files
@app.get("/{file_path}", response_class=FileResponse)
def get_static_file(file_path: str):
    static_path = Path("static") / file_path
    if static_path.is_file():
        return str(static_path)
    raise HTTPException(status_code=404, detail="What are you trying to do? ")
