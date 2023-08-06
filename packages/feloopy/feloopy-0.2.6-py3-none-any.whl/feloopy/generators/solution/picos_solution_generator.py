'''
 # @ Author: Keivan Tafakkori
 # @ Created: 2023-05-11
 # @ Modified: 2023-05-12
 # @ Contact: https://www.linkedin.com/in/keivan-tafakkori/
 # @ Github: https://github.com/ktafakkori
 # @ Website: https://ktafakkori.github.io/
 # @ Copyright: 2023. MIT License. All Rights Reserved.
 '''

import picos as picos_interface
import timeit

picos_solver_selector = {'cplex': 'cplex',
                         'cvxopt': 'cvxopt',
                         'ecos': 'ecos',
                         'glpk': 'glpk',
                         'gurobi': 'gurobi',
                         'mosek': 'mosek',
                         'mskfsn': 'mskfsn',
                         'osqp': 'osqp',
                         'scip': 'scip',
                         'smcp': 'smcp'}


def generate_solution(features):

    model_object = features['model_object_before_solve']
    model_objectives = features['objectives']
    model_constraints = features['constraints']
    directions = features['directions']
    constraint_labels = features['constraint_labels']
    debug = features['debug_mode']
    time_limit = features['time_limit']
    absolute_gap = features['absolute_gap']
    relative_gap = features['relative_gap']
    thread_count = features['thread_count']
    solver_name = features['solver_name']
    objective_id = features['objective_being_optimized']
    log = features['log']
    save = features['save_solver_log']
    save_model = features['write_model_file']
    email = features['email_address']
    max_iterations = features['max_iterations']
    solver_options = features['solver_options']

    if solver_name not in picos_solver_selector.keys():
        raise RuntimeError(
            "Using solver '%s' is not supported by 'picos'! \nPossible fixes: \n1) Check the solver name. \n2) Use another interface. \n" % (solver_name))

    match debug:

        case False:

            match directions[objective_id]:
                case "min":
                    model_object.set_objective(
                        'min', model_objectives[objective_id])
                case "max":
                    model_object.set_objective(
                        'max', model_objectives[objective_id])

            for constraint in model_constraints:
                model_object += constraint

            time_solve_begin = timeit.default_timer()
            result = model_object.solve(solver=solver_name)
            time_solve_end = timeit.default_timer()
            generated_solution = [result, [time_solve_begin, time_solve_end]]

    return generated_solution
