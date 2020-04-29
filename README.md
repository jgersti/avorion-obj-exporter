# Avorion-OBJ-Export

Simple export app for Avorion Ship XML to OBJ/STL/PLY/VTK format.

OBJ/STL only support mesh export, PLY also exports color data.
VTK exports color, block type, build material, and cell index data in addition to the PolyData mesh.

The exported mesh contains the faces of all blocks.

## Requirements

 *  Python >= 3.7
 *  NumPy
 *  VTK
 *  PyVista
 
 ## Installation
 
  * Repository Clone
    ```
    git clone https://github.com/jgersti/avorion-obj-exporter.git
    cd avorion-obj-exporter
    pip install -e .
    ```
     
  * Archive
  
    Download archive and execute
    ```
    pip install <Archive>
    ```
 
 ## Usage

```
avorion-obj-exporter [-h] [-p [PATH]] [-f [{obj,stl,ply,vtk}]] [-o [OUTPUT]] file

positional arguments:
  file                  XML ship file to render.

optional arguments:
  -h, --help            show this help message and exit
  -p [PATH], --path [PATH]
                        Path to the file. Defaults to the 'ships' folder of
                        the avorion installation.
  -f [{obj,stl,ply,vtk}], --format [{obj,stl,ply,vtk}]
                        Format to export. [Default: obj]
  -o [OUTPUT], --output [OUTPUT]
                        Output file name. File ending will be ignored.
                        [Default: file argument]
   ```
