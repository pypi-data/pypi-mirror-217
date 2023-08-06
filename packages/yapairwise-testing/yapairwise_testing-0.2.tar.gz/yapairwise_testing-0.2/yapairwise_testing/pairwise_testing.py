import csv
import pandas as pd

def pairwise_testing(input_variables, results_rules, csv_file):
    from itertools import product

    variables = list(input_variables.keys())
    if len(variables) < 2:
        return "Precisamos de pelo menos duas variáveis para gerar conjuntos."

    test_cases = []
    for values in product(*input_variables.values()):
        test_case = dict(zip(variables, values))
        test_cases.append(test_case)

    results = list(results_rules.keys())
    with open(csv_file, mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(variables + results)
        for test_case in test_cases:
            results_values = [rule(test_case) for rule in results_rules.values()]
            writer.writerow(list(test_case.values()) + results_values)

    print(f"Os casos de teste foram salvos no arquivo {csv_file}.")
    return pd.read_csv(csv_file)
