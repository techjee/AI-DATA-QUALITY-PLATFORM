from fastapi import FastAPI, UploadFile, File
import pandas as pd
import io


app = FastAPI()

@app.get("/")
def home():
    return {"message": "Backend is running!"}

@app.post("/upload")

async def upload_csv(file: UploadFile = File(...)):

    contents = await file.read()

    df = pd.read_csv(
        io.StringIO(contents.decode("utf-8"))
    )

    return {
        "filename": file.filename,
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns)
    }