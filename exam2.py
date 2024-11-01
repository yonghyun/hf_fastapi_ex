# 한국어 금융 감성 분석
# step1
from fastapi import FastAPI, Form
from transformers import pipeline
import uvicorn


# https://huggingface.co/ProsusAI/finbert?text=Stocks+rallied+and+the+British+pound+gained.
classifier = pipeline("sentiment-analysis", model="snunlp/KR-FinBert-SC", device=0)

app = FastAPI()


@app.post("/infer/")
async def infer(text: str = Form()):
    # step3
    # text = "3년 동안의 주식 투자로 20억 원의 수익을 창출하며 투자 수익률을 800%로 높일 수 있습니다"
    # text = "수익률 완전 대박"
    # text = "으악 완전 쪽박이네"


    # step4
    result = classifier(text)

    # step5
    # 0: 부정, 1: 긍정
    print(result)

    return result[0]

if __name__ == "__main__":
    uvicorn.run("exam2:app", port=8000, host="localhost", reload=True)