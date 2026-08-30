from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import os

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS disasters (
            id SERIAL PRIMARY KEY,
            name TEXT,
            type TEXT,
            lat REAL,
            lng REAL
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

init_db()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class Disaster(BaseModel):
    name: str
    type: str
    lat: float
    lng: float

@app.get("/")
def read_root():
    return {"message": "Disaster Management API is running!"}

@app.get("/disasters")
def get_disasters():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, type, lat, lng FROM disasters")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows # RealDictCursor already returns list of dicts

safe_zones = [
    {"id": 1, "name": "City Stadium Shelter", "lat": 17.4239, "lng": 78.4738},
    {"id": 2, "name": "Community Hall", "lat": 17.4483, "lng": 78.3915},
    {"id": 3, "name": "Open Ground - Park", "lat": 17.3850, "lng": 78.4867},
]

@app.get("/nearest-safe-zone")
def nearest_safe_zone(lat: float, lng: float):
    nearest = None
    min_dist = None
    for zone in safe_zones:
        dist = ((zone["lat"] - lat) ** 2 + (zone["lng"] - lng) ** 2) ** 0.5
        if min_dist is None or dist < min_dist:
            min_dist = dist
            nearest = zone
    return nearest

@app.post("/disasters")
def add_disaster(disaster: Disaster):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO disasters (name, type, lat, lng) VALUES (%s, %s, %s, %s)",
        (disaster.name, disaster.type, disaster.lat, disaster.lng)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Disaster added", "data": disaster}

@app.put("/disasters/{disaster_id}")
def update_disaster(disaster_id: int, disaster: Disaster):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE disasters SET name=%s, type=%s, lat=%s, lng=%s WHERE id=%s",
        (disaster.name, disaster.type, disaster.lat, disaster.lng, disaster_id)
    )
    conn.commit()
    updated = cursor.rowcount
    cursor.close()
    conn.close()
    if updated == 0:
        raise HTTPException(status_code=404, detail="Disaster not found")
    return {"message": "Disaster updated"}

@app.delete("/disasters/{disaster_id}")
def delete_disaster(disaster_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM disasters WHERE id=%s", (disaster_id,))
    conn.commit()
    deleted = cursor.rowcount
    cursor.close()
    conn.close()
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Disaster not found")
    return {"message": "Disaster deleted"}