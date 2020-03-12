class LayerSpecs():

    def __init__(self):

        self.layers = {}
        self.default = {"layer": 0, "datatype": 0}

    def __setitem__(self, name, data):
        self.layers[name] = {"layer": data[0], "datatype": data[1]}

    def __getitem__(self, name):
        if name not in self.layers:
            print("WARNING: Layer [%s] not defined, using default values (%i, %i)"%(name, self.default["layer"], self.default["datatype"]))
            self.layers[name] = self.default

        return self.layers[name]
