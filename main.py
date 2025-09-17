# api.py
from typing import List, Optional
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, HttpUrl
from starlette.concurrency import run_in_threadpool

# ⬇️ import your function (update the module path to where you keep it)
from app.vehicle_finder_ikman import get_vehicle_details  # e.g., put your code in scraper.py

app = FastAPI(title="Ikman Vehicle Scraper API", version="1.0.0")


class AdItem(BaseModel):
    title: str
    link: HttpUrl
    image: Optional[HttpUrl] = None
    mileage: str
    location_category: str
    price: str
    updated: str


@app.get("/vehicles", response_model=List[AdItem])
async def vehicles(q: str = Query(..., min_length=1, description="Search term, e.g. 'Alto'")):
    """
    Proxy endpoint that scrapes Ikman listings using your existing function.
    """
    try:
        # offload the blocking requests/bs4 work to a thread so it doesn't block the event loop
        ads = await run_in_threadpool(get_vehicle_details, q)
        return ads
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Scrape failed: {e.__class__.__name__}: {e}")
