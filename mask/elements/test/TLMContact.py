import gdspy
import math

from .. import Element

class TLMContact(Element):

    def __init__(self, parent, name,
        lengths,
        stripw=100, stripoverlap=50,
        contactw=1000, contactspacing=2540,
        overhang=10, layers=None, lib=None):

        self.lengths = lengths
        self.lengths.sort()

        self.overhang = overhang

        self.stripw = stripw
        self.stripoverlap = stripoverlap

        self.contactspacing = contactspacing
        self.contactw = contactw

        super().__init__(parent, name, layers, lib)

    def _addContact(self, x, y):
        oh = self.overhang
        cw = self.contactw

        contact = gdspy.Rectangle((x, y - oh), (x + cw + 2*oh, y + cw + oh), **self.layers["METALIZATION"])
        open = gdspy.Rectangle((x + oh, y), (x + cw + oh, y + cw), **self.layers["PASSIVATION_OPEN"])

        self.cell.add(contact)
        self.cell.add(open)


    def _addConnection(self, x, n, down=False):
        cs = self.contactspacing
        cw = self.contactw
        sw2 = self.stripw/2
        so = self.stripoverlap
        oh = self.overhang

        hw = 4*so

        v_dir = -1 if down else 1

        mid = ((cs/2 - cw/2)/2 + so/2)

        # First vertical path
        vert1 = gdspy.Rectangle((x, -sw2*v_dir), (x + so, v_dir*mid), **self.layers["METALIZATION"])
        self.cell.add(vert1)

        # Decide if horizontal path is necessary
        if x + so > n*cs + cw:
            h_dir = -1
            hw = max(hw, x + so - (n*cs + cw))
        elif x < n*cs:
            h_dir = +1
            hw = max(hw, n*cs - x)
        else:
            h_dir = 0

        if h_dir != 0:
            # Add horizontal path
            hor = gdspy.Rectangle((x + so/2*(1 - h_dir), v_dir*mid), (x + h_dir*hw + so/2*(1 - h_dir), v_dir*(mid + so)), **self.layers["METALIZATION"])
            self.cell.add(hor)

        # Second vertical path
        vert2 = gdspy.Rectangle((x + h_dir*hw, v_dir*mid), (x + h_dir*hw + so, v_dir*(cs/2 - cw/2 - oh)), **self.layers["METALIZATION"])
        self.cell.add(vert2)


    def construct(self):

        oh = self.overhang

        cs = self.contactspacing
        cw = self.contactw

        sw = self.stripw
        sw2 = self.stripw/2

        so = self.stripoverlap

        # Total length of the resistive strip
        maxl = max(self.lengths) + 2*so

        # Number of contact pairs
        ncontact = math.ceil(maxl / cs) + 1

        # Add the resistive strip
        strip = gdspy.Rectangle((-oh, -sw2), (maxl + oh, sw2), **self.layers["CONTACT_DOPING"])
        self.cell.add(strip)

        # Add the contact pairs
        for cc in range(0, ncontact):
            x = cc*(cs)
            self._addContact(x, cs/2 - cw/2)
            self._addContact(x, -cs/2 - cw/2)



        ## Contact connection for '0'
        contact_0 = gdspy.Rectangle((0, -sw2), (so, cs/2 - cw/2 - oh), **self.layers["METALIZATION"])
        self.cell.add(contact_0)

        ## Make all connections to contacts
        self.last_n = 0
        self.last_count = 1

        for l in self.lengths:
            n = math.ceil(l/cs - 1/2)
            x = l + so

            if self.last_n < n:
                self.last_n = n
                self.last_count = 1
            else:
                self.last_count += 1

            if self.last_count > 2:
                raise Exception('Can not place length [%i] on contact #%i\nContacts: %s'%(l, n, str(self.lengths)))

            self._addConnection(x, n, self.last_count > 1)
