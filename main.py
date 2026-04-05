import io
import os
import asyncio
import nest_asyncio
import edge_tts
import torch
from groq import Groq
from transformers import AutoModelForCausalLM
from PIL import Image, UnidentifiedImageError
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from huggingface_hub import login
import uvicorn

try:
    from google.colab import userdata
    HF_TOKEN = userdata.get('HF_TOKEN')
    GROQ_API_KEY = userdata.get('GROQ_API_KEY')
except Exception:
    from dotenv import load_dotenv
    load_dotenv()
    HF_TOKEN = os.getenv('HF_TOKEN')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Apply nest_asyncio to allow nested event loops in colab
nest_asyncio.apply()

class Moondream2:
    def __init__(self):
        login(token=HF_TOKEN)
        self.model = AutoModelForCausalLM.from_pretrained(
            "vikhyatk/moondream2",
            revision="2025-01-09",
            trust_remote_code=True,
            device_map={"": "cuda"}
        )

    def __call__(self, image, question):
        result = self.model.query(
            image=image,
            question=question
        )
        return result["answer"]

class FoodStoryGenerator:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)

    def __call__(self, food_desc):
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{
                "role": "user",
                "content": f"""
                Dựa vào mô tả món ăn: "{food_desc}"
                Viết đoạn văn tiếng Việt hấp dẫn về:
                1. Lịch sử món ăn
                2. Đặc điểm nổi bật
                3. Cách thưởng thức
                """
            }]
        )
        return response.choices[0].message.content

class VietnameseTTS:
    def __init__(self, voice="vi-VN-HoaiMyNeural"):
        self.voice = voice

    async def _generate(self, text, output_path):
        communicate = edge_tts.Communicate(text=text, voice=self.voice)
        await communicate.save(output_path)

    def generate(self, text, output_path="output.mp3"):
        # Create a new event loop just for generation if running synchronously
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._generate(text, output_path))
        return output_path

    def __call__(self, text, output_path="output.mp3"):
        return self.generate(text, output_path)

# Initialize models
moondream = None
generator = None
tts = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading models...")
    global moondream, generator, tts
    moondream  = Moondream2()
    generator  = FoodStoryGenerator()
    tts        = VietnameseTTS()
    print("Models loaded successfully.")
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/')
async def root():
    return {
        "name": "Food Story API",
        "description": "Hệ thống API để nhận diện ảnh món ăn và generate story.",
        "endpoints": {
            "GET  /":        "Giới thiệu hệ thống",
            "GET  /health":  "Kiểm tra trạng thái",
            "POST /predict": "Nhận diện món ăn từ ảnh",
            "POST /generate":"Nhận diện + generate story + TTS",
            "GET  /audio":   "Trả về file audio"
        }
    }

@app.get('/health')
async def health():
    status = {}
    try:
        moondream.model
        status["moondream"] = "loaded"
    except:
        status["moondream"] = "error"

    try:
        generator.client.models.list()
        status["groq"] = "loaded"
    except:
        status["groq"] = "error"

    try:
        tts.voice
        status["tts"] = "loaded"
    except:
        status["tts"] = "error"

    status["gpu"] = f"{torch.cuda.get_device_name(0)} is ok" if torch.cuda.is_available() else "CPU ⚠️"

    return {
        "status": "OK" if all("loaded" in v for v in status.values()) else "degraded",
        "models": status
    }

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp", "image/jpg"]

@app.post('/predict')
async def predict(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail={"success": False, "message": f"File error: only {', '.join(ALLOWED_TYPES)}"})
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail={"success": False, "message": "File too large. Max 10MB."})
    try:
        image = Image.open(io.BytesIO(contents))
        image.verify()
        image = Image.open(io.BytesIO(contents))
    except Exception:
        raise HTTPException(status_code=400, detail={"success": False, "message": "Invalid image format."})
    
    try:
        food_desc = moondream(image=image, question="What food is this? Describe it briefly.")
    except Exception as e:
        raise HTTPException(status_code=500, detail={"success": False, "message": f"Error recognizing image: {str(e)}"})
    
    return {"food_description": food_desc}


@app.post('/generate')
async def generate(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail={"success": False, "message": f"File error: only {', '.join(ALLOWED_TYPES)}"})
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail={"success": False, "message": "File too large. Max 10MB."})
    try:
        image = Image.open(io.BytesIO(contents))
        image.verify()
        image = Image.open(io.BytesIO(contents))
    except Exception:
        raise HTTPException(status_code=400, detail={"success": False, "message": "Invalid image format."})

    try:
        food_desc = moondream(image=image, question="What food is this? Describe it briefly.")
    except Exception as e:
        raise HTTPException(status_code=500, detail={"success": False, "message": f"Error recognizing image: {str(e)}"})

    if not food_desc or not food_desc.strip():
        raise HTTPException(status_code=500, detail={"success": False, "message": "Could not recognize food."})

    try:
        story = generator(food_desc)
    except Exception as e:
        raise HTTPException(status_code=500, detail={"success": False, "message": f"Error generating story: {str(e)}"})

    try:
        audio_path = tts.generate(story)
    except Exception as e:
        raise HTTPException(status_code=500, detail={"success": False, "message": f"Error generating audio: {str(e)}"})

    return {
        "success": True,
        "data": {
            "food_description": food_desc,
            "story": story,
            "audio_url": "/audio"
        }
    }


@app.get('/audio')
async def get_audio():
    audio_path = "output.mp3"
    if not os.path.exists(audio_path):
        raise HTTPException(status_code=404, detail={"success": False, "message": "Audio file not found. Call /generate first."})
    return FileResponse(audio_path, media_type="audio/mpeg", filename="food_story.mp3")

if __name__ == "__main__":
    import sys
    import threading

    def start_pinggy():
        import subprocess
        import time
        time.sleep(2)  # Đợi uvicorn khởi động vài giây
        print("\n" + "="*50)
        print("🌐 ĐANG MỞ CỔNG PUBLIC (PINGGY) 🌐")
        print("Vui lòng chờ vài giây để lấy Link Public (đuôi .pinggy.link)")
        print("="*50 + "\n")
        subprocess.call(["ssh", "-p", "443", "-R0:localhost:8000", "-o", "StrictHostKeyChecking=no", "a.pinggy.io"])

    if "--share" in sys.argv:
        # Chạy pinggy ở một luồng độc lập (Background thread)
        threading.Thread(target=start_pinggy, daemon=True).start()

    uvicorn.run("main:app", host="0.0.0.0", port=8000, loop="asyncio")
