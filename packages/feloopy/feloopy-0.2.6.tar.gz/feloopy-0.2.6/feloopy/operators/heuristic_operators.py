'''
 # @ Author: Keivan Tafakkori
 # @ Created: 2023-05-11
 # @ Modified: 2023-05-12
 # @ Contact: https://www.linkedin.com/in/keivan-tafakkori/
 # @ Github: https://github.com/ktafakkori
 # @ Website: https://ktafakkori.github.io/
 # @ Copyright: 2023. MIT License. All Rights Reserved.
 '''

from ..helpers.empty import *
from ..helpers.error import *
import numpy as np
import math as mt


def generate_heuristic_variable(features, type, name, variable_dim, variable_bound, agent, no_agents):

    if no_agents==None:
        no_agents=100
    

    if features['agent_status'] == 'idle':

        if features['vectorized']:

            if variable_dim == 0:

                if type == 'pvar' or type == 'fvar':
                    return variable_bound[0] + np.random.rand(no_agents,1)*(variable_bound[1]-variable_bound[0])
                if type == 'bvar' or type == 'ivar':
                    return np.round(variable_bound[0] + np.random.rand(no_agents,1)*(variable_bound[1]-variable_bound[0])).astype(int)
                if type == 'svar':
                    raise VariableDimError("Dimension is set to be 0 or not defined for a sequential variable.")
                
            else:

                if type == 'pvar' or type == 'fvar':
                    return variable_bound[0] + np.random.rand(*tuple([no_agents]+[len(dims) for dims in variable_dim]))*(variable_bound[1]-variable_bound[0])
                if type == 'bvar' or type == 'ivar':
                    return np.round(variable_bound[0] + np.random.rand(*tuple([no_agents]+[len(dims) for dims in variable_dim]))*(variable_bound[1]-variable_bound[0])).astype(int) 
                if type == 'svar':          
                    return np.argsort(np.random.rand(*tuple([no_agents]+[len(dims) for dims in variable_dim])), axis=1)

        else:

            if variable_dim == 0:

                if type == 'pvar' or type == 'fvar':
                    return variable_bound[0] + np.random.rand()*(variable_bound[1]-variable_bound[0])
                if type == 'bvar' or type == 'ivar':
                    return np.round(variable_bound[0] + np.random.rand()*(variable_bound[1]-variable_bound[0])).astype(int)
                if type == 'svar':
                    raise VariableDimError("Dimension is set to be 0 or not defined for a sequential variable.")
            
            else:

                if type == 'pvar' or type == 'fvar':
                    return variable_bound[0] + np.random.rand(*tuple([len(dims) for dims in variable_dim]))*(variable_bound[1]-variable_bound[0])
                if type == 'bvar' or type == 'ivar':
                    return np.round(variable_bound[0] + np.random.rand(*tuple([len(dims) for dims in variable_dim]))*(variable_bound[1]-variable_bound[0])).astype(int) 
                if type == 'svar':          
                    return np.argsort(np.random.rand(*tuple([len(dims) for dims in variable_dim])), axis=1)
    else:

        spread = features['variable_spread'][name]
        if features['vectorized']:
            if variable_dim == 0:
                if type == 'bvar' or type == 'ivar':
                    return np.round(variable_bound[0] + agent[:, spread[0]:spread[1]] * (variable_bound[1] - variable_bound[0])).astype(int)
                
                elif type == 'pvar' or type == 'fvar':
                    return variable_bound[0] + agent[:, spread[0]:spread[1]] * (variable_bound[1] - variable_bound[0])
                else:
                    return np.argsort(agent[:, spread[name][0]:spread[name][1]])
            else:

                if type == 'bvar' or type == 'ivar':

                    var = np.round(
                        variable_bound[0] + agent[:, spread[0]:spread[1]] * (variable_bound[1] - variable_bound[0])).astype(int)

                    return np.reshape(var, [var.shape[0]]+[len(dims) for dims in variable_dim])

                elif type == 'pvar' or type == 'fvar':

                    var = variable_bound[0] + agent[:, spread[0]:spread[1]
                                                    ] * (variable_bound[1] - variable_bound[0])

                    return np.reshape(var, [var.shape[0]]+[len(dims) for dims in variable_dim])

                else:

                    return np.argsort(agent[:, spread[name][0]:spread[name][1]])
        else:

            if variable_dim == 0:

                if type == 'bvar' or type == 'ivar':

                    return np.round(variable_bound[0] + agent[spread[0]:spread[1]] * (variable_bound[1] - variable_bound[0])).astype(int)

                elif type == 'pvar' or type == 'fvar':

                    return variable_bound[0] + agent[spread[0]:spread[1]] * (variable_bound[1] - variable_bound[0])

                else:

                    return np.argsort(agent[spread[name][0]:spread[name][1]])

            else:

                if type == 'bvar' or type == 'ivar':

                    return np.reshape(np.round(variable_bound[0] + agent[spread[0]:spread[1]] * (variable_bound[1] - variable_bound[0])), [len(dims) for dims in variable_dim]).astype(int)

                elif type == 'pvar' or type == 'fvar':

                    return np.reshape(variable_bound[0] + agent[spread[0]:spread[1]] * (variable_bound[1] - variable_bound[0]), [len(dims) for dims in variable_dim])

                else:

                    return np.argsort(agent[spread[name][0]:spread[name][1]])