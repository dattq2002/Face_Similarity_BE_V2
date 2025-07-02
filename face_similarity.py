import os
import warnings
# Tắt TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
warnings.filterwarnings("ignore", category=DeprecationWarning)

import os
import warnings
# Tắt TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
warnings.filterwarnings("ignore", category=DeprecationWarning)

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from deepface import DeepFace
import uuid
import numpy as np
import cv2
import traceback
from typing import Dict, Any

app = FastAPI(title="Face Similarity API", description="API for comparing face similarity using DeepFace")

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong production nên chỉ định cụ thể domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Hàm chuyển file ảnh từ UploadFile thành ảnh OpenCV (không lưu vào đĩa)
async def read_image(file: UploadFile) -> np.ndarray:
    """Đọc ảnh từ UploadFile và chuyển thành numpy array cho OpenCV"""
    contents = await file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

@app.get("/")
async def root() -> Dict[str, str]:
    """Endpoint chào mừng"""
    return {"message": "Welcome to the Face Similarity API! Use POST /compare with img1 & img2."}

@app.post("/compare")
async def compare_faces(
    img1: UploadFile = File(..., description="First image file"),
    img2: UploadFile = File(..., description="Second image file")
) -> Dict[str, Any]:
    """
    So sánh độ tương đồng giữa hai khuôn mặt
    
    Args:
        img1: File ảnh đầu tiên
        img2: File ảnh thứ hai
        
    Returns:
        Dict chứa kết quả so sánh và tỷ lệ phần trăm tương đồng
    """
    try:
        # Kiểm tra định dạng file
        allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/bmp"]
        if img1.content_type not in allowed_types or img2.content_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail="Only image files (JPEG, PNG, BMP) are allowed"
            )

        # Tạo thư mục temp nếu chưa có
        os.makedirs("temp", exist_ok=True)
        
        # Tạo tên file tạm với UUID
        img1_path = f"temp/{uuid.uuid4()}.jpg"
        img2_path = f"temp/{uuid.uuid4()}.jpg"

        try:
            # Lưu file tạm
            with open(img1_path, "wb") as f:
                f.write(await img1.read())
            
            with open(img2_path, "wb") as f:
                f.write(await img2.read())

            # Gọi DeepFace để so sánh
            result = DeepFace.verify(
                img1_path, 
                img2_path, 
                enforce_detection=False, 
                model_name="VGG-Face"
            )
            
            # Tính toán tỷ lệ phần trăm tương đồng
            distance = result.get("distance", None)
            similarity_percentage = None
            if distance is not None:
                similarity_percentage = round((1 - distance) * 100, 2)

            # Thêm similarity_percentage vào kết quả
            result["similarity_percentage"] = similarity_percentage

            return result

        finally:
            # Đảm bảo xóa file tạm trong mọi trường hợp
            for path in [img1_path, img2_path]:
                if os.path.exists(path):
                    os.remove(path)

    except HTTPException:
        raise
    except Exception as e:
        # Trả về lỗi chi tiết cho debugging
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        )

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,  # Truyền trực tiếp app object thay vì string
        host="0.0.0.0",
        port=5000,
        reload=False,  # Tự động reload khi có thay đổi code (chỉ dùng trong development)
        log_level="info"
    )