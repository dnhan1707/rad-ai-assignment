from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from src.services.food_facility_service import FoodFacilityService
from src.rate_limit import rate_limit


def create_food_facility_router() -> APIRouter:
    router = APIRouter(
        prefix="/food_facilities",
        dependencies=[Depends(rate_limit)]
    )

    food_facility_service = FoodFacilityService()

    @router.get("/list_of_applicant")
    async def applicant_list():
        try:
            return await food_facility_service.get_applicant_list()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'Error with applicant_list: {str(e)}')

    @router.get("/search_by_name")
    async def search_by_name(name: str, status: Optional[str] = None):
        try:
            return await food_facility_service.search_by_name(name, status)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'Error with search_by_name: {str(e)}')

    @router.get("/search_by_street_name")
    async def search_by_street_name(name: str):
        try:
            return await food_facility_service.search_by_street_name(name)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'Error with search_by_street_name: {str(e)}')

    @router.get("/search_k_nearest")
    async def search_by_lat_lng(lat: float, lng: float, k: int, status: str = "APPROVED"):
        try:
            return await food_facility_service.find_k_nearest(lat, lng, k, status)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'Error with search_by_lat_lng: {str(e)}')

    return router
