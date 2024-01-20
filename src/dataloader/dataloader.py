import os
from multiprocessing import Pool
import pandas as pd

def loader(filename):
    return pd.read_csv(filename)

def worker(data):
    csv = data[0]
    query = data[1]
    try:
        return csv.query(query)
    except Exception:
        return None

class Dataloader:
    def __init__(self, path, proc_count = 4):
        self.path = path
        self.proc_count = proc_count
        file_list = os.listdir(path)

        csv_names = [f"{path}/{file}" for file in file_list if ".csv" in file]
        with Pool(processes=self.proc_count) as pool:
            self.csv_files = pool.map(loader, csv_names)
    
    def query(self, query, columns):
        data = [[file,query] for file in self.csv_files]
        with Pool(processes=self.proc_count) as pool:
            results = pool.map(worker, data)
        
        if len(columns) > 0:
            return [[result[column].values[0] for result in results if result is not None and len(result[column].values) > 0] for column in columns] # OH YEAAAH BABYYYYY THAT'S WHAT WE'RE TALIKIN' 'BOUT
        else:
            return results


if __name__ == '__main__':
    dataloader = Dataloader("data/csv_data")
    results = dataloader.query('uzemi_txt == "Plzeň" and odpad_kod == 20')
    print(results)