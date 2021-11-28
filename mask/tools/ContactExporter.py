import gdspy

import re
import numpy as np

from .LibIterator import LibIterator, Transform

class ContactExporter(LibIterator):

    def __init__(self, lib):
        super().__init__(lib)

        self.devices = {}

        self.contact_data = {}

        self.reference_name = None
        self.sort_func = None

    def contacts(self, filter, points):
        self.contact_data[filter] = points

    def reference(self, name):
        self.reference_name = name

    def sort(self, func):
        self.sort_func = func

    def _exec(self, name, cell, t):
        self.devices[name] = t

    def generate(self):
        self.traverseAll()

        # Apply custom reference (0,0) device location
        if self.reference_name is not None:
            ref_point = self.devices[self.reference_name].apply([0,0])
        else:
            ref_point = np.zeros(2)

        # Reorder devices if sort is given
        keys = list(self.devices.keys())
        if callable(self.sort_func):
            keys.sort(key=self.sort_func)

        for key in keys:
            transform = self.devices[key]

            for filter, contacts in self.contact_data.items():

                if re.search(filter, key):
                    for suffix, value in contacts.items():

                        contact_pos = transform.apply(value) - ref_point
                        # TODO: For now just print to stdout
                        print("%i, %i, %s%s"%(contact_pos[0], contact_pos[1], key, suffix))
