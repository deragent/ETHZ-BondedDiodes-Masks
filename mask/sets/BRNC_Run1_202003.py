import gdspy
import math

## Disable the default lib to make multi lib use possible
gdspy.library.use_current_library = False

from mask import config
from mask.processes import BRNC_202003
from mask.macros import Run1_TestSet

from mask.tools import MaskMerge

from mask.elements.electrical import Diode
from mask.elements.meta import Wafer
from mask.elements.meta import Mask
from mask.elements.fabrication import MarkerCoarse, DeviceColumn
from mask.forms import DicingLine



def main(args):

    ### Create the library and top cell
    lib = gdspy.GdsLibrary()
    config.GLOBAL["LIB"] = lib

    top = lib.new_cell('TOP_CELL')


    ### Create meta cells
    wafer = Wafer(top, 'WAFER', 150000)
    mask = Mask(top, 'MASK', 7*25400, {
            "DATE": "2020-03-12",
            "USER": "jorich",
            "LAYOUT": "DIODE-RUN-1%s"%("" if args.side is None else "-%s"%(args.side))
        }, githash=True)


    ### Add Markers
    markers, keepouts = BRNC_202003.createMarkers(lib)
    top.add(markers)



    ### Create diode cells
    diodes = lib.new_cell('DIODES')

    if args.side is not None:
        LABEL_HEIGHT = 500
        LABEL = (args.side, LABEL_HEIGHT)
    else:
        LABEL = None

    d15 = Diode(None, 'DIODE_15mm', 15000, rounding=1500, label=LABEL)
    d15_w = Diode(None, 'DIODE_W_15mm', 15000, rounding=1500, window=3000, label=LABEL)
    d12 = Diode(None, 'DIODE_12mm', 12000, rounding=1200, label=LABEL)
    d12_w = Diode(None, 'DIODE_W_12mm', 12000, rounding=1200, window=3000, label=LABEL)
    d8 = Diode(None, 'DIODE_8mm', 8000, rounding=800, label=LABEL)
    d8_w = Diode(None, 'DIODE_W_8mm', 8000, rounding=800, window=2000, label=LABEL)
    d6 = Diode(None, 'DIODE_6mm', 6000, rounding=600, label=LABEL)
    d6_w = Diode(None, 'DIODE_W_6mm', 6000, rounding=600, window=2000, label=LABEL)
    d4 = Diode(None, 'DIODE_4mm', 4000, rounding=400, label=LABEL)
    d4_w = Diode(None, 'DIODE_W_4mm', 4000, rounding=400, window=1000, label=LABEL)
    d2 = Diode(None, 'DIODE_2mm', 2000, rounding=200, label=LABEL)
    d2_w = Diode(None, 'DIODE_W_2mm', 2000, rounding=200, window=1000, label=LABEL)

    margin = 350
    dicingwidth = 100

    xoffset = margin

    ymin = [-61500, -61500, -56000, -49000, -42000, -36500]
    ymax = 50300

    DIODE_CONFIGS = [
        [d15_w, d15, d15],
        [d12_w, d12, d12],
        [d8_w, d8, d8],
        [d6_w, d6, d6],
        [d4_w, d4, d4],
        [d2_w, d2, d2],
    ]

    for ii, elements in enumerate(DIODE_CONFIGS):

        devices = [d.cell for d in elements]

        x = xoffset + elements[0].width/2

        column_r = DeviceColumn(diodes, 'COLUMN_R_%s'%(elements[0].name), devices,
            x, ymin[ii], min(-1*ymin[ii], ymax),
            margin=margin, dicingwidth=dicingwidth, keepout=keepouts)

        column_l = DeviceColumn(diodes, 'COLUMN_L_%s'%(elements[0].name), devices,
            -1*x, ymin[ii], min(-1*ymin[ii], ymax),
            margin=margin, dicingwidth=dicingwidth, keepout=keepouts)

        xoffset += elements[0].width + 2*margin

    top_dicing = DicingLine(config.GLOBAL["LAYERS"]["DICING"], diodes,
        dicingwidth, (-48400, 50500), (48400, 50500))

    top.add(diodes)

    ## Add test structures (VPD + TLM)
    testset = Run1_TestSet(lib)

    top.add(gdspy.CellReference(testset, rotation=90, origin=(-63000, -5000)))
    top.add(gdspy.CellReference(testset, rotation=-90, origin=(+63000, +5000)))
    top.add(gdspy.CellReference(testset, rotation=0, origin=(-5000, +63000)))


    ### Save the gds file
    lib.write_gds(args.output)
    ### Save and svg representation
    top.write_svg(args.output + '.svg', 0.1)

    if args.export is not None:
        merge = MaskMerge(top)

        for name, layers in config.GLOBAL["EXPORT"]:

            mask.setMaskName(name)

            merge.refresh()
            out = merge.mergeLayersIntoLib(layers, **config.GLOBAL["LAYERS"][name])

            out.write_gds(args.export + "/%s.gds"%(name))


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description='Create the mask layout for the BRNC Run-1 [202003].')
    parser.add_argument('-o', '--output', required=True,
                        help='Name of the output file.')
    parser.add_argument('-e', '--export', default=None,
                        help='Flag to export the fabrication mask layers into individual files.')
    parser.add_argument('-s', '--side', default=None, choices=["N", "P"],
                        help='Generate the mask for a specific side of the diodes.')

    args = parser.parse_args()

    main(args)
