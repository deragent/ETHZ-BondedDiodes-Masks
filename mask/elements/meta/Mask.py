import gdspy

from .. import Element

from ...forms import TextList

class Mask(Element):

    T_HEIGHT = 2000

    def __init__(self, parent, name, size, text, margin=4000, layers=None, lib=None, githash=False):

        self.size = size
        self.margin = margin
        self.text = text

        if githash:
            import git
            repo = git.Repo(search_parent_directories=True)
            self.text['git'] = repo.head.object.hexsha[0:8]

        super().__init__(parent, name, layers, lib)

    def construct(self):

        self._constructFrame()

        if len(self.text) > 0:
            self._constructLabel()

    def _constructFrame(self):
        s2 = self.size/2
        s2m = self.size/2 - self.margin

        outer = gdspy.Rectangle((-s2, -s2), (s2, s2))
        inner = gdspy.Rectangle((-s2m, -s2m), (s2m, s2m))

        outline = gdspy.boolean(outer, inner, 'not', **self.layers["MASK_OUTLINE"])

        # offset1 = gdspy.offset(self.base, offset + spec[0], join='round', tolerance=self.tolerance)
        # offset2 = gdspy.offset(self.base, offset + spec[0] + spec[1], join='round', tolerance=self.tolerance)
        #
        # diff = gdspy.boolean(offset2, offset1, 'not', **self.layers["WAFER_OUTLINE"])

        os = self.margin / 5
        holes = [
            gdspy.Rectangle((-s2m, s2m+os), (s2m, s2-os)),
            gdspy.Rectangle((-s2m, -s2m-os), (s2m, -s2+os)),
            gdspy.Rectangle((s2m+os, -s2m), (s2-os, s2m)),
            gdspy.Rectangle((-s2m-os, -s2m), (-s2+os, s2m)),
        ]
        for hole in holes:
            outline = gdspy.boolean(outline, hole, 'not', **self.layers["MASK_OUTLINE"])

        self.cell.add(outline)


    def _constructLabel(self):

        x0 = -self.size/2 + 2.5*self.margin
        y0 = -self.size/2 + 2.5*self.margin

        textcell = self.lib.new_cell(self.name + '_LABEL')

        label = TextList(self.layers["MASK_LABEL"], textcell,
            self.text, height=2000, origin=(x0, y0))

        self.cell.add(textcell)
