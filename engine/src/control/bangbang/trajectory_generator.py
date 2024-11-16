import numpy as np
import math
from control.bangbang.solver import DOFSolver
from control.bangbang.utils import Constraints, State
from sysmic_kit import *

class TrajectoryGenerator:
    def __init__(self, robot_constraints : Constraints):
        self.robot_constraints = robot_constraints

    def get_trajectory(self, v : Vector2, from_point : tuple[float, float], to_point : tuple[float, float]):
        wfx = to_point.x - from_point.x
        wfy = to_point.y - from_point.y
        problem = DOFSolver( State(v.x, 0, 0, 0) , State(v.y, 0, 0, 0), self.robot_constraints, wfx, wfy)
        x, y = problem.solve()
        # Combine points
        if len(x) == 1:
            x.append(x[0])
        if len(y) == 1:
            y.append(y[0])
        #x = [state.v for state in x]
        #y = [state.v for state in y]
        x = self._generate_points(x)
        y = self._generate_points(y)
        sol = self._combine_points(x,y)
        final_sol = []
        for point in sol:
            final_sol.append(Vector2(point[0], point[1]))
        return final_sol


    def _combine_points(self, list1, list2):
        # Get the length of the longest list
        max_length = max(len(list1), len(list2))
        
        # Extend both lists to the maximum length by filling with the default value
        extended_list1 = list1 + [0] * (max_length - len(list1))
        extended_list2 = list2 + [0] * (max_length - len(list2))
        
        # Combine both extended lists into tuples
        combined = list(zip(extended_list1, extended_list2))
        
        return combined
        
    # PROBLEM: the generated points is not reaching the final value for example [1,2] => [1,...,1.96]
    def _generate_points(self, input_list, total_points=60):
            final_list = []
            for i in range(0, len(input_list) - 1):
                point_i0 = input_list[i]
                point_i1 = input_list[i + 1]
                diff_t = point_i1.t - point_i0.t
                n_points = math.ceil(diff_t*60)
                points = np.linspace(point_i0.v, point_i1.v, n_points, endpoint=False).tolist()
                final_list += points
            return final_list
    