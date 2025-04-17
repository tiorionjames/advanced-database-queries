from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from db import get_all_entries, get_entry, add_entry

app = FastAPI()

# serve your HTML/JS from the 'static' folder
app.mount("/", StaticFiles(directory="static", html=True), name="static")


# ——— GET all entries ———
@app.get("/api/entries")
def endpoint_get_all_entries():
    return get_all_entries()


# ——— GET one entry by ID ———
@app.get("/api/entries/{entry_id}")
def endpoint_get_entry(entry_id: int):
    entry = get_entry(entry_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry


# ——— POST a new entry ———
@app.post("/api/entries")
async def endpoint_new_entry(request: Request):
    payload = await request.json()
    new_entry = add_entry(payload)
    return new_entry


# ——— leave these for Part II ———
@app.delete("/api/entries/{entry_id}")
def endpoint_delete_entry(entry_id: int):
    success = delete_entry(entry_id)
    if not success:
        raise HTTPException(status_code=404, detail="Entry not found")
    return {"success": True}


@app.put("/api/entries/{entry_id}")
async def endpoint_update_entry(entry_id: int, request: Request):
    payload = await request.json()
    updated = update_entry(entry_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Entry not found")
    return updated
