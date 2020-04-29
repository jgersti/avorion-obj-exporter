import numpy as np
from avorion_obj_exporter.categories import SHAPES

def _rotateReference(points, orientation):
    # np.any((a < 1) | (a > 5))
    if np.any((orientation < 0) | (orientation > 5)):
        print(f'Invalid orientation: {orientation}')
        return points

    o = np.asarray([0.5, 0.5,0.5])
    R = np.zeros((3,3))

    sign = lambda b: 2*b-1

    i, j = orientation // 2
    k = 3 - i - j
    u, v = sign(orientation % 2)
    w = u*v*sign(i < j)*sign(k != 1)
    R[i,0] = u
    R[j,1] = v
    R[k,2] = w

    return np.einsum('ij,...j->...i', R, points-o) + o

def _getHexahedron(lower, upper, orientation):
    ref = np.asarray([[0, 0, 0],
                      [0, 0, 1],
                      [1, 0, 1],
                      [1, 0, 0],
                      [0, 1, 0],
                      [0, 1, 1],
                      [1, 1, 1],
                      [1, 1, 0]])
    indices = np.asarray([0, 1, 2, 3, 4, 5, 6, 7])

    points = _rotateReference(ref, orientation)
    points = np.einsum('...i,i->...i', points, upper-lower) + lower
    return '12', indices, points

def _getWedge(lower, upper, orientation):
    ref = np.asarray([[0, 0, 0],
                      [1, 0, 0],
                      [1, 0, 1],
                      [0, 0, 1],
                      [1, 1, 0],
                      [1, 1, 1]])
    indices = np.asarray([3, 2, 5, 0, 1, 4])

    points = _rotateReference(ref, orientation)
    points = np.einsum('...i,i->...i', points, upper-lower) + lower
    return '13', indices, points

def _getPyramid1(lower, upper, orientation):
    ref = np.asarray([[0, 0, 0],
                      [0, 0, 1],
                      [1, 0, 1],
                      [1, 0, 0],
                      [1, 1, 0]])
    indices = np.asarray([0, 1, 2, 3, 4])

    points = _rotateReference(ref, orientation)
    points = np.einsum('...i,i->...i', points, upper-lower) + lower
    return '14', indices, points


def _getPyramid2(lower, upper, orientation):
    ref = np.asarray([[0, 0, 0],
                      [0, 1, 0],
                      [1, 1, 1],
                      [1, 0, 1],
                      [1, 0, 0]])
    indices = np.asarray([0, 1, 2, 3, 4])

    points = _rotateReference(ref, orientation)
    points = np.einsum('...i,i->...i', points, upper-lower) + lower
    return '14', indices, points

def _getTetra1(lower, upper, orientation):
    ref = np.asarray([[0, 0, 0],
                      [1, 0, 0],
                      [1, 0, 1],
                      [1, 1, 0]])
    indices = np.asarray([0, 1, 3, 2])

    points = _rotateReference(ref, orientation)
    points = np.einsum('...i,i->...i', points, upper-lower) + lower
    return '10', indices, points

def _getTetra2(lower, upper, orientation):
    ref = np.asarray([[0, 0, 0],
                      [0, 0, 1],
                      [1, 0, 1],
                      [0, 1, 0]])
    indices = np.asarray([0, 1, 2, 3])

    points = _rotateReference(ref, orientation)
    points = np.einsum('...i,i->...i', points, upper-lower) + lower
    return '10', indices, points

def _getTetra3(lower, upper, orientation):
    ref = np.asarray([[1, 0, 0],
                      [0, 0, 1],
                      [1, 0, 1],
                      [1, 1, 0]])
    indices = np.asarray([0, 1, 2, 3])

    points = _rotateReference(ref, orientation)
    points = np.einsum('...i,i->...i', points, upper-lower) + lower
    return '10', indices, points

def _getPolyhedron(lower, upper, orientation):
    ref = np.asarray([[0, 0, 0],
                      [0, 0, 1],
                      [1, 0, 1],
                      [1, 0, 0],
                      [0, 1, 0],
                      [1, 1, 1],
                      [1, 1, 0]])
    indices = [np.asarray([0, 1, 2, 3]),
               np.asarray([0, 4, 6, 3]),
               np.asarray([2, 3, 6, 5]),
               np.asarray([0, 1, 4]),
               np.asarray([1, 2, 5]),
               np.asarray([4, 5, 6]),
               np.asarray([1, 5, 4])]

    points = _rotateReference(ref, orientation)
    points = np.einsum('...i,i->...i', points, upper-lower) + lower
    return '42', indices, points

def getCell(block):
    index = block['type']
    lower = block['lower']
    upper = block['upper']
    orientation = block['orientation']

    if index in SHAPES['Edge']:
        return _getWedge(lower, upper, orientation)
    elif index in SHAPES['Corner 1']:
        return _getTetra1(lower, upper, orientation)
    elif index in SHAPES['Corner 2']:
        return _getPolyhedron(lower, upper, orientation)
    elif index in SHAPES['Corner 3']:
        return _getPyramid1(lower, upper, orientation)
    elif index in SHAPES['Twisted Corner 1']:
        return _getTetra2(lower, upper, orientation)
    elif index in SHAPES['Twisted Corner 2']:
        return _getTetra3(lower, upper, orientation)
    elif index in SHAPES['Flat Corner']:
        return _getPyramid2(lower, upper, orientation)
    else:
        return _getHexahedron(lower, upper, orientation)
