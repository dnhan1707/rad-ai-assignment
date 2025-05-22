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
        5) Access 'http://localhost:8080/docs' to try it out. (if that link does not work, try: 'http://0.0.0.0:8080/docs')

    + From terminal: 
        1) Navigate to the root of the project
        2) Run 'python3 -m venv venv' to create 'venv'
        3) Activate virtual environemt: 
            - Mac -> run 'source venv/bin/activate' 
            - Window -> run 'venv\Scripts\activate'  
        4) Download dependencies: 
            'pip install -r requirements-dev.txt' and 'pip install -r requirements.txt'
        5) Run 'uvicorn src.main:app --reload' 
        6) Access 'http://localhost:8080/docs' to try it out.

## Critique Section

1) **What would you have done differently if you had engaged in this more time?**

- **Backend**: I would have worked on a more dynamic search and filtering capability. In addition, I wanted to incorporate AI with MCP (Model Context Protocol) or a RAG (Retrieval-Augmented Generation) model, so users could ask more natural human questions on the dataset while it still produced quality, user-friendly responses. 

- **Frontend**: I was picturing a map-based version of Google Maps for finding mobile food facilities. The map would include a filtering sidebar and a chatbot to connect the MCP or RAG model to the user. The map would shift dynamically depending on the user's requests and needs.

2) **What trade-offs did you potentially consider?**

- **Dependency management**: The project uses 'requirements.txt' and 'requirements-dev.txt' files to manage dependencies. Other dependency management tools like Pipenv exist, but I chose to use the 'requirements.txt' and 'requirements-dev.txt' files because the number of total dependencies was small and I could control the dependencies as one developer. In this case, I saw an advantage to being less complicated and more transparent.

- **Haversine formula instead of Google Map API**: I used the Haversine formula to calculate the distance between two locations using the geographical latitude and longitude. While Google Maps has better features, a lot of them are not needed for this project. Using the Haversine formula saves some cost and keeps the application lightweight and focused on core functionality.

3) **What are the things I left out?**
- **User interface**: I did not develop a front end, but an excellent web UI, with a responsive and interactive map, would greatly improve the user experience.
- **Data persistence**: My application uses CSV files directly instead of using a proper database. Instead on properly designed production code, I would have selected PostgreSQL to be used with PostGIS for geospatial querying, which would allow much better performance on location-based searches.
- **Authentication & Authorisation**: The app does not have any user management, or more importantly, API authentication (such as JWT or OAuth2), which would be critical for the realistic world.

4. **What are the shortcomings of your implementations and how would you address them if we were required to scale the application for a large number of users?**  

- **Limited Functionality**: The current version does not include the standard CRUD operations (i.e. creating a record, updating a record, deleting a record) but only allows searching. 

- **No Route Protection**: There is no middleware, or CORS, for restricting access to the API. I intended to put this in place, but ran out of time and there were so many different edge cases making it difficult to consider.

- **Local Deployment**: The application is locally hosted and to scale for a larger audience I would deploy this system on AWS EC2. With EC2 you have the option to scale up with more CPU and RAM, and a t2.micro instance is sufficient for very small/first production. AWS supports horizontal scaling with Auto Scaling Groups to manage spikes in traffic effectively and efficiently. The need for the custom rate limiting function we were using between requests would no longer be needed and we could maintain a smooth and reliable performance.
