import pandas as pd
from typing import Optional
import numpy as np

class CSVservices:
    def __init__(self):
        self.data_path = "src\dataset\Mobile_Food_Facility_Permit.csv"
        self.df = pd.read_csv(self.data_path)


    def get_df(self):
        return self.df

    def get_applicant_list(self):
        query = self.df["Applicant"]
        return query
    
    def search_by_name(self, name: str, status: Optional[str] = None):
        name_query = self.df["Applicant"].str.contains(name, case=False, na=False)
        filtered_df = self.df[name_query]

        if(status):
            filtered_df = filtered_df[filtered_df["Status"] == status]
        
        result = filtered_df.replace({np.nan: None})

        return {"result": result.to_dict(orient="records")}
    
    def search_by_street_name(self, street_name: str):
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
            a = sin²(Δφ/2) + cos(φ1) * cos(φ2) * sin²(Δλ/2)
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

        
