from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from src.services.food_facility_service import FoodFacilityService
from src.rate_limit import rate_limit


def create_food_facility_router() -> APIRouter:
    food_facility_router = APIRouter(
        prefix="/food-facilities",
        dependencies=[Depends(rate_limit)]
    )

    food_facility_service = FoodFacilityService()

    @food_facility_router.get("/")
    async def get_food_facilities(name: str, status: Optional[str] = None):
        """
        Get food facilities by name with optional status filter.
        """
        try:
            return await food_facility_service.search_by_name(name, status)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'Error retrieving food facilities: {str(e)}')

    @food_facility_router.get("/by-street")
    async def get_food_facilities_by_street(name: str):
        """
        Get food facilities located on a specific street.
        """
        try:
            return await food_facility_service.search_by_street_name(name)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'Error retrieving food facilities by street: {str(e)}')

    @food_facility_router.get("/nearby")
    async def get_nearby_food_facilities(
        lat: Optional[float] = None, 
        lng: Optional[float] = None, 
        limit: int = 5, 
        status: str = "APPROVED"
    ):
        """
        Get the nearest food facilities based on coordinates.
        """
        try:
            return await food_facility_service.find_k_nearest(lat, lng, limit, status)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'Error retrieving nearby food facilities: {str(e)}')

    # @food_facility_router.get("/applicants")
    # async def get_applicant_list():
    #     """
    #     Get list of all applicants.
    #     """
    #     try:
    #         return await food_facility_service.get_applicant_list()
    #     except Exception as e:
    #         raise HTTPException(status_code=500, detail=f'Error retrieving applicant list: {str(e)}')

    return food_facility_router