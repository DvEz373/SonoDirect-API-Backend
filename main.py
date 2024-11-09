# uvicorn main:app --host <ip-address> --port 8000

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
import random
import firebase_admin
from firebase_admin import credentials, db
import uvicorn

# Use your downloaded service account JSON file
cred = credentials.Certificate(r"C:\Users\Acer\Documents\Flutter\sonodirect_dashboard\lib\server_plot_backend\service-account.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://esp32-d7997-default-rtdb.asia-southeast1.firebasedatabase.app'
})

app = FastAPI()

# Add CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (use specific origins in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to generate random data for multiple devices
def generate_random_data(length: int) -> Dict[str, List[float]]:
    return {f"Device_{i+1}": [round(random.uniform(-50, 50), 2) for _ in range(length)] for i in range(4)}

# Function to generate degree recommendation and sound score
def generate_recommendation():
    degree = random.randint(-90, 90)  # Random degree between -90 and 90
    sound_score = random.randint(0, 100)  # Random sound score between 0 and 100
    return {"degree": degree, "score": sound_score}

# Function to generate a 15x11 heatmap matrix
def generate_heatmap_matrix() -> List[List[float]]:
    return [[round(random.uniform(0, 1), 2) for _ in range(15)] for _ in range(11)]

@app.get("/get_spl_data")
async def get_spl_data():
    return {
        "type": "SPL",
        "data": generate_random_data(20)
    }

@app.get("/get_fft_data")
async def get_fft_data():
    return {
        "type": "FFT",
        "data": generate_random_data(20)
    }

@app.get("/get_thd_data")
async def get_thd_data():
    return {
        "type": "THD",
        "data": generate_random_data(20)
    }

@app.get("/get_snr_data")
async def get_snr_data():
    return {
        "type": "SNR",
        "data": generate_random_data(20)
    }

# Endpoint for degree recommendation
@app.get("/recommendation")
async def get_recommendation():
    return generate_recommendation()

# Endpoint for the heatmap data
@app.get("/heatmap")
async def get_heatmap():
    return {"heatmap": generate_heatmap_matrix()}

@app.get("/fetch-sound-metrics")
async def fetch_sound_metrics():
    try:
        ref = db.reference("test")
        sound_data = ref.get()
        return {"status": "success", "data": sound_data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
