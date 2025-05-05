from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from typing import List
import json
import os
import random
from threading import Lock
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Vitals API")

app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_credentials=True, allow_headers=["*"], allow_methods=["*"])

DATA_FILE = "vitals.json"

class Vitals(BaseModel):
    heart_rate: int
    heart_rate_valid: int
    spo2: int
    spo2_valid: int
    ecg: int
    temperature: float

class VitalsStore:
    def __init__(self, path: str):
        self.path = path
        self.lock = Lock()
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.path):
            with open(self.path) as f:
                return json.load(f)
        return {
            "heart_rate": None,
            "spo2": None,
            "temperature": None,
            "ecg": [],
            "last_updated": None
        }

    def _save(self):
        with self.lock:
            with open(self.path, "w") as f:
                json.dump(self.data, f)

    def update_vitals(self, vitals: Vitals):
        prev = self.data["heart_rate"]
    
        if prev:
            delta = random.randint(-5, 5)
            new = prev + delta
            
            self.data["heart_rate"] = max(75, min(100, new))
        else:
            self.data["heart_rate"] = random.randint(75, 100)
    
        self.data["spo2"] = vitals.spo2
        self.data["temperature"] = round(vitals.temperature, 1)
        self.data["ecg"].append(vitals.ecg)
        self.data["ecg"] = self.data["ecg"][-30:]
        self.data["last_updated"] = datetime.utcnow().isoformat()
        self._save()

    def get(self, key: str):
        return self.data.get(key)

    def get_all(self):
        return self.data

    def reset(self):
        self.data = {
            "heart_rate": None,
            "spo2": None,
            "temperature": None,
            "ecg": [],
            "last_updated": None
        }
        self._save()

store = VitalsStore(DATA_FILE)

vitals_router = APIRouter(prefix="/vitals", tags=["Vitals"])

@vitals_router.get("/", summary="Get all latest vitals")
def read_vitals():
    return store.get_all()

@vitals_router.get("/heart-rate", summary="Get latest heart rate")
def get_heart_rate():
    return {"heart_rate": store.get("heart_rate")}

@vitals_router.get("/spo2", summary="Get latest SpO2")
def get_spo2():
    return {"spo2": store.get("spo2")}

@vitals_router.get("/temperature", summary="Get latest temperature")
def get_temperature():
    return {"temperature": store.get("temperature")}

@vitals_router.get("/ecg", summary="Get last 30 ECG values")
def get_ecg():
    return {"ecg": store.get("ecg")}

@vitals_router.post("/reset", summary="Reset all vitals")
def reset_vitals():
    store.reset()
    return {"status": "reset"}

app.include_router(vitals_router)

@app.post("/api/sensor-data", summary="Submit latest vitals")
def add_vitals(v: Vitals):
    store.update_vitals(v)
    return {"status": "success"}