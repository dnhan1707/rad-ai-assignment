# RAD AI Assignment

## Problem

We are given a Mobile Food Facility CSV file containing 24 columns. However, we will focus only on the following columns:

- `Applicant`
- `Address`
- `Status`
- `Latitude`
- `Longitude`

Our goal is to find food facilities by:
- **Name** (with optional status)
- **Street name**
- **Nearest `k` facilities** given `latitude` and `longitude` coordinates

---

## Solution

### Architecture

The project is structured into the following layers:

- **API Routers Layer (`endpoints/`)**: Contains all route definitions.
- **Dataset Folder (`dataset/`)**: Contains the original CSV file.
- **Services (`services/`)**: Contains logic for CSV processing and search functionality.

---

### Workflow

#### CSV Processing Service (`csv_services.py`)
- Uses the `pandas` library to read the CSV file into a DataFrame (`df`), which is accessible throughout the application.

#### Food Facility Service (`food_facility_service.py`)
This service uses the DataFrame and provides methods to search for food facilities:

- **Search by Name**
  - **Parameters**: `name: str`, `status: Optional[str] = None`
  - Filters entries by name (case-sensitive), then by status if provided.
  - Returns results as:  
    ```json
    {"result": result.to_dict(orient="records")}
    ```

- **Search by Street Name**
  - **Parameter**: `street_name: str`
  - Case-insensitive match of the given name with the `Address` field.

- **Find K-Nearest Facilities**
  - **Parameters**: `lat: Optional[float]`, `lng: Optional[float]`, `k: int = 5`, `status: str = "APPROVED"`
  - Calculates Haversine distance between provided coordinates and facilities.
  - Filters by status, computes distances, sorts by nearest, and returns top `k` results.
  - If no coordinates are provided, returns all facilities with the given status.

#### Food Facility Endpoints (`food_facility.py`)
- **Rate Limiting**: Applies a limit of **10 requests per 5 seconds** per user.  
  Example error response:
  ```json
  {
    "detail": {
      "error": "Rate limit exceeded",
      "timeout": 1.22
    }
  }
  ```

- **Endpoints**:
  - `GET /food-facilities/`: Calls `search_by_name(name, status)`
  - `GET /food-facilities/by-street`: Calls `search_by_street_name(name)`
  - `GET /food-facilities/nearby`: Calls `find_k_nearest(lat, lng, limit, status)`

All endpoints are wrapped in `try-except` blocks to handle errors gracefully.

---

## Testing

### Unit Tests (`tests/unit_test/`)

- `test_food_facility_service.py`
  - Tests:
    - Haversine distance (same location = 0)
    - Known distance between cities (e.g., SF to Oakland)
    - Search by name with and without status
    - Search by street name
    - Find k-nearest functionality

### Integration Tests (`tests/integration_test/`)

- `test_food_facility_endpoint.py`
  - Tests:
    - Search by name with and without filters
    - Handling of empty results
    - Missing parameter errors
    - Street name search
    - Nearest facilities search
  - Uses FastAPI’s `TestClient` for testing routes without starting the server



- Steps run the application:
    + From Dockerfile:
        1) Navigate to the root of the project in the terminal
        2) Open your Docker Desktop
        3) Run 'docker build -t radaiassignment:latest .'
        4) Run 'docker run --name radassignment_run_1 -p 8080:8080 radaiassignment:latest'
        5) Access 'http://localhost:8080/docs' to try it out. (if that link does not work, try: 'http://0.0.0.0:8080')

    + From terminal: 
        1) navigate to the root of the project
        2) Run 'python3 -m venv venv' to create 'venv'
        3) Activate virtual environemt: 
            Mac -> run 'source venv/bin/activate' 
            Window -> run 'venv\Scripts\activate'  
        4) Download dependencies: 
            'pip install -r requirements-dev.txt' and 'pip install -r requirements.txt'
        5) Run 'uvicorn src.main:app --reload' 
        6) Access 'http://localhost:8080/docs' to try it out.

## Critique Section

1) **What would you have done differently if you had spent more time on this?**

- **Backend**: I plan to have more dynamic searching, filtering functionalities. I also want to implement AI by MCP (Model Context Protocol) or building a RAG model, this allow user to ask more human-like question about the dataset and still ensure the high-quality human-friendly response.

- **Frontend**: I would like to build a map-based website that works like a Google Map for Location of Mobile Food Facility, there  
will be a filtering side bar and a chatbot to talk with MCP or RAG model. The map will be updated based on users need.

2) **What are the trade-offs you might have made?**

- **Dependencies management**: the application has  'requirements-dev.txt' and 'requirements.txt' from where user have to download dependencies. Another common way is using 'Pipenv' as the dependency manager, however, because of the small amount of packages and I can have full control over those packages, I decide to use the 'requirements.txt' file way.

- **Haversine formula instead of Google Map API**: I decided implement this function to calculate the distance between 2 locations with give longtitude and latitude because it is all we need, Google Map provide many others services that does not align much with the project, therefore, to save the cost and keep the simplicity I believe using Haversine function is the best way.

3) **What are the things you left out?**

- Things that I left out including building UI and backend hosting, currently the application ask user to access the API through FastAPI on localhost.

4) **What are the problems with your implementation and how would you solve them if we had to scale the application to a large number of users?**  

- There is a major limitation with the current application, it only allow searching but not other CRUD such as creating, updating, deleting. 

- Also there are not routes protection such as using Middleware or CORS to limit the API access, this is on purpose because of the inconsistency and complexity. 

- Everything is currently on Local, we can improve this by hosting FastAPI based project on AWS EC2. This also allow the application to habdle larger number of users because it provides more RAM, CPU, and using t2.micro system normally is good enough for scalable project, its horizontal scaling is also extremely good thanks to their Auto Scaling Group handling traffic spikes. Using AWS service allow us to remove the 'rate limit function' in the app and still ensure the smooth response from backend.
