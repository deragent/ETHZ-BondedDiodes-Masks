import gdspy

from .. import Element

from ...forms import DicingLine

class DeviceColumn(Element):

    def __init__(self, parent, name, generator, x, ymin, ymax, margin=150, dicingwidth=100, keepout=[], layers=None, lib=None):

        self.generator = generator

        self.x = x
        self.ymin = ymin
        self.ymax = ymax

        self.margin = margin
        self.dicingwidth = dicingwidth
        self.keepout = keepout

        super().__init__(parent, name, layers, lib)

    def construct(self):

        dw = self.dicingwidth

        bbox = self.generator.bbox()

        devw = bbox[1,0] - bbox[0,0]
        devh = bbox[1,1] - bbox[0,1]

        # TODO: This code currently assumes, that the cells to be repeated in
        # column are symmetric around X=0 and Y=0. This is not always the case.
        # To be fixed in the future!

        origin = (self.x, self.ymin + devh/2)

        ymax = 0

        dev_index = 0

        while True:

            ref = self.generator.instance()
            ref.translate(*origin)

            if ref.get_bounding_box()[1,1] > self.ymax:
                self.generator.retract()
                break

            collision = self.__inKeepout(ref.get_bounding_box())
            if collision is not None:
                origin = (origin[0], origin[1] + collision + dw)
                self.generator.retract()
                continue

            ref_ymin = ref.get_bounding_box()[0,1]
            ref_ymax = ref.get_bounding_box()[1,1]
            self.cell.add(ref)

            ## TODO fix proper detection for top and bottom end of vertical dicing lines
            ymax = ref_ymax


            origin = (origin[0], origin[1] + devh - dw)


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
