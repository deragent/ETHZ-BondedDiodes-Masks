import gdspy

class Generator():

    def bbox(self):
        raise NotImplementedError

    def instance(self):
        raise NotImplementedError

    def retract(self):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError

    def width(self):
        bbox = self.bbox()
        return bbox[1,0] - bbox[0,0]

    def height(self):
        bbox = self.bbox()
        return bbox[1,1] - bbox[0,1]


class ReferenceGenerator(Generator):

    def __init__(self, devices):

        if type(devices) == type([]):
            self.devices = devices
        else:
            self.devices = [devices]

        self.n_devices = len(self.devices)

        self.reset()

    def reset(self):
        self.index = 0

    def bbox(self):
        if len(self.devices) < 1:
            return None

        common = self.devices[0].get_bounding_box()
        for dev in self.devices[1:]:
            bbox = dev.get_bounding_box()

            common[0,0] = min(common[0,0], bbox[0,0])
            common[0,1] = min(common[0,1], bbox[0,1])
            common[1,0] = max(common[1,0], bbox[1,0])
            common[1,1] = max(common[1,1], bbox[1,1])

        return common

    def instance(self):
        ref = gdspy.CellReference(self.devices[self.index])

        self.index = (self.index + 1)%self.n_devices

        return ref

    def retract(self):
        self.index = (self.index + (self.n_devices - 1))%self.n_devices


class CallbackGenerator(Generator):

    def __init__(self, callback):
        self.callback = callback

        self.count = 0

        self.cells = []

        self.reset()

    def reset(self):
        self.index = 0

    def bbox(self):
        ref = self.instance()
        bbox = ref.get_bounding_box()
        self.retract()

        return bbox

    def instance(self):
        cell = self.callback(self.count, self.index)
        ref = gdspy.CellReference(cell)

        self.cells.append(cell)

        self.index += 1
        self.count += 1

        return ref

    def retract(self):
        self.index -= 1
        self.count -= 1

        self.cells.pop()

    def addCellsToLib(self, lib):
        for cell in self.cells:
            lib.add(cell)
