import vtk


def writeVTK (model, file):
    file = file.with_suffix('.vtp')
    print(f'Writing File : {file}')

    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetInputData(model)
    writer.SetFileName(str(file))
    writer.SetDataModeToBinary()
    writer.Write()


def writePLY(model, file):
    file = file.with_suffix('.ply')
    print(f'Writing File : {file}')

    writer = vtk.vtkPLYWriter()
    writer.SetEnableAlpha(True)
    writer.SetInputData(model)
    writer.SetArrayName('color')
    writer.SetFileName(str(file))
    writer.SetFileTypeToBinary()
    writer.Write()


def writeSimpleOBJ(model, file):
    file = file.with_suffix('.obj')
    print(f'Writing File : {file}')

    writer = vtk.vtkOBJWriter()
    writer.SetFileName(str(file))
    writer.SetInputData(model)
    writer.Write()


def writeSTL(model, file):
    file = file.with_suffix('.stl')
    print(f'Writing File : {file}')

    model.compute_normals(inplace=True)

    writer = vtk.vtkSTLWriter()
    writer.SetFileName(str(file))
    writer.SetInputData(model)
    writer.Write()
