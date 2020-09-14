import gdspy

import rich

import re
import sys

class HeidelbergLWFileCheck():

    def warn(self, str):
        if self._silent: return

        rich.print("[blue]Warning:[/blue]\t[grey]%s[/grey]"%(str))
        self.warnings += 1

    def error(self, str):
        if self._silent: return

        rich.print("[red]Error:[/red]\t\t[grey]%s[/grey]"%(str))
        self.errors += 1


    def __init__(self, silent=False):
        self.warnings = 0
        self.errors = 0

        self._silent = silent

    def check(self, file):

        lib = gdspy.GdsLibrary(infile=file)

        for top in lib.top_level():
            self._checkCellName(top.name)

            for cell in top.get_dependencies(recursive=True):
                self._checkCellName(cell.name)

        ## TODO: Add verification if centered around [0,0]

        ## TODO maybe: Check if all polygons are closed

        ## TODO maybe: Check if contains text which is not polygons

        return self.errors == 0


    def _checkCellName(self, name):

        if name.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
            self.warn("Cell name [%s] starts with a number."%name)

        leftover = re.sub(r'[0-9a-zA-Z_]', r'', name)
        if leftover != "":
            self.error("Cell name [%s] contains invalid characters: (%s)"%(name, leftover))


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description='Check a GDSII file for compliance with the Heidelberg DWL at BRNC.')
    parser.add_argument('file', help='The path to the file to be checked.')
    args = parser.parse_args()

    check = HeidelbergLWFileCheck()
    if not check.check(args.file):
        sys.exit(1)
    else:
        sys.exit(0)
