from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse
from transformers import pipeline
from contextlib import asynccontextmanager

import uvicorn

ml_model = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    ml_model["summarizer"] = pipeline("summarization", "sshleifer/distilbart-cnn-12-6", device=0)
    yield
    # Clean up the ML models and release the resources
    ml_model.clear()

app = FastAPI(lifespan=lifespan)

@app.post("/summarize", response_model=str)
async def summary(file: UploadFile):
    content = await file.read()
    content = content.decode()
    content = content.replace('\r\n', ' ')
    
    # 최대 길이를 지정하고 텍스트를 자릅니다.
    max_length = 500
    content = content[:max_length]
    
    # 요약 수행
    result = ml_model["summarizer"](content)
    return f"요약된 내용 : {result[0]['summary_text']}"

@app.get("/")
async def main():
    content = """
      <body>
        <h2>요약하려는 텍스트 파일을 업로드하세요</h2>
        <hr>
        <form action="/summarize" enctype="multipart/form-data" method="post">
          <input name="file" type="file">
          <input type="submit">
        </form>       
      </body>
    """
    return HTMLResponse(content=content)

if __name__ == "__main__":
    uvicorn.run("exam8:app", port=8000, host="localhost", reload=True)
