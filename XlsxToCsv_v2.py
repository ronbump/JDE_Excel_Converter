from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import os

app = FastAPI()

# This defines the "Envelope" JDE will send
class ConversionRequest(BaseModel):
    varFilePath: str
    varFileName: str
    varDestinationPath: str
    varNewFileName: str
    varWorkSheet: str

@app.post("/convert_by_path")
async def convert_by_path(req: ConversionRequest):
    # 1. Build the full network paths
    # Uses raw strings to handle backslashes in Windows paths correctly
    source_path = os.path.join(req.varFilePath, req.varFileName)
    dest_path = os.path.join(req.varDestinationPath, req.varNewFileName)
    
    # 2. Check if the source actually exists before trying to read it
    if not os.path.exists(source_path):
        raise HTTPException(status_code=404, detail=f"Source file not found at: {source_path}")

    try:
        # 3. Read the Excel file from the network share
        # This requires 'openpyxl' (pip install openpyxl)
        df = pd.read_excel(source_path, sheet_name=req.varWorkSheet)
        
        # 4. Save as CSV to the destination network share
        df.to_csv(dest_path, index=False)
        
        return {
            "status": "SUCCESS",
            "source": source_path,
            "destination": dest_path,
            "rows_processed": len(df)
        }
    except Exception as e:
        # If anything fails (permissions, locked files, etc.), tell JDE why
        raise HTTPException(status_code=500, detail=f"Conversion Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # JDE Connection IP: 10.102.181.207
    # Use this in Orchestrator: http://10.102.181.207:8000/convert