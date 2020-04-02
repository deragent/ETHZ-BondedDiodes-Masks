import gdspy

from .Layers import LayerSpecs
from .Export import ExportSpecs

GLOBAL = {
    "LAYERS": LayerSpecs(),
    "EXPORT": ExportSpecs(),
    "LIB": gdspy.GdsLibrary(),
}
