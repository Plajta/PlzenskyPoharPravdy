import random
import json

def fstr(template):
    return eval(f"f'{template}'")

with open('config/fact_config.json') as json_file:
    categories = json.load(json_file)

def generate_fact(dataload, obec):
    chosen = random.choice(list(categories.values()))
    try:
        path = random.choice(chosen["filepath"])
    except Exception:
        path = None
    results = []
    for column in chosen["columns"]:
        query = f'{chosen["uzemi_col"]} == "{obec}" and {column["column"]} == {column["value"]}'
        resul = dataload.query(query, column["output"], path)
        # print(resul)
        for num, result in enumerate(resul):
            print(f"{str(column['var_name'][num])}: {str(result)}")
            globals()[str(column['var_name'][num])] = str(result[0])
    # print(globals())
    globals()["obec"] = obec
    fact = fstr(chosen["template"])
    return fact