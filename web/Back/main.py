from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, WebSocket
from ml import correctImage, findfigureImage
from PIL import Image
from io import BytesIO
import uvicorn
import torch
import base64

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = torch.hub.load('ultralytics/yolov5', 'custom', path='./weights/best.pt', force_reload=False)
model.conf = 0.5

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            img = correctImage(data)
            correctImg = findfigureImage(img, model)

            bytes_io = BytesIO()
            for img in correctImg.ims:
                bytes_io = BytesIO()
                img_base64 = Image.fromarray(img)
                img_base64.save(bytes_io, format="jpeg")

            await websocket.send_bytes(base64.b64encode(bytes_io.getvalue()).decode('utf-8'))
    except Exception as e:
        print(e)
    finally:
        await websocket.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)

        
