from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sqlite3
import requests
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import io

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- DATABASE ----------------
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
password TEXT
)
""")
conn.commit()

class User(BaseModel):
    username: str
    password: str

# ---------------- PAGE ROUTES ----------------
@app.get("/")
def home():
    return FileResponse("../index.html")

@app.get("/login")
def login_page():
    return FileResponse("../login.html")

@app.get("/signup")
def signup_page():
    return FileResponse("../signup.html")

@app.get("/dashboard")
def dashboard_page():
    return FileResponse("../dashboard.html")

@app.get("/detect-page")
def detect_page():
    return FileResponse("../detect.html")

@app.get("/market")
def market_page():
    return FileResponse("../market.html")

@app.get("/subsidy")
def subsidy_page():
    return FileResponse("../subsidy.html")

@app.get("/crop")
def crop_page():
    return FileResponse("../crop.html")

@app.get("/fertilizer")
def fertilizer_page():
    return FileResponse("../fertilizer.html")

@app.get("/pest")
def pest_page():
    return FileResponse("../pest.html")

@app.get("/chatbot")
def chatbot_page():
    return FileResponse("../chatbot.html")

@app.get("/help")
def help_page():
    return FileResponse("../help.html")

@app.get("/about")
def about_page():
    return FileResponse("../about.html")

# ---------------- LOGIN / SIGNUP ----------------
@app.post("/signup")
def signup(user: User):

    cursor.execute("INSERT INTO users (username,password) VALUES (?,?)",
                   (user.username, user.password))
    conn.commit()

    return {"message": "User registered successfully"}

@app.post("/login")
def login(user: User):

    cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
                   (user.username, user.password))

    result = cursor.fetchone()

    if result:
        return {"message": "Login successful"}
    else:
        return {"message": "Invalid username or password"}

import requests
from fastapi.responses import FileResponse

API_KEY="7526722f477c27caf02a79c99a733df8"


@app.get("/weather-page")
def weather_page():
    return FileResponse("weather.html")


@app.get("/weather/{city}")
def weather(city:str):

    url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={"7526722f477c27caf02a79c99a733df8"}&units=metric"

    res=requests.get(url).json()

    data={

    "current":{

    "temp":res["main"]["temp"],

    "condition":res["weather"][0]["main"],

    "humidity":res["main"]["humidity"],

    "wind":res["wind"]["speed"],

    "rain":0

    },

    "hourly":[

    {"time":"1 PM","temp":res["main"]["temp"]},
    {"time":"3 PM","temp":res["main"]["temp"]-1},
    {"time":"5 PM","temp":res["main"]["temp"]-2},
    {"time":"7 PM","temp":res["main"]["temp"]-3}

    ],

    "daily":[

    {"day":"Mon","temp":res["main"]["temp"]},
    {"day":"Tue","temp":res["main"]["temp"]-1},
    {"day":"Wed","temp":res["main"]["temp"]-2},
    {"day":"Thu","temp":res["main"]["temp"]-3},
    {"day":"Fri","temp":res["main"]["temp"]-4}

    ]

    }

    return data

# ---------------- AI MODEL ----------------
device = torch.device("cpu")

model = models.resnet18(pretrained=False)
model.fc = nn.Linear(model.fc.in_features, 6)
model.load_state_dict(torch.load("crop_model.pth", map_location=device))
model.eval()

transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor()
])

classes = [
"Potato Early Blight",
"Potato Healthy",
"Potato Late Blight",
"Tomato Early Blight",
"Tomato Late Blight",
"Tomato Leaf Mold"
]
disease_info = {

"Potato Early Blight":{
"description":"Early blight is a fungal disease caused by Alternaria solani which creates dark rings on leaves.",
"crop":"Potato",
"treatment":"Remove infected leaves and spray Mancozeb fungicide every 7 days."
},

"Potato Healthy":{
"description":"Leaf appears healthy and shows no disease symptoms.",
"crop":"Potato",
"treatment":"No treatment required."
},

"Potato Late Blight":{
"description":"Late blight spreads quickly in humid weather causing dark lesions.",
"crop":"Potato",
"treatment":"Apply Metalaxyl or Mancozeb fungicide."
},

"Tomato Early Blight":{
"description":"Early blight causes brown spots with rings on tomato leaves.",
"crop":"Tomato",
"treatment":"Remove infected leaves and spray Chlorothalonil fungicide."
},

"Tomato Late Blight":{
"description":"Late blight causes dark patches on tomato leaves.",
"crop":"Tomato",
"treatment":"Apply fungicides and maintain plant spacing."
},

"Tomato Leaf Mold":{
"description":"Leaf mold causes yellow spots and gray mold under leaves.",
"crop":"Tomato",
"treatment":"Improve air circulation and apply fungicide spray."
}

}

# ---------------- DISEASE DETECTION ----------------
@app.get("/detect")
def detect_page():
    return FileResponse("../detect.html")

@app.post("/detect")
async def detect_disease(file: UploadFile = File(...)):

    contents = await file.read()

    image = Image.open(io.BytesIO(contents)).convert("RGB")

    img = transform(image).unsqueeze(0)

    with torch.no_grad():

        outputs = model(img)

        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)

        confidence = torch.max(probabilities).item() * 100

        _, predicted = torch.max(outputs, 1)

    disease = classes[predicted.item()]

    info = disease_info[disease]

    return {
        "disease": disease,
        "confidence": round(confidence,2),
        "description": info["description"],
        "crop": info["crop"],
        "treatment": info["treatment"]
    }
# ---------------- FERTILIZER RECOMMENDATION ----------------

@app.post("/fertilizer-recommend")
def fertilizer_recommend(data: dict):

    soil = data.get("soil")
    temp = float(data.get("temperature"))
    rainfall = float(data.get("rainfall"))

    # Fertilizer logic
    if soil == "Sandy Soil":
        fertilizer = "Nitrogen rich fertilizer such as Urea is recommended."

    elif soil == "Clay Soil":
        fertilizer = "Phosphorus fertilizer such as DAP is recommended."

    elif soil == "Loamy Soil":
        fertilizer = "Balanced fertilizer such as NPK (10:10:10) is recommended."

    else:
        fertilizer = "Use organic compost or manure."

    # Weather advice
    if temp > 35:
        advice = "High temperature detected. Apply fertilizer in early morning or evening."

    elif rainfall > 200:
        advice = "Heavy rainfall expected. Avoid fertilizer application to prevent washout."

    else:
        advice = "Weather conditions are suitable for fertilizer application."

    return {
        "fertilizer": fertilizer,
        "advice": advice
    }
# ---------------- MARKET PRICE API ----------------

@app.get("/market-data/{crop}")
def get_market(crop: str):

    url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"

    params = {
        "api-key": "579b464db66ec23bdd0000012aa147b07e3e42b1775738d3585588d2",
        "format": "json",
        "limit": 1000
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return {"data": []}

    data = response.json()

    results = []
    states_seen = set()

    for item in data.get("records", []):

        commodity = item.get("commodity","")

        if crop.lower() in commodity.lower():

            state = item.get("state","N/A")

            # avoid repeating same state too many times
            if state not in states_seen:

                results.append({
                    "market": item.get("market","N/A"),
                    "state": state,
                    "price": item.get("modal_price","N/A")
                })

                states_seen.add(state)

        if len(results) >= 15:
            break

    return {"data": results}
