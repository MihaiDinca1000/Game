import argparse
import os

par = argparse.ArgumentParser(description="write text into a file")
#  defineste argumente
par.add_argument('file',type=str, help='the file to store the text in')
par.add_argument('text',type=str, help='the text to write to the file')

args = par .parse_args()

print("writing to {}".format(args.file))
print ("\t{}".format(args.text))
 
fileToOpen = open(args.file, 'w') 
fileToOpen.write(args.text) 



# for i in args.integers:
# 	print()






# par.add_argument("--sound", action="store_true", help="that turnes on the sound")
# par.add_argument("-v","--volume", action="store_true", help="that turnes on the volume")
# args = par.parse_args()
# if args.sound:
# 	print("sound turned on !")
# else:
# 	print("volume turned on !")	


