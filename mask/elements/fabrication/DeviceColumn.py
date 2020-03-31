import gdspy

from .. import Element

from ...forms import DicingLine

class DeviceColumn(Element):

    def __init__(self, parent, name, device, x, ymin, ymax, margin=150, dicingwidth=100, keepout=[], layers=None, lib=None):

        self.device = device

        self.x = x
        self.ymin = ymin
        self.ymax = ymax

        self.margin = margin
        self.dicingwidth = dicingwidth
        self.keepout = keepout

        super().__init__(parent, name, layers, lib)

    def construct(self):

        m = self.margin

        bbox = self.device.get_bounding_box()
        devw = bbox[1,0] - bbox[0,0]
        devh = bbox[1,1] - bbox[0,1]

        doffset = devw / 2 + m

        origin = (self.x, self.ymin + m + devh/2)

        ymax = 0

        while True:

            ref = gdspy.CellReference(self.device, origin=origin)

            if ref.get_bounding_box()[1,1] > self.ymax:
                break

            collision = self.__inKeepout(ref.get_bounding_box())
            if collision is not None:
                origin = (origin[0], origin[1] + collision + 3*m)
                continue

            ref_ymin = ref.get_bounding_box()[0,1]
            ref_ymax = ref.get_bounding_box()[1,1]
            self.cell.add(ref)

            ## Add top and bottom dicing line
            dicing_bottom = DicingLine(self.layers["DICING"], self.cell,
                self.dicingwidth, (self.x - doffset, ref_ymin - m), (self.x + doffset, ref_ymin - m))
            dicing_top = DicingLine(self.layers["DICING"], self.cell,
                self.dicingwidth, (self.x - doffset, ref_ymax + m), (self.x + doffset, ref_ymax + m))

            ## TODO fix proper detection for top and bottom end of vertical dicing lines
            ymax = ref_ymax


            origin = (origin[0], origin[1] + devh + 2*m)

        ## Add left and right dicing line
        dicing_left = DicingLine(self.layers["DICING"], self.cell,
            self.dicingwidth, (self.x - doffset, self.ymin), (self.x - doffset, ymax + m))
        dicing_right = DicingLine(self.layers["DICING"], self.cell,
            self.dicingwidth, (self.x + doffset, self.ymin), (self.x + doffset, ymax + m))


    def __inKeepout(self, bbox):

        for keepoutbox in self.keepout:
            if self.__bboxOverlap(bbox, keepoutbox):
                return keepoutbox[1,1] - bbox[0,1]

        return None

    def __bboxOverlap(self, bbox1, bbox2):

        if bbox1[0,0] > bbox2[1,0] or bbox2[0,0] > bbox1[1,0]:
            return False

        if bbox1[0,1] > bbox2[1,1] or bbox2[0,1] > bbox1[1,1]:
            return False

        return True
