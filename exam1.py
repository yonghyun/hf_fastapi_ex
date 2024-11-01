# ProsusAI/finbert : FinBERT는 금융 텍스트의 감정을 분석하기 위한 사전 훈련된 NLP 모델

# step1
from transformers import pipeline
from fastapi import FastAPI, Form
import uvicorn

# step2
classifier = pipeline("sentiment-analysis", model="ProsusAI/finbert")

app = FastAPI()

@app.post("/infer/")
async def infer(text: str = Form()):
    
    # step3
    # text = "Stocks rallied and the British pound gained."

    # step4
    result = classifier(text)

    # step5
    # 0: 부정, 1: 긍정
    print(result[0])
    return {"result": result[0]}

if __name__ == "__main__":
    uvicorn.run("exam1:app", port=8000, host="localhost", reload=True)