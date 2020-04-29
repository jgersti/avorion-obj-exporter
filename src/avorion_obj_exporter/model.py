import vtk
import numpy as np
import pyvista as pv

from avorion_obj_exporter.shapes import getCell


def _getColors(blocks):
    helper = vtk.vtkNamedColors()
    return np.asarray([helper.HTMLColorToRGBA(f"#{b['color'][2:]}") for b in blocks], dtype=np.uint8)


def _getOrientations(blocks, comp):
    return np.array([b['orientation'][comp] for b in blocks], dtype=np.uint64)


def _getMaterials(blocks):
    return np.array([b['material'] for b in blocks], dtype=np.uint64)


def _getTypes(blocks):
    return np.array([b['type'] for b in blocks], dtype=np.uint64)


def createModel(blocks, merge=False, tolerance=1e-6):

    def dist2(x,y):
        z = x-y
        return np.einsum('...i,...i->...', z, z)

    def insert(points, newPoints, indices):
        if merge:
            pIndices = []
            for p in newPoints:
                try:
                    i = next(i for i, q in enumerate(points) if dist2(p, q) < tolerance)
                except:
                    i = len(points)
                    points.append(p)
                finally:
                    pIndices.append(i)

            return np.array(pIndices)
        else:
            n = len(points)
            points.extend(newPoints)
            return np.arange(n, n+len(newPoints))

    cells = []
    offsets = []
    points = []
    types = []

    n = len(blocks)
    for i, _block in enumerate(blocks):
        _type, _indices, _points = getCell(_block)
        pIndices = insert(points, _points, _indices)

        if type(_indices) is list:
            cell = [[1+len(_indices), len(_indices)]]
            for sub in _indices:
                cell.extend([[len(sub)], pIndices[sub]])
                cell[0][0] += len(sub)
        else:
            cell = [[len(_indices)], pIndices[_indices]]

        cells.extend(np.concatenate(cell))
        offsets.append(1 + cell[0][0] + (offsets[-1] if offsets else 0))
        types.append(_type)

    model = pv.UnstructuredGrid(np.asarray(offsets), np.asarray(cells), np.asarray(types), np.asarray(points))

    data = model.cell_arrays
    data['color'] = _getColors(blocks)
    data['material'] = _getMaterials(blocks)
    data['type'] = _getTypes(blocks)

    return model.extract_surface(pass_pointid=False)
