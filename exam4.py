# 단일파일 업로드
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

@app.post("/singlefile")
async def create_file(file: bytes = File()):
  return {"file_size": len(file)}

@app.post("/singleuploadfile")
async def create_upload_file(file: UploadFile):
  return {"filename": file.filename}

@app.get("/")
async def main():
  content = """
      <body>
      <body>
      <h2>단일 파일 업로드</h2>
      <hr>
      <form action="/singlefile" enctype="multipart/form-data" method="post">
      <input name="file" type="file">
      <input type="submit">
      </form>
      <hr>
      <form action="/singleuploadfile" enctype="multipart/form-data" method="post">
      <input name="file" type="file">
      <input type="submit">
      </form>
      </body>
    """
  return HTMLResponse(content=content)

if __name__ == "__main__":
    uvicorn.run("exam4:app", port=8000, host="localhost", reload=True)