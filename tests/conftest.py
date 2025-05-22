import pytest
from src.services.food_facility_service import FoodFacilityService

@pytest.fixture
def service():
    return FoodFacilityService()

@pytest.fixture
def sf_coordinates():
    # Return San Francisco coordinates
    return {"lng": -122.4194, "lat": 37.7749}

@pytest.fixture
def oakland_coordinates():
    # Return Oakland coordinates
    return {"lng": -122.2712, "lat": 37.8044}

@pytest.fixture
def valid_search_name_status():
    name = "datam"
    status = "APPROVED"
    return {"name": name, "status": status}

@pytest.fixture
def valid_street_name():
    street_name = "san"
    return street_name


@pytest.fixture
def invalid_search_name_status():
    name = "datam"
    status = "REQUIRED"
    return {"name": name, "status": status}

@pytest.fixture
def invalid_name():
    name = "nonexistentfacility"
    return name