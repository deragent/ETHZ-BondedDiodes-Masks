import argparse
import os

from .BRNC_Run1_202003 import main

parser = argparse.ArgumentParser(description='Create the mask layout for the BRNC Run-1 [202003] - N-Side.')
parser.add_argument('-o', '--output', required=True,
                    help='Name of the output file.')
parser.add_argument('-e', '--export', default=None,
                    help='Flag to export the fabrication mask layers into individual files.')

args = parser.parse_args()

# Add the additional side argument
args.side = "N"

# Call the BRNC_202003 main function
main(args)
