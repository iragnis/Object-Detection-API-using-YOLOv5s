from fastapi import FastAPI, File
import preprocess as ym
from starlette.responses import Response
import io
from PIL import Image
import json
from fastapi.middleware.cors import CORSMiddleware

model = ym.get_yolov5()

app = FastAPI(
    title=" YOLOV5 Machine Learning API",
    description="""Obtain bounding box coordinates and class label""",
    version="0.0.1",
)
origins = [
    "http://localhost",
    "http://localhost:8000",
    "*"
]
app.add_middleware(
     CORSMiddleware,
     allow_origins=origins,
     allow_credentials=True,
     allow_methods=["*"],
     allow_headers=["*"],
)

@app.get('/notify/health')
def get_health():
    return dict(msg='OK')

@app.post("/object-to-json")
async def json_bounding_box(file: bytes = File(...)):
    input_image = ym.get_image_from_bytes(file)
    results = model(input_image)
    detect_res = results.pandas().xyxy[0].to_json(orient="records")
    detect_res = json.loads(detect_res)
    return {"result": detect_res}

@app.post("/object-to-img")
async def draw_bounding_box(file: bytes = File(...)):
    input_image = ym.get_image_from_bytes(file)
    results = model(input_image)
    results.render()  # updates results.imgs with boxes and labels
    for img in results.ims:
        bytes_io = io.BytesIO()
        img_base64 = Image.fromarray(img)
        img_base64.save(bytes_io, format="jpeg")
    return Response(content=bytes_io.getvalue(),media_type="image/jpeg")