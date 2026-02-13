# JDE_Excel_Converter

A high-performance Python microservice designed to bridge JD Edwards Orchestrator with advanced Excel data processing.

## Overview
This service provides a REST API endpoint that accepts Excel files in Base64 format and returns standardized CSV data. This allows JDE to process modern `.xlsx` files without requiring local file system access or complex Java libraries within the AIS server.

## Architecture
1. **JDE Orchestration:** Reads a file from the network and converts it to Base64.
2. **REST Call:** Sends JSON payload to this service's `/convert` endpoint.
3. **Transformation:** Service uses `pandas` and `openpyxl` to parse Excel and generate CSV text.
4. **Return:** JDE receives the CSV string and writes the final output to the destination.



## Technical Stack
* **Language:** Python 3.11
* **Framework:** FastAPI
* **Libraries:** Pandas, Openpyxl, Uvicorn
* **Deployment:** Docker / Render / Cloud-ready

## API Usage
**Endpoint:** `POST /convert`

**Request Body:**
```json
{
  "file_data": "Base64_Encoded_String_Here",
  "filename": "data.xlsx"
}