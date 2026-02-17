from fastapi import FastAPI, Body, Header, HTTPException
import pandas as pd
import base64
import io

app = FastAPI()

# 1. Define your secret key
SAFE_KEY = "MyPrivateJDEKey2026"

@app.post("/convert")
async def convert_excel_to_csv(
    # This looks for a header named 'X-API-KEY'
    x_api_key: str = Header(None), 
    data: dict = Body(...)
):
    # 2. Security Check: Validate the key before doing any work
    if x_api_key != SAFE_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized: Invalid API Key")

    # --- Your existing logic ---
    encoded_file = data.get("file_data")
    if not encoded_file:
        return {"status": "error", "message": "No file data received"}

    try:
        decoded_bytes = base64.b64decode(encoded_file)
        df = pd.read_excel(io.BytesIO(decoded_bytes))
        csv_output = df.to_csv(index=False)
        
        return {
            "status": "success",
            "csv_content": csv_output
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9225)