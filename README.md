FastAPI backend for managing and storing vitals data.

## Setup and Run

### Prerequisites

* Python 3.11.12

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Adi8712/edp-backend.git
   cd edp-backend
   ```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Run the API

Start the FastAPI server:

```bash
fastapi dev main.py
```

The API will be available at `http://127.0.0.1:8000`.


## Endpoints

### 1. **Get All Latest Vitals**
- **Route**: `/vitals/`
- **Method**: `GET`
- **Request**: No request body required.
- **Response**:
  - **200 OK**: 
    ```json
    {
      "heart_rate": 88,
      "spo2": 95,
      "temperature": 36.7,
      "ecg": [100, 102, 104],
      "last_updated": "2025-05-05T12:00:00"
    }
    ```

### 2. **Get Latest Heart Rate**
- **Route**: `/vitals/heart-rate`
- **Method**: `GET`
- **Response**:
  - **200 OK**: 
    ```json
    {
      "heart_rate": 88
    }
    ```

### 3. **Get Latest SpO2**
- **Route**: `/vitals/spo2`
- **Method**: `GET`
- **Response**:
  - **200 OK**: 
    ```json
    {
      "spo2": 95
    }
    ```

### 4. **Get Latest Temperature**
- **Route**: `/vitals/temperature`
- **Method**: `GET`
- **Response**:
  - **200 OK**: 
    ```json
    {
      "temperature": 36.7
    }
    ```

### 5. **Get Last 30 ECG Values**
- **Route**: `/vitals/ecg`
- **Method**: `GET`
- **Response**:
  - **200 OK**: 
    ```json
    {
      "ecg": [100, 102, 104]
    }
    ```

### 6. **Reset All Vitals**
- **Route**: `/vitals/reset`
- **Method**: `POST`
- **Response**:
  - **200 OK**: 
    ```json
    {
      "status": "reset"
    }
    ```

### 7. **Submit Latest Vitals**
- **Route**: `/api/sensor-data`
- **Method**: `POST`
- **Request**: 
  ```json
  {
    "heart_rate": 90,
    "heart_rate_valid": 1,
    "spo2": 95,
    "spo2_valid": 1,
    "ecg": 102,
    "temperature": 36.5
  }
- **Response**:
    - **200 OK**: 
      ```json
      {
        "status": "success"
      }
      ```
