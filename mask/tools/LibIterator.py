import gdspy

import re
import numpy as np

class Transform():

    def apply(t, point):
        old = np.ones((3, 1))
        old[0:2,0] = point
        new = t @ old

        return new[0:2,0].T

    def identity():
        return np.diag((1,1,1))

    def magnify(f):
        t = Transform.identity()
        t[0,0] = f
        t[1,1] = f
        return t

    def xref():
        t = Transform.identity()
        # Reflection on the x axis, not along the x-axis!!!
        t[1,1] = -1
        return t

    def rotate(theta):
        t = Transform.identity()
        c, s = np.cos(theta), np.sin(theta)
        t[0:2,0:2] = np.array(((c, -s), (s, c)))
        return t

    def translate(origin):
        t = Transform.identity()
        t[0:2,2] = np.array(origin)
        return t

    def __init__(self, ref=None):
        t = Transform.identity()

        if ref is not None:
            if ref.magnification is not None:
                t = Transform.magnify(self.magnification) @ t
            if ref.x_reflection:
                t = Transform.xref() @ t
            if ref.rotation is not None:
                t = Transform.rotate(np.radians(ref.rotation)) @ t
            t = Transform.translate(ref.origin) @ t

        self.t = t


class LibIterator():

    def __init__(self, lib):

        self.lib = lib

        self.match = []
        self.replace = []

    def rename(self, match, replace):
        self.replace.append((match, replace))

    def include(self, filter):
        self.match.append(filter)

    def _match(self, name):
        if len(self.match) == 0:
            return True

        for match in self.match:
            if re.search(match, name):
                return True

        return False

    def _rename(self, name):

        for match, replace in self.replace:
            name = re.sub(match, replace, name)

        return name

    def _traverse(self, cell, t):

        # Treat the current cell
        if self._match(cell.name):
            name = self._rename(cell.name)
            self._exec(name, cell, t)

        # Recurse into referenced sub-cells
        for ref in cell.references:
            nt = Transform(ref).t

            self._traverse(ref.ref_cell, t @ nt)

    def traverseAll(self):

        for top in self.lib.top_level():
            self._traverse(top, Transform.identity())
