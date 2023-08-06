'''
 # @ Author: Keivan Tafakkori
 # @ Created: 2023-05-11
 # @ Modified: 2023-05-12
 # @ Contact: https://www.linkedin.com/in/keivan-tafakkori/
 # @ Github: https://github.com/ktafakkori
 # @ Website: https://ktafakkori.github.io/
 # @ Copyright: 2023. MIT License. All Rights Reserved.
 '''

import cylp as cylp_interface
from cylp.cy import CyClpSimplex


def Get(model_object, result, input1, input2=None):

    input1 = input1[0]

    match input1:

        case 'variable':

            return model_object.primalVariableSolution[input2]

        case 'status':

            return result[0].status

        case 'objective':

            return -model_object.objectiveValue

        case 'time':

            return (result[1][1]-result[1][0])
