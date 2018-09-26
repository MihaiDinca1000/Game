import argparse


if __name__ == "__main__":

	par = argparse.ArgumentParser(description="Sound tools")
	par.add_argument("-n1", "--number1",type=int, help="first number")
	par.add_argument("-n2", "--number2",type=int, help="second number")
	par.add_argument("-op", "--operation", help="operatie")

	args = par.parse_args()

	n1= args.number1
	n2= args.number2

	result = None  
	if args.operation == "add":
		result = n1+n2
	elif args.operation == "sub":
		result = n1-n2
	elif args.operation == "mul":
		result = n1*n2
	else:
		print("nu exista operatia asta ")		
	print(result)	
