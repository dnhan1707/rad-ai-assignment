from typing import Optional
import numpy as np
from src.services.csv_services import CSVservices


file_path = "src/dataset/Mobile_Food_Facility_Permit.csv"
csv_services = CSVservices(file_path)

class FoodFacilityService:
    def __init__(self):
        csv_services.load_csv() 
        self.df = csv_services.get_df()
        if self.df is None:
            raise ValueError("DataFrame not loaded properly")
            
    async def search_by_name(self, name: str, status: Optional[str] = None):
        name_query = self.df["Applicant"].str.contains(name, case=False, na=False)
        filtered_df = self.df[name_query]

        if(status):
            filtered_df = filtered_df[filtered_df["Status"].str.upper() == status]
        
        result = filtered_df.replace({np.nan: None})
        return {"result": result.to_dict(orient="records")}
    
    async def search_by_street_name(self, street_name: str):
        street_name_query = self.df["Address"].str.contains(street_name, case=False, na=False)
        filtered_df = self.df[street_name_query]
        
        result = filtered_df.replace({np.nan: None})
        return {"result": result.to_dict(orient="records")}
    
    def haversine_distance_formula(self, lng_1, lat_1, lng_2, lat_2):
        '''
            d = 2 * r * asin(sqrt(a))
            where:
                d: is the disd: is the distance between the two points.
                r: is the radius of the sphere (e.g., for Earth, r ≈ 6371 km or 3959 miles).
                asin: is the inverse sine functiontance between the two points.
            and:
            a = sin^2(Δφ/2) + cos(φ1) * cos(φ2) * sin^2(Δλ/2)
                Δφ: is the difference in latitude (φ2 - φ1). 
                Δλ: is the difference in longitude (λ2 - λ1). 
                φ1: and φ2 are the latitudes of the two points. 
                λ1: and λ2 are the longitudes of the two points. 

        '''
        r = 6371 # This is Earth radius

        # Convert degrees to radians
        lng_1, lat_1, lng_2, lat_2 = map(np.radians, [lng_1, lat_1, lng_2, lat_2])
        lng_diff = abs(lng_1 - lng_2)
        lat_diff = abs(lat_1 - lat_2)

        a = np.sin(lat_diff/2)**2 + np.cos(lat_1) * np.cos(lat_2) * np.sin(lng_diff/2)**2
        d = 2 * r * np.arcsin(np.sqrt(a))

        return d
    
    async def find_k_nearest(self, lat: Optional[float] = None, lng: Optional[float] = None, k: int = 5, status: str = "APPROVED"):
        filtered_df = self.df[self.df["Status"].str.upper() == status]
        if(lng and lat):
            filtered_df = filtered_df.dropna(subset=["Latitude", "Longitude"])

            # calculate distance and add distance column
            filtered_df["distance"] = filtered_df.apply(
                lambda row: self.haversine_distance_formula(lng, lat, row["Longitude"], row["Latitude"]),
                axis=1
            )
            k_nearest = filtered_df.sort_values("distance").head(k)
            result = k_nearest.replace({np.nan: None})

            return {"result": result.to_dict(orient="records")}
        else:
            filtered_df = filtered_df.head(k)
            result = filtered_df.replace({np.nan: None})
            return {"result": result.to_dict(orient="records")}

        
