# 문장 요약(영문, 한글)
# step1
from transformers import pipeline
from fastapi import FastAPI, Form
import uvicorn


# step2
summarizer = pipeline("summarization", model = "stevhliu/my_awesome_billsum_model", device=0)
summarizer_kr = pipeline("summarization", model="psyche/KoT5-summarization", device=0)

app = FastAPI()


@app.post("/infer/")
async def infer(text: str = Form(), kor_text: str = Form()):
    
    # step3
    # text = "Opens and identifies the given image file."
    # kor_text = "네이버와 함께 아름다운 한글간판을 나눕니다. 한글의 의미를 되새기고, 그 아름다움을 널리 전하고자 서울부터 제주까지 전국 20개 상점과 네이버가 한글간판을"

    # step4
    result = summarizer(text)
    kor_result = summarizer_kr(kor_text)

    return {"result": result, "result2": kor_result}

if __name__ == "__main__":
    uvicorn.run("exam3:app", port=8000, host="localhost", reload=True)