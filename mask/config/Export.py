import copy

class ExportSpecs():

    def __init__(self):

        self.exportlayers = {}
        self.alwayslayers = []

    def add(self, name, layer):
        if name not in self.exportlayers:
            self.exportlayers[name] = []
        self.exportlayers[name].append(layer["layer"])

    def always(self, layer):
        self.alwayslayers.append(layer["layer"])

    def __iter__(self):
        self.iter = iter(self.exportlayers)
        return self

    def __next__(self):
        try:
            key = next(self.iter)
        except IndexError:
            raise

        layers = copy.copy(self.alwayslayers)
        layers.extend(self.exportlayers[key])

        return key, layers
