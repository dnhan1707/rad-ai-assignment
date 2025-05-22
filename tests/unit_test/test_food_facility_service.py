import pytest

def test_same_location_returns_zero(service, sf_coordinates):
    lng_1 = sf_coordinates["lng"]
    lat_1 = sf_coordinates["lat"]
    lng_2 = sf_coordinates["lng"]
    lat_2 = sf_coordinates["lat"]

    distance = service.haversine_distance_formula(lng_1, lat_1, lng_2, lat_2)
    assert distance == 0

def test_known_distance(service, sf_coordinates, oakland_coordinates):
    # SF to Oakland is around 12km
    distance = service.haversine_distance_formula(
        sf_coordinates["lng"], sf_coordinates["lat"],
        oakland_coordinates["lng"], oakland_coordinates["lat"]
    )
    assert abs(distance - 12.0) < 2.0

@pytest.mark.asyncio
async def test_search_by_known_name(service, test_search_term):
    response = await service.search_by_name(test_search_term)
    
    assert "result" in response, "Response missing 'result' key"
    assert len(response["result"]) > 0, f"No results found for '{test_search_term}'"
    
    first_result = response["result"][0]
    first_result_applicant = first_result["Applicant"]
    
    # Check if search term is contained within the result (case-insensitive)
    assert test_search_term.lower() in first_result_applicant.lower()

@pytest.mark.asyncio
async def test_search_fail_by_status(service, test_search_term):
    status = "REQUESTED"
    response = await service.search_by_name(test_search_term, status)
    
    assert len(response["result"]) == 0, f"No results found for '{test_search_term}' with status '{status}'"

@pytest.mark.asyncio
async def test_search_streetname(service):
    street_name = "cali"
    response = await service.search_by_street_name(street_name)
    
    assert len(response["result"]) > 0

@pytest.mark.asyncio
async def test_find_k_nearest(service, sf_coordinates):
    response = await service.find_k_nearest(
        sf_coordinates["lat"], 
        sf_coordinates["lng"], 
        4
    )
    
    assert len(response["result"]) == 4