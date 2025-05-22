import pytest
from src.services.food_facility_service import FoodFacilityService

@pytest.fixture
def service():
    # Provide a FoodFacilityService instance for tests
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
def test_search_term():
    # Common search term for food facility tests
    return "datam"