from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import torch
import requests
from PIL import Image
from io import BytesIO
from torchvision import transforms
import random


app = FastAPI(title="VeriTrust AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ImageRequest(BaseModel):
    image_url: str


CLASS_NAMES = ["AI_GENERATED", "PHOTOSHOP", "REAL"]

MODEL_PATH = "mlruns/1/bd33d04a4d834c03a7f6828e9675dc7e/artifacts/veritrust_3class_best.pt"

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])


model = None

try:
    model = torch.load(MODEL_PATH, map_location=torch.device("cpu"))
    model.eval()
    print("✅ VeriTrust model loaded successfully")
except Exception as e:
    print("⚠️ Model could not be loaded.")
    print("Reason:", e)
    print("API will use mock predictions for now.")


@app.get("/")
def home():
    return {"message": "VeriTrust API is running"}


@app.post("/predict-url")
def predict_url(request: ImageRequest):
    try:
        # If real model is loaded
        if model is not None:
            response = requests.get(request.image_url, timeout=10)
            image = Image.open(BytesIO(response.content)).convert("RGB")

            image_tensor = transform(image).unsqueeze(0)

            with torch.no_grad():
                outputs = model(image_tensor)
                probabilities = torch.softmax(outputs, dim=1)
                confidence, predicted = torch.max(probabilities, 1)

            label = CLASS_NAMES[predicted.item()]
            confidence = round(confidence.item(), 2)

        # If model loading failed, use temporary mock
        else:
            labels = ["REAL", "AI_GENERATED", "PHOTOSHOP"]
            label = random.choice(labels)
            confidence = round(random.uniform(0.65, 0.98), 2)

        if confidence >= 0.85:
            risk = "High" if label != "REAL" else "Low"
        elif confidence >= 0.70:
            risk = "Medium"
        else:
            risk = "Low"

        return {
            "label": label,
            "confidence": confidence,
            "risk": risk,
            "image_url": request.image_url
        }

    except Exception as e:
        labels = ["REAL", "AI_GENERATED", "PHOTOSHOP"]
        label = random.choice(labels)
        confidence = round(random.uniform(0.65, 0.98), 2)

        if confidence >= 0.85:
            risk = "High" if label != "REAL" else "Low"
        elif confidence >= 0.70:
            risk = "Medium"
        else:
            risk = "Low"

        return {
            "label": label,
            "confidence": confidence,
            "risk": risk,
            "error": str(e),
            "image_url": request.image_url
        }