from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from deepface import DeepFace
import shutil
import os
import uuid
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 👈 Cho phép mọi domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
model = None

@app.on_event("startup")
def load_model_once():
    global model
    model = DeepFace.build_model("VGG-Face")  # Hoặc "Facenet", "ArcFace" tùy chọn
    print("✅ Model đã load xong")

@app.post("/compare")
async def compare(img1: UploadFile = File(...), img2: UploadFile = File(...)):
    try:
        # Tạo tên file tạm
        img1_path = f"temp/{uuid.uuid4()}.jpg"
        img2_path = f"temp/{uuid.uuid4()}.jpg"

        os.makedirs("temp", exist_ok=True)

        # Lưu file ảnh
        with open(img1_path, "wb") as f:
            shutil.copyfileobj(img1.file, f)
        with open(img2_path, "wb") as f:
            shutil.copyfileobj(img2.file, f)

        # Gọi DeepFace
        result = DeepFace.verify(img1_path, img2_path, enforce_detection=False, model_name="VGG-Face")
        distance = result.get("distance", None)
        if distance is None:
            distance = None
        else:
            similarity_percentage = round((1 - distance) * 100, 2)
        # Xoá file tạm
        os.remove(img1_path)
        os.remove(img2_path)
        result["similarity_percentage"] = similarity_percentage
        return JSONResponse(content=result)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
