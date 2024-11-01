from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from transformers import pipeline
from contextlib import asynccontextmanager
from PIL import Image
from io import BytesIO

import uvicorn

ml_model = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
	# Load the ML model
	ml_model["imagetotext"] = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large", device=0)     
	yield
	# Clean up the ML models and release the resources
	ml_model.clear()


app = FastAPI(lifespan=lifespan)

@app.post("/imagetotext", response_model = str)
async def imagetotext(file: UploadFile):
	content = await file.read()
	img_content = Image.open(BytesIO(content))
	result = ml_model["imagetotext"](img_content)
	return f"이미지에 대한 설명글 : {result[0]['generated_text']}"

@app.get("/")
async def main():
  content = """
      <body>
        <h2>이미지에 대한 설명글을 작성하려는 이미지 파일을 업로드하세요</h2>
        <hr>
        <form action="/imagetotext" enctype="multipart/form-data" method="post">
        <input name="file" type="file">
        <input type="submit">
        </form>       
      </body>
    """
  return HTMLResponse(content=content)

if __name__ == "__main__":
  uvicorn.run("exam9:app", port=8000, host="localhost", reload=True)