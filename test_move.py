from fastapi import FastAPI, Body
import shutil
import os

app = FastAPI()

@app.post("/test_move")
async def test_move(
    varFilePath: str = Body(...),
    varFileName: str = Body(...),
    varDestinationPath: str = Body(...)
):
    try:
        # Construct the full paths
        source = os.path.join(varFilePath, varFileName)
        destination = os.path.join(varDestinationPath, varFileName)
        
        # Move the file
        shutil.move(source, destination)
        
        return {"status": "success", "message": f"Moved {varFileName} to {varDestinationPath}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)