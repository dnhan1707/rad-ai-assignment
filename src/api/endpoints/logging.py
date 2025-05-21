from fastapi import APIRouter, HTTPException
from src.services.csv_services import CSVservices
from typing import Optional

router = APIRouter(
    prefix="/logging"
)

csv_service = CSVservices()

@router.get("/list_of_applicant")
def applicant_list():
    try:
        return csv_service.get_applicant_list()
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error with applicant_list, {str(e)}')

@router.get("/search_by_name")
def search_applicant_by_name(name: str, status: Optional[str] = None):
    try:
        return csv_service.search_by_name(name, status)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error with search_applicant, {str(e)}')


@router.get("/search_by_street_name")
def search_applicant_by_street_name(name: str):
    try:
        return csv_service.search_by_street_name(name)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error with search_applicant, {str(e)}')




