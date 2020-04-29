
import numpy as np

try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET

from pathlib import Path
from dataclasses import dataclass


@dataclass
class Block:
    lower: np.ndarray
    upper: np.ndarray
    orientation: np.ndarray
    type: int
    material: int
    color: str


def _blockStats(block, legacy=False):
    stats = {}
    if block.tag == 'block':
        attr = block.attrib
        stats['orientation'] = np.array([attr['look'], attr['up']], dtype=np.int64)
        stats['type'] = int(attr['index'])
        stats['material'] = int(attr['material'])
        stats['color'] = attr['color']

        if legacy:
            stats['lower'] = np.array([attr['lowerX'], attr['lowerY'], attr['lowerZ']], dtype=np.float64)
            stats['upper'] = np.array([attr['upperX'], attr['upperY'], attr['upperZ']], dtype=np.float64)
        else:
            stats['lower'] = np.array([attr['lx'], attr['ly'], attr['lz']], dtype=np.float64)
            stats['upper'] = np.array([attr['ux'], attr['uy'], attr['uz']], dtype=np.float64)
    else:
        raise ValueError('invalid tag.')

    return stats


def readShipXML (file):
    print(f'Reading File: {file}')
    tree = ET.parse(str(file))
    root = tree.getroot()

    format = root.find('.//block[@lx]') == None
    blocks = [_blockStats(i, legacy=format) for i in root.findall('.//block' if format else 'plan//block')]

    if len(blocks) == 0:
        raise IOError(f'Could not read file \'{file}\'.')

    return blocks
