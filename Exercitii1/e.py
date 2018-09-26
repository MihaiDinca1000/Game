__author__ = 'Gigel'

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--muschi", help="activeaza toti muschii la 100%",
					action="store_true")
args = parser.parse_args()
if args.muschi:
	print("muschi activati !")