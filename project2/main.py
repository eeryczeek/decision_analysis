import matplotlib.pyplot as plt
from problem import Problem
from uta import UTA
import pulp
from pulp import LpVariable, value, lpSum


def plot_functions(break_points: list[LpVariable]):
    max_value = max(value(break_point.utility)
                    for break_points in break_points.values() for break_point in break_points)

    for data_column, break_points in break_points.items():
        plt.figure()
        sorted_values = sorted(break_points, key=lambda x: value(x.value))
        x = [float(break_point.value) for break_point in sorted_values]
        y = [value(break_point.utility) for break_point in sorted_values]
        plt.plot(x, y, label=data_column)
        plt.xlabel(data_column)
        plt.ylabel('Utility')
        plt.title(f'Utility function for {data_column}')
        plt.legend()
        plt.ylim(-0.05, max_value + 0.05)
        plt.savefig(f'project2/results/{data_column.replace(' ', '_')}.png')


if __name__ == '__main__':
    parameters = {
        'Gross Domestic Product': {'type': 'gain', 'break points': 3},
        'Unemployment Rate': {'type': 'cost', 'break points': 3},
        'Income Tax Rate': {'type': 'cost', 'break points': 3},
        'Inflation': {'type': 'cost', 'break points': 3},
        'Total Reserves': {'type': 'gain', 'break points': 3},
        'GINI': {'type': 'cost', 'break points': 3},
    }

    parameters_test = {
        'g1': {'type': 'gain', 'break points': 5},
        'g2': {'type': 'gain', 'break points': 5},
        'g3': {'type': 'cost', 'break points': 5},
    }

    constraints = ['Colombia P Serbia', 'Serbia P Greece', 'Greece P Colombia',
                   'Colombia P Argentina', 'Argentina P Guatemala', 'Guatemala P Colombia']
    problem = Problem('data/prunned_dataset.csv', parameters)
    pulp.LpSolverDefault.msg = 0

    additional_constraints = []

    uta = UTA().add_constraints(problem, constraints).add_objective(problem)
    while True:
        print(f'additional_constraints: {additional_constraints}')
        for constraint in additional_constraints:
            uta.problem += constraint
        status = uta.problem.solve()

        omited_constraints = set()
        for variable in uta.problem.variables():
            if any(relation in variable.name for relation in ['_I_', '_P_']) and value(variable) == 1:
                omited_constraints.add(variable)
        additional_constraints.append(
            lpSum(omited_constraints) <= len(omited_constraints) - 1)
        print(f'omited_constraints: {omited_constraints}')

        if status != 1:
            print('no other solution found')
            break
        else:
            print('solution found')
            print(f'Objective value: {value(uta.problem.objective)}')
            plot_functions(uta.break_points)
            print(uta.get_resulting_ranking(problem))

        print('\n\n')
    print(uta.problem)
