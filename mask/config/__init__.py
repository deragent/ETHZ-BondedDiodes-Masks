import gdspy

from .Layers import LayerSpecs

GLOBAL = {
    "LAYERS": LayerSpecs(),
    "LIB": gdspy.GdsLibrary(),
}
