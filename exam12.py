from typing import Dict, Annotated
from fastapi import FastAPI, Form
from transformers import pipeline
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse
import uvicorn

classifier = None
@asynccontextmanager
async def startup(app: FastAPI):
  global classifier 
  classifier = pipeline("sentiment-analysis", device=0)
  print(classifier)
  yield

app = FastAPI(lifespan=startup)

@app.post("/predict", response_model = Dict)
# 변수: Annotated[기본타입, 메타데이터]
# 기본 타입에 추가 정보를 덧붙여 데이터 유효성 검사나 API 요청 처리를 돕는 데 사용
def predict(content: Annotated[str, Form()]):
  result = classifier(content)
  print(result[0])
  return result[0]

@app.get("/")
async def main():
  content = """
      <!DOCTYPE html> 
      <html>
        <head>
        <meta charset="UTF-8">
        <title>FastAPI+HuggingFace</title>
      </head>
      <body>
        <h1>허깅페이스 모델을 활용한 sentiment-analysis 테스트</h1><hr>
        <form action="/predict" method="post">
        <input name="content" type="text" size="50" placeholder="분석을 원하는 글을 입력하세요"><br>
        <input type="submit" value="요청">
        </form>
      </body>
    """
  return HTMLResponse(content=content)

if __name__ == "__main__":
  uvicorn.run("exam12:app", port=8000, host="localhost", reload=True)