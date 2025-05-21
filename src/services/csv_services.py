import pandas as pd

class CSVservices:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def get_df(self):
        return self.df
    
    def load_csv(self):
        self.df = pd.read_csv(self.file_path)

    