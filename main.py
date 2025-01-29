from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, StreamingResponse
import os
import string

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    html_content = open("index.html").read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/download")
async def download():
    data_size = 100 * 1024 * 1024  # 100 MB
    chunk_size = 1024 * 1024  # 1 MB chunks

    async def generate_data():
        remaining = data_size
        while remaining > 0:
            chunk = os.urandom(min(chunk_size, remaining))
            remaining -= len(chunk)
            yield chunk

    return StreamingResponse(content=generate_data(), media_type="application/octet-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)