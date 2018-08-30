__author__ = 'Mihai Dincă'

import os
import shutil
import argparse
from pathlib import Path

def copydirectories(input_dir, output_dir, ignore_dir):
	if os.path.exists(output_dir): 
		dirlist = os.path.isdir(output_dir)
		if not dirlist:
		 
			os.rmdir(output_dir)
		else:
			shutil.rmtree(output_dir)
	shutil.copytree(input_dir, output_dir, ignore=ignore_dir)
	return 0 

if __name__ == "__main__":

	var1 = ""
	var2 = ""
	source_file = "D:/MSRE"
	
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
	 
	print("plateform ",args.platform)
	print("architecture ",args.arch)
	platform_dir = []
	if args.platform == "all" or args.platform == "":
		platform_dir = ["Windows" , "Linux"]
	else: 
		platform_dir = [args.platform[:1].upper() + args.platform[:1]]
		
		
	arch_dir = []
	
	if args.arch == "32b":
		arch_dir = ["i386"]
	if args.arch == "64b":
		arch_dir = ["x86_64"]
	if args.arch == "all" or args.arch == "":
		arch_dir = ["i386","x86_64"]
    
	#for i in range(len(platform_dir)): 
	#	for j in range(len(arch_dir)):
	#		print(platform_dir[i],arch_dir[j])
	
	ignoreP =shutil.ignore_patterns(
	    ".git","src","conf", "inc", "java", "VERSION")
	
	for i in range(len(platform_dir)): 
		for j in range(len(arch_dir)):
	 
			input_dir = source_file
			output_dir = destination_file
			input_dir+= os.sep + "install" + os.sep + platform_dir[i] + os.sep + arch_dir[j]
			output_dir += os.sep + "install" + os.sep + platform_dir[i] + os.sep + arch_dir[j]
			#print ("intput ",input_dir," output ",output_dir)
			copydirectories(input_dir, output_dir, ignoreP)
	
	print("copy done")
	