import random
import json

# categories = {
#     "svatby_a_rozvody": {"columns": [{"column": "vuk","value": '"DEM0013"', "output": ["hodnota", "rok"], "var_name": ["snatky", "rok"]}, {"column": "vuk","value": '"DEM0014"', "output": ["hodnota", "rok"], "var_name": ["rozvody", "rok"]}], "uzemi_col": "vuzemi_txt", "template": "Vědeli jste že v {misto} se za rok {rok} vzalo {snatky} a rozvedlo {rozvody} párů?"}, # DEM0013 Svatby, DEM0014 Rozvody
#     "zemreli": {"columns": [{"column": "vuk","value": '"DEM0008"', "output": ["hodnota", "rok"], "var_name": ["smrti", "rok"]}], "template": "Vědeli jste že v {misto} za rok {rok} zemřelo {zemrelo} lidi."},
#     "pristehovali": {"columns": [{"column": "vuk","value": '"DEM0009"', "output": ["hodnota", "rok"], "var_name": ["pristehovalo", "rok"]}]},
#     "zumpa": {"columns": [["odpad_kod", 20]], "uzemi_col": "uzemi_txt", "output":  ["hodnota"]}
# }

def fstr(template):
    return eval(f"f'{template}'")

with open('data/other_data/fact_config.json') as json_file:
    categories = json.load(json_file)

def generate_fact(dataload, obec):
    chosen = random.choice(list(categories.values()))
    results = []
    for column in chosen["columns"]:
        query = f'{chosen["uzemi_col"]} == "{obec}" and {column["column"]} == {column["value"]}'
        resul = dataload.query(query, column["output"])
        # print(resul)
        for num, result in enumerate(resul):
            print(f"{str(column['var_name'][num])}: {str(result)}")
            globals()[str(column['var_name'][num])] = str(result[0])
    # print(globals())
    globals()["obec"] = obec
    fact = fstr(chosen["template"])
    return fact
    

if __name__ == "__main__":
    from dataloader import Dataloader
    dataload = Dataloader("data/csv_data")
    print(generate_fact(dataload, "Plzeň"))