from fastapi import FastAPI, Body
import pandas as pd
import base64
import io

app = FastAPI()

@app.post("/convert")
async def convert_excel_to_csv(data: dict = Body(...)):
    # 1. Get the base64 string from the JDE request
    encoded_file = data.get("file_data")
    
    if not encoded_file:
        return {"status": "error", "message": "No file data received"}

    try:
        # 2. Decode base64 to bytes and read into Pandas
        decoded_bytes = base64.b64decode(encoded_file)
        df = pd.read_excel(io.BytesIO(decoded_bytes))
        
        # 3. Convert to CSV string
        csv_output = df.to_csv(index=False)
        
        return {
            "status": "success",
            "csv_content": csv_output
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    # Use 9225 since we know that port is behaving
    uvicorn.run(app, host="0.0.0.0", port=9225)