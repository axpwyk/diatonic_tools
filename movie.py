import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation


''' ----------------------------------------------------------------------------------------- '''
''' *********************************** curve and motion ************************************ '''
''' ----------------------------------------------------------------------------------------- '''


def bezier3(lambdas, position_1, position_2, control_point_1, control_point_2):
    x0 = np.array(position_1).reshape((1, -1))
    x1 = np.array(control_point_1).reshape((1, -1))
    x2 = np.array(control_point_2).reshape((1, -1))
    x3 = np.array(position_2).reshape((1, -1))
    lambdas = np.reshape(np.array(lambdas), (-1, 1))
    return (1-lambdas)**3*x0 + 3*(1-lambdas)**2*lambdas*x1 + 3*(1-lambdas)*lambdas**2*x2 + lambdas**3*x3


def bezier3t(times, position_1, position_2, control_point_1, control_point_2, precision=1e-12):
    # the first variable of position_1 (or position_2, control_point_1, control_point_2) is time variable
    func = lambda x: bezier3(x, position_1, position_2, control_point_1, control_point_2)
    times = np.array(times).reshape((-1, 1))
    test = 1/2*np.ones_like(times)
    iter = 2
    while(any(abs(times-func(test)[:, :1])>precision)):
        test = test + np.sign(times-func(test)[:, :1])*(1/2)**iter
        iter = iter + 1
        if iter - 1 > 1e5:
            raise BaseException('Max iteration times exceeded!')
    return bezier3(test, position_1, position_2, control_point_1, control_point_2)


def fancy_motion(times, time1, time2, pos1, pos2, type=None, factor=0.0):
    times = np.array(times).reshape((-1, 1))
    pos1 = np.array(pos1).reshape((1, -1))
    pos2 = np.array(pos2).reshape((1, -1))
    dim = len(pos1)
    sigmoid = lambda x: 1/(1+np.exp(-x))
    ease_factor = sigmoid(factor)
    fast_factor = sigmoid(factor)
    if type == 'slow-in-out':
        cp1 = (ease_factor, ) + (0, )*dim
        cp2 = (1-ease_factor, ) + (1, )*dim
    elif type == 'slow-in':
        cp1 = (ease_factor, ) + (0, )*dim
        cp2 = (1, )*(dim+1)
    elif type == 'slow-out':
        cp1 = (0, )*(dim+1)
        cp2 = (1-ease_factor, ) + (1, )*dim
    elif type == 'fast-in-out':
        cp1 = (0, ) + (fast_factor, )*dim
        cp2 = (1, ) + (1-fast_factor, )*dim
    elif type == 'fast-in':
        cp1 = (0, ) + (fast_factor, )*dim
        cp2 = (1, )*(dim+1)
    elif type == 'fast-out':
        cp1 = (0, )*(dim+1)
        cp2 = (1, ) + (1-fast_factor, )*dim
    elif type == 'slow-in-fast-out':
        cp1 = (ease_factor, ) + (0, )*dim
        cp2 = (1, ) + (1-fast_factor, )*dim
    elif type == 'fast-in-slow-out':
        cp1 = (0, ) + (fast_factor, )*dim
        cp2 = (1-ease_factor, ) + (1, )*dim
    else:
        cp1 = (0, )*(dim+1)
        cp2 = (1, )*(dim+1)
    def generator(times):
        return bezier3t(times, np.zeros((1, dim+1)),
                            np.ones((1, dim+1)),
                            np.array(cp1).reshape((1, -1)),
                            np.array(cp2).reshape((1, -1)))[:, 1:]
    return (pos2-pos1)*(generator((times-time1)/(time2-time1))-generator(0))+pos1


def bezier(lambdas, control_points):
    lambdas = np.array(lambdas).reshape(-1, 1)
    control_points = [np.array([np.array(point).reshape(1, -1) for point in control_points])]
    while(len(control_points[-1])>1):
        cur_points = control_points[-1]
        control_points.append([cur_point + lambdas * (next_point - cur_point) for (cur_point, next_point) in zip(cur_points[:-1], cur_points[1:])])
    return control_points[-1][0]


class Bezier(object):
    def __init__(self, lambdas, control_points):
        # L sections, N control points, D-dimension space, K iteration times, K = N
        self.lambdas = np.array(lambdas).reshape(-1, 1)  # [L, 1]
        self.control_points = np.array([np.array(control_point).reshape(-1) for control_point in control_points])  # [N, D]
        L = len(self.lambdas); N = len(self.control_points); D = len(self.control_points[0])
        self.control_points = np.stack([self.control_points]*L, axis=1)  # [N, L, D]
        self.tensor = np.zeros((N, N, L, D))  # [K, N, L, D]
        self.tensor[0, :, :, :] = self.control_points
        for k in range(1, len(self.control_points)):
            self.tensor[k, k:N] = self.tensor[k-1, k-1:N-1, :, :] + np.stack([self.lambdas]*(N-k), axis=0) * (self.tensor[k-1, k:N, :, :] - self.tensor[k-1, k-1:N-1, :, :])

    def get_data(self):
        # return x_data, y_data, z_data, ...
        return self.tensor[-1, -1, :, :].T

    def get_control_points(self, k, l):
        # k must in range(K), and l must in range(L)
        control_points = self.tensor[k, k:, l, :].T
        return control_points
