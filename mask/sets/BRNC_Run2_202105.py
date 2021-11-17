import gdspy
import math
import os

import numpy as np

## Disable the default lib to make multi lib use possible
gdspy.library.use_current_library = False

from mask import config as GC
from mask.processes import BRNC_202105
from mask.macros import Run2_TestSet, Run1_TestSet

from mask.tools import MaskMerge
from mask.tools import Outline

from mask.elements.electrical import Diode, Pixels2xN, Pixels4x4
from mask.elements.meta import Wafer
from mask.elements.meta import Mask
from mask.elements.fabrication import MarkerCoarse, DeviceColumn
from mask.forms import DicingLine, Flood
from mask.elements import CallbackGenerator

from mask.tools import PlotterLib


def main(args):

    ### Create the library and top cell
    lib = gdspy.GdsLibrary()
    GC.GLOBAL["LIB"] = lib

    top = lib.new_cell('TOP_CELL')


    outline = Outline(100000, flat=32500)


    ### Create meta cells
    wafer = Wafer(top, 'WAFER', 100000, flat=32500, margin=3000)
    mask = Mask(top, 'MASK', 5*25400, {
            "DATE": "2021-05-31",
            "USER": "jorich",
            "LAYOUT": "DIODE-RUN-2%s"%("" if args.side is None else "-%s"%(args.side))
        }, textheight=1500, margin=3000, githash=True)


    ### Add Markers
    markers, keepouts = BRNC_202105.createMarkers(lib)
    top.add(gdspy.CellReference(markers))

    ### Add Wafer Markers
    wafer_markers = BRNC_202105.createWaferAlignment(lib)
    top.add(gdspy.CellReference(wafer_markers))

    ### Create diode cells
    diodes = lib.new_cell('DIODES')

    LABEL_HEIGHT = 300

    ADD_LABEL = (args.side == 'N')

    MARGIN = 150
    DW = 100

    BACK = args.side=='P'

    xoffset = -DW/2

    ymin = [-43000, -40000, -35000, -29500, -24000]
    ymax = 29000

    DIODE_CONFIGS = [
        ['DIODE_12mm', 12000, 3000, 'B'],
        ['DIODE_8mm', 8000, 2000, 'C'],
        ['DIODE_6mm', 6000, 2000, 'D'],
        ['DIODE_4mm', 4000, 1000, 'E'],
        ['DIODE_2mm', 2000, 1000, 'F'],
    ]

    TOP_DICING_Y = 29000

    for ii, config in enumerate(DIODE_CONFIGS):

        def createDiode(lib, count, index):
            if ADD_LABEL:
                label = (config[3] + str(count), LABEL_HEIGHT)
            else:
                label = None

            name = config[0] + '_%i'%(count)
            window = config[2] if (index % 3) == 2 else 0

            element = Diode(lib, name, config[1], back=BACK,
                            rounding=(config[1]/10), window=window,
                            label=label, dicingwidth=DW, margin=MARGIN)

            return element.cell

        generator = CallbackGenerator(lib, createDiode)


        x = xoffset + generator.width()/2

        dicinglines = [0]

        column_r = DeviceColumn(diodes, 'COLUMN_R_%s'%(config[0]), generator,
            x, ymin[ii], min(-1*ymin[ii], ymax),
            margin=MARGIN, dicingwidth=DW, keepout=keepouts)

        dicinglines.append(column_r.cell.get_bounding_box()[1][0])

        generator.reset()

        column_l = DeviceColumn(diodes, 'COLUMN_L_%s'%(config[0]), generator,
            -1*x, ymin[ii], min(-1*ymin[ii], ymax),
            margin=MARGIN, dicingwidth=DW, keepout=keepouts)

        dicinglines.append(column_l.cell.get_bounding_box()[0][0])


        # Add vertical dicing lines from the wafer edge
        for pos in dicinglines:
            ystart = outline.yMaxAtX(pos)
            if ystart > TOP_DICING_Y:
                ystart = TOP_DICING_Y

            if pos != 0:
                pos = pos - math.copysign(DW/2, pos)

            line = DicingLine(GC.GLOBAL["LAYERS"]["DICING"], diodes,
                DW, (pos, ystart), (pos, outline.yMinAtX(pos)))


        xoffset += generator.width() - DW

    # Horizontal dicing line to separate the top test structures
    top_dicing = DicingLine(GC.GLOBAL["LAYERS"]["DICING"], diodes,
        DW, (outline.xMinAtY(TOP_DICING_Y), TOP_DICING_Y), (outline.xMaxAtY(TOP_DICING_Y), TOP_DICING_Y))

    top.add(gdspy.CellReference(diodes,
        x_reflection=BACK, rotation=(180 if BACK else 0)
    ))



    # Add multi pixel test structures
    pixels = lib.new_cell('PIXEL_STRUCTURES')

    pixel2 = Pixels2xN(lib, 'PIXEL_2X2', 2, 500, 100,
        dicingwidth=DW, margin=MARGIN, back=BACK)

    pixels.add(gdspy.CellReference(pixel2.cell, origin=(0, TOP_DICING_Y+(pixel2.height-DW)*0.5)))
    pixels.add(gdspy.CellReference(pixel2.cell, origin=(0, TOP_DICING_Y+(pixel2.height-DW)*1.5)))
    pixels.add(gdspy.CellReference(pixel2.cell, origin=(0, TOP_DICING_Y+(pixel2.height-DW)*2.5)))


    pixel4x4_large = Pixels4x4(lib, 'PIXEL_4X4_LARGE', 1000, 200, contactsize=1000, back=BACK)

    x_offset = (pixel2.width + pixel4x4_large.width - 2*DW)*0.5
    pixels.add(gdspy.CellReference(pixel4x4_large.cell, origin=(-x_offset, TOP_DICING_Y+(pixel4x4_large.height-DW)*0.5)))
    pixels.add(gdspy.CellReference(pixel4x4_large.cell, origin=(+x_offset, TOP_DICING_Y+(pixel4x4_large.height-DW)*0.5)))


    pixel15 = Pixels2xN(lib, 'PIXEL_2X15', 15, 500, 100,
        dicingwidth=DW, margin=MARGIN, back=BACK)

    x_offset += (pixel4x4_large.width + pixel15.height - 2*DW)*0.5
    pixels.add(gdspy.CellReference(pixel15.cell, rotation=90, origin=(-x_offset, TOP_DICING_Y+(pixel15.width-DW)*0.5)))
    pixels.add(gdspy.CellReference(pixel15.cell, rotation=90, origin=(+x_offset, TOP_DICING_Y+(pixel15.width-DW)*0.5)))


    pixel4x4 = Pixels4x4(lib, 'PIXEL_4X4', 500, 100, back=BACK)

    x_offset += (pixel15.height + pixel4x4.width - 2*DW)*0.5
    pixels.add(gdspy.CellReference(pixel4x4.cell, origin=(-x_offset, TOP_DICING_Y+(pixel4x4.height-DW)*0.5)))
    pixels.add(gdspy.CellReference(pixel4x4.cell, origin=(+x_offset, TOP_DICING_Y+(pixel4x4.height-DW)*0.5)))
    pixels.add(gdspy.CellReference(pixel4x4.cell, origin=(-x_offset, TOP_DICING_Y+(pixel4x4.height-DW)*1.5)))
    pixels.add(gdspy.CellReference(pixel4x4.cell, origin=(+x_offset, TOP_DICING_Y+(pixel4x4.height-DW)*1.5)))


    pixel4x4_small = Pixels4x4(lib, 'PIXEL_4X4_SMALL', 200, 50, contactsize=200, trench=20, back=BACK)

    x_offset += (pixel4x4.height + pixel4x4_small.width - 2*DW)*0.5
    for ii in range(4):
        pixels.add(gdspy.CellReference(pixel4x4_small.cell, origin=(-x_offset, TOP_DICING_Y+(pixel4x4_small.height-DW)*(ii+0.5))))
        pixels.add(gdspy.CellReference(pixel4x4_small.cell, origin=(+x_offset, TOP_DICING_Y+(pixel4x4_small.height-DW)*(ii+0.5))))


    top.add(gdspy.CellReference(pixels,
        x_reflection=BACK, rotation=(180 if BACK else 0)
    ))


    ## Add test structures (VPD + TLM)
    testset_vert, testset_hor = Run2_TestSet(lib)

    top.add(gdspy.CellReference(testset_vert, rotation=180, origin=(+42500, -11000), x_reflection=True))
    top.add(gdspy.CellReference(testset_vert, rotation=0, origin=(-42500, -11000)))

    top.add(gdspy.CellReference(testset_hor, rotation=180, origin=(+32500, +31000), x_reflection=True))
    top.add(gdspy.CellReference(testset_hor, rotation=0, origin=(-32500, +31000)))

    # Add old linear TLM as a reference
    testset_old = Run1_TestSet(lib)

    top.add(gdspy.CellReference(testset_old, origin=(-10000, 41500)))



    ## Add text ident
    title_text = gdspy.Text(
        "ETHZ - IPA\nRubbia Group\nSensor Project\nSimple Bonded Diodes - Run 2", 700,
        position=(-43500, 3000), angle=0.5*math.pi, **GC.GLOBAL["LAYERS"]["METALIZATION"]
    )
    top.add(title_text)

    author_text = gdspy.Text(
        "Johannes Wuethrich\nJune 2021", 700,
        position=(+42000, 3000), angle=0.5*math.pi, **GC.GLOBAL["LAYERS"]["METALIZATION"]
    )
    top.add(author_text)


    ### Save the gds file
    lib.write_gds(args.output)
    ### Save and svg representation
    top.write_svg(args.output + '.svg', 0.1)


    ### Generate a matplotlib-plotter
    plot_name = os.path.basename(args.output).replace(".gds", "")
    plot_name = "Plotter" + plot_name.replace("_", "")
    plotter = PlotterLib(plot_name, lib)

    plotter.include("DIODE_.*_[0-9]+")
    plotter.rename("DIODE_", "_")
    plotter.rename("_2mm_", "F")
    plotter.rename("_4mm_", "E")
    plotter.rename("_6mm_", "D")
    plotter.rename("_8mm_", "C")
    plotter.rename("_12mm_", "B")

    plotter.generate()
    plot_file = os.path.split(args.output)[0]
    plot_file = os.path.join(plot_file, plot_name + ".py")
    plotter.write(plot_file)

    if args.export is not None:
        merge = MaskMerge(top)

        for name, layers in GC.GLOBAL["EXPORT"]:

            mask.setMaskName(name)

            merge.refresh()
            out = merge.mergeLayersIntoLib(layers, **GC.GLOBAL["LAYERS"][name])

            out.write_gds(args.export + "/%s.gds"%(name))

            ### Save and svg representation
            style = {(GC.GLOBAL["LAYERS"][name]["layer"], GC.GLOBAL["LAYERS"][name]["datatype"]): {'fill': '#FFFFFF'}}
            out.top_level()[0].write_svg(args.export + "/%s.svg"%(name), 0.02, style=style)


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description='Create the mask layout for the BRNC Run-2 [202105].')
    parser.add_argument('-o', '--output', required=True,
                        help='Name of the output file.')
    parser.add_argument('-e', '--export', default=None,
                        help='Flag to export the fabrication mask layers into individual files.')
    parser.add_argument('-s', '--side', default=None, choices=["N", "P"],
                        help='Generate the mask for a specific side of the diodes.')

    args = parser.parse_args()

    main(args)
