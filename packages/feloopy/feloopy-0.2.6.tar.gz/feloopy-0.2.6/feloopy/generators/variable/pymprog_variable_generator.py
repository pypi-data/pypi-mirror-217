'''
 # @ Author: Keivan Tafakkori
 # @ Created: 2023-05-11
 # @ Modified: 2023-05-12
 # @ Contact: https://www.linkedin.com/in/keivan-tafakkori/
 # @ Github: https://github.com/ktafakkori
 # @ Website: https://ktafakkori.github.io/
 # @ Copyright: 2023. MIT License. All Rights Reserved.
 '''

import pymprog as pymprog_interface
import itertools as it

sets = it.product

VariableGenerator = pymprog_interface.var


def generate_variable(model_object, variable_type, variable_name, variable_bound, variable_dim=0):

    match variable_type:

        case 'pvar':

            '''

            Positive Variable Generator


            '''

            if variable_dim == 0:
                GeneratedVariable = VariableGenerator(
                    variable_name, bounds=(variable_bound[0], variable_bound[1]))
            else:
                if len(variable_dim) == 1:
                    GeneratedVariable = {key: VariableGenerator(variable_name, bounds=(
                        variable_bound[0], variable_bound[1])) for key in variable_dim[0]}
                else:
                    GeneratedVariable = {key: VariableGenerator(variable_name, bounds=(
                        variable_bound[0], variable_bound[1])) for key in it.product(*variable_dim)}

        case 'bvar':

            '''

            Binary Variable Generator


            '''
            if variable_dim == 0:
                GeneratedVariable = VariableGenerator(variable_name, bounds=(
                    variable_bound[0], variable_bound[1]), kind=int)
            else:
                if len(variable_dim) == 1:
                    GeneratedVariable = {key: VariableGenerator(variable_name, bounds=(
                        variable_bound[0], variable_bound[1]), kind=int) for key in variable_dim[0]}
                else:
                    GeneratedVariable = {key: VariableGenerator(variable_name, bounds=(
                        variable_bound[0], variable_bound[1]), kind=int) for key in it.product(*variable_dim)}

        case 'ivar':

            '''

            Integer Variable Generator


            '''

            if variable_dim == 0:
                GeneratedVariable = VariableGenerator(variable_name, bounds=(
                    variable_bound[0], variable_bound[1]), kind=int)
            else:
                if len(variable_dim) == 1:
                    GeneratedVariable = {key: VariableGenerator(variable_name, bounds=(
                        variable_bound[0], variable_bound[1]), kind=int) for key in variable_dim[0]}
                else:
                    GeneratedVariable = {key: VariableGenerator(variable_name, bounds=(
                        variable_bound[0], variable_bound[1]), kind=int) for key in it.product(*variable_dim)}

        case 'fvar':

            '''

            Free Variable Generator


            '''

            if variable_dim == 0:
                GeneratedVariable = VariableGenerator(
                    variable_name, bounds=(variable_bound[0], variable_bound[1]))
            else:
                if len(variable_dim) == 1:
                    GeneratedVariable = {key: VariableGenerator(variable_name, bounds=(
                        variable_bound[0], variable_bound[1])) for key in variable_dim[0]}
                else:
                    GeneratedVariable = {key: VariableGenerator(variable_name, bounds=(
                        variable_bound[0], variable_bound[1])) for key in it.product(*variable_dim)}

    return GeneratedVariable
