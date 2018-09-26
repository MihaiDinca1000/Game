__author__ = 'Mihai Dinca'

import os
from shutil import *
import argparse


var1 = ""
var2 = ""
source_file = ""
destination_file = ""

pars = argparse.ArgumentParser(prog='copy dirs script', description="à copier MSRE localment:",
                               epilog="Comme ça on copie les repertoires")
pars.add_argument("-i", "--input", nargs="?", type = lambda s : s.lower(),
                       help="the source dirctory is /""X:/MSRE/Ref/MSRE_10.2.0/install")
pars.add_argument("-o", "--output", nargs="?", type = lambda s : s.lower(),
                       help="the destination dirctory is the curently working dirctory")
pars.add_argument("-a", "--arch", choices=("all", "i386", "x86_64"), type = lambda s : s.lower(),
                       help="Targeted check architecture: 32b, 64b, All")
pars.add_argument("-p", "--platform", choices=("all", "windows", "linux"), type = lambda s : s.lower(),
                       help="Targeted check platform: Windows, Linux, All")
args = pars.parse_args()

print(args)
print('\n')

if str(args.input) and str(args.output):
    source_file = "X:/MSRE/Ref/MSRE_10.2.0/install"
    destination_file = os.path.join(os.getcwd(), "MSRE_10.2.0/install_light")
else:
    print("wrog command !!! Please follow the help commands") # + pars.print_help()

print(args)
print('\n')

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
    "libdecibel.dll.a", "libCodec.dll.a", "DRB.lib", "CodecStatic.lib", "*.txt", var1, var2)

# print(str(ignoreP))

copytree(source_file, destination_file, ignore=ignoreP)

	print("  ,---.           ,--.          ,--. ") 
	print(" /  O  \ ,--.--.,-'  '-. ,--,--.|  | ") 
	print("|  .-.  ||  .--''-.  .-'' ,-.  ||  | ") 
	print("|  | |  ||  |     |  |  \ '-'  ||  | ") 
	print("`--' `--'`--'     `--'   `--`--'`--' ")