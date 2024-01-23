import os
from multiprocessing import Pool
import pandas as pd

def loader(filename):
    return [filename,pd.read_csv(filename)]

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
        self.csv_files = {}
        file_list = os.listdir(path)

        csv_names = [os.path.join(path,file) for file in file_list if ".csv" in file]
        with Pool(processes=self.proc_count) as pool:
            for filename, csv in pool.map(loader, csv_names):
                self.csv_files[os.path.basename(filename)] = csv
    
    def query(self, query, columns=[], filename=None):
        data = [[file[1],query] for file in self.csv_files.items() if filename is None or filename == file[0]]
        with Pool(processes=self.proc_count) as pool:
            results = pool.map(worker, data)
        
        if len(columns) > 0:
            return [[result[column].values[0] for result in results if result is not None and len(result[column].values) > 0] for column in columns] # OH YEAAAH BABYYYYY THAT'S WHAT WE'RE TALIKIN' 'BOUT
        else:
            return results


if __name__ == '__main__':
    dataloader = Dataloader("data/csv_data")
    results = dataloader.query('uzemi_txt == "Plzeň" and odpad_kod == 20', "data/csv_data/kanaliza.csv")
    print(results)