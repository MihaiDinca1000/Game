__author__ = 'Mihai Dincă'

import os
from shutil import *
import argparse
from pathlib import Path



if __name__ == "__main__":

	var1 = ""
	var2 = ""
	source_file = "X:/MSRE/Ref/MSRE_10.2.0/install"
	
	destination_file = ''

	########################################################################################################
	pars = argparse.ArgumentParser(prog='copy dirs script', description="à copier MSRE localment:",
	                               epilog="Comme ça on copie les repertoires")

	pars.add_argument("-o", "--output", default = destination_file,
	                       help="the destination dirctory is the curently working dirctory")
	pars.add_argument("-a", "--arch",  default="all", type = lambda s : s.lower(),nargs="?", 
	                       const="all", help="Targeted check architecture: 32b, 64b, All")
	pars.add_argument("-p", "--platform",  default="all", type = lambda s : s.lower(),nargs="?", 
	                	   const="all", help="Targeted check platform: Windows, Linux, All")
	args = pars.parse_args()

	#############il faut introduir la destination a la main lorsque vous lancez le script###################	
	destination_file = args.output

	##################################### Aficher les arguments ############################################

	print(args)
	print('\n')

	########################################################################################################
	# 9 cas possibles:
	if args.arch == 'all' and args.platform == 'all':
		var1 = ''
		var2 = ''
	elif args.arch == 'all' and args.platform == 'linux':
		var1 = ''
		var2 = 'windows'
	elif args.arch == 'all' and args.platform == 'windows':
		var1 = ''
		var2 = 'linux'
	elif args.arch == 'i386' and args.platform == 'all':
		var1 = 'x86_64'
		var2 = ''
	elif args.arch == 'i386' and args.platform == 'linux':
		var1 = 'x86_64'
		var2 = 'windows'
	elif args.arch == 'i386' and args.platform == 'windows':
		var1 = 'x86_64'
		var2 = 'linux'
	elif args.arch == 'x86_64' and args.platform == 'all':
		var1 = 'i386'
		var2 = ''
	elif args.arch == 'x86_64' and args.platform == 'linux':
		var1 = 'i386'
		var2 = 'windows'	
	elif args.arch == 'x86_64' and args.platform == 'windows':
		var1 = 'i386'
		var2 = 'linux'	
	else:
		print("an error has occurred")


	########################################################################################################
	# Le programme va ignorer les fichiers suivantes(des extensionsm des repertoires, et des variables comme "va1", "var2"):  
	ignoreP =ignore_patterns(
	    "conf", "inc", "java", "VERSION", "*.ini", "*.ksh",
	    "Maestro", "maestro", "*.sh", "libSL.so", "libOP.so", "libnucleus.so",
	    "libims_Vistas.so", "libGenVistasModel.so", "libGEN_FDEF.so",
	    "libDRB.so", "libdecibel.so", "libCodec.so", "libDRB.a",
	    "libCodecStatic.a", "*.bat", "*.vbs", "zlib1.dll", "SL.dll",
	    "libxml2.dll", "libwinpthread-1.dll", "libstdc++-6.dll",
	    "libOP.dll", "libnucleus.dll", "libims_Vistas.dll", "libgcc_s_dw2-1.dll",
	    "iconv.dll", "GenVistasModel.dll", "GEN_FDEF.dll", "DRB.dll",
	    "decibel.dll", "Codec.dll", "libSL.dll.a", "libDRB.dll.a",
	    "libdecibel.dll.a", "libCodec.dll.a", "DRB.lib", "CodecStatic.lib", "Readme.txt",
	     var1, var2)
	# ignore_patterns c'est un parametre de la "copytree" qui est une factory fonction

	print('\n')
	print("la source c'est: ",source_file)
	print("la destination c'est: ",destination_file)
	print('\n')

	########################################################################################################
	copytree(source_file, destination_file, ignore=ignoreP)

	print("  ,---.           ,--.          ,--. ") 
	print(" /  O  \ ,--.--.,-'  '-. ,--,--.|  | ") 
	print("|  .-.  ||  .--''-.  .-'' ,-.  ||  | ") 
	print("|  | |  ||  |     |  |  \ '-'  ||  | ") 
	print("`--' `--'`--'     `--'   `--`--'`--' ")
