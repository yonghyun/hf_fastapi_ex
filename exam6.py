# 비동기 실행 
from typing import List
from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
import os
import signal
import uvicorn

# FastAPI에서 애플리케이션의 생명주기 동안 특정 작업을 비동기 방식으로 수행
# yield 전 부분은 앱이 시작될 때 실행되고, yield 이후 부분은 서버가 종료될 때 실행
@asynccontextmanager
async def my_lifespan(app: FastAPI):
    print("서버 기동시 실행")
    if not os.path.isdir("static/files"):
      os.mkdir("static/files")
      # yield 키워드 전은 서버 실행 전에 수행
    yield
      # yield 키워드 후는 서버 실행 후에 수행

app = FastAPI(lifespan=my_lifespan) 

@app.get("/kill") 
async def lll() :
  os.kill(os.getpid(), signal.SIGTERM)  # 요청이되면 서비스 프로세스를 죽임


@app.post("/singleuploadfile")
async def create_upload_file(file: UploadFile):
  path = f"static/files/{file.filename}"
  content = await file.read()   # file read 비동기 처리, 파일을 읽는 동안 다른 요청을 동시에 처리할 수 있음
  with open(path, 'w+b') as fp:
    fp.write(content)

  return {
      'file': file.filename,
      'content': file.content_type, 
      'path': path,
  }




@app.post("/uploadfiles")
async def create_upload_files(files: List[UploadFile]):
  result = []
  for file in files:
    path = f"static/files/{file.filename}"
    content = await file.read()
    with open(path, 'w+b') as fp:
      fp.write(content) 

    result.append({
      'file': file.filename,
      'content': file.content_type,
      'path': path,
    })
  return result


@app.get("/")
async def main():
  content = """
      <body>
        <h2>파일 업로드하여 서버에 저장하기</h2>
        <hr>
        <form action="/singleuploadfile" enctype="multipart/form-data" method="post">
        <input name="file" type="file">
        <input type="submit" value="싱글파일 업로드">
        </form>
        <hr>
        <form action="/uploadfiles" enctype="multipart/form-data" method="post">
        <input name="files" type="file" multiple>
        <input type="submit" value="다중파일 업로드">
        </form>
      </body>
    """
  return HTMLResponse(content=content)
if __name__ == "__main__":
    uvicorn.run("exam6:app", port=8000, host="localhost", reload=True)