def test_search_by_name_success(testing_app, valid_search_name_status):
    response = testing_app.get(
        f'/food-facilities/?name={valid_search_name_status["name"]}'
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert len(data["result"]) > 0


def test_search_by_name_with_status(testing_app, valid_search_name_status):
    # Test with name and status parameters
    response = testing_app.get(
        f'/food-facilities/?name={valid_search_name_status["name"]}'
        f'&status={valid_search_name_status["status"]}'
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    
    # Check that all returned results have the requested status
    if len(data["result"]) > 0:
        for item in data["result"]:
            assert item["Status"] == "APPROVED"


def test_search_by_name_empty_results(testing_app, invalid_name):
    # Test with a name that shouldn't exist
    response = testing_app.get(f'/food-facilities/?name={invalid_name}')
    
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert len(data["result"]) == 0


def test_search_by_name_missing_parameter(testing_app):
    # Test missing required parameter
    response = testing_app.get("/food-facilities/")
    assert response.status_code == 422


def test_search_by_street_name(testing_app, valid_street_name):
    # Test street name search
    response = testing_app.get(f'/food-facilities/by-street?name={valid_street_name}')
    
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert len(data["result"]) > 0


def test_search_k_nearest(testing_app, sf_coordinates, k=5):
    # Test k-nearest search with SF coordinates
    response = testing_app.get(
        f'/food-facilities/nearby?'
        f'lat={sf_coordinates["lat"]}&lng={sf_coordinates["lng"]}&k={k}'
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert len(data["result"]) == k  


def test_search_k_nearest_with_status(testing_app, sf_coordinates, k=3, status="APPROVED"):
    # Test k-nearest with status filter
    response = testing_app.get(
        f'/food-facilities/nearby?'
        f'lat={sf_coordinates["lat"]}&lng={sf_coordinates["lng"]}'
        f'&k={k}&status={status}'
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert len(data["result"]) == k
    for facility in data["result"]:
        assert facility["Status"] == "APPROVED"