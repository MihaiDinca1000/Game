
# inheritance !!!!!
# from Chef import Chef
# from ChineseChef import ChineseChef


# myChef = Chef()
# myChef.make_special_dish()

# myChineseChef= ChineseChef()
# myChineseChef.make_fried_rice()













# fonctions classes !!!!!!
# from Student import Student

# student1 = Student("El_Ano", "Business", 9.8, False)
# student2 = Student("Gogu_Pantofu", "arte", 6.5, True)

# print(student1.on_honor_roll())


#  joc cu intrebari !!!!!!
# from Question import Question

# question_prompts = [
# 	"Ce culoare au merele ?\n(a) rosu/verde\n(b) purple\n(c) orange\n\n",
# 	"Ce culaore au bananele ?\n(a) galben\n(b) magenta\n(c) blue\n\n",
# 	"Ce culoare au strugurii ?\n(a) galben\n(b) rosu\n(b) blue\n\n"
# ]


# questions = [
# 	Question(question_prompts[0], "a"),
# 	Question(question_prompts[1], "c"),
# 	Question(question_prompts[2], "b")
# ]

# def run_test(questions):
# 	score = 0
# 	for question in questions:
# 		answer = input(question.prompt)
# 		if answer == question.answer:
# 			score +=1
# 	print("you got "+str(score)+ "/" +str(len(questions))+ " correct")
	
# run_test(questions)			



# from Student import Student

# student1 = Student("Jim", "Business", 8.1, False)
# student2 = Student("Gogu", "arte", 2.5, True)

# print(student1.name)
# print(student1.gpa)





# import x
# print(x.roll_dice(10))

# files: 

# licenta = open("joe.txt", "a")
# licenta1 = open("index.html", "w")

# licenta.write("\namantu la femei")
# licenta1.write("<p>This is just some text</p>")


# licenta.close()
# licenta1.close()



# licenta = open("joe.txt", "r")

# print(licenta.readable())
# print(licenta.read())
# print(licenta.readline())  #prima linie
# print(licenta.readline())  #citeste a doua linie
# for nume in licenta.readlines():
# 	print(nume)
# print(licenta.readlines()[1])


'''
r = read
w = write
a = append
r+ =write and read
'''

'''
try exception
'''
# try:
# 	value = 10/0
# 	number = int(input("enter a number: "))
# 	print(number)
# except ZeroDivisionError as err:
# 	print(err)
# except ValueError:
# 	print("invalid input prostovane	")	








'''
transalator
'''
# def translate(fraza):
# 	translation = ""
# 	for letter in fraza:
# 		if letter in "AEIOUaeiou":
# 			translation = translation+"g"
# 				if letter.isupper():
# 					translation = translation+ "G"
# 				else:
# 				translation = translation+"g"	
# 		else:
# 			translation = translation+letter
# 	return translation
	
# print(translate(input("scrie o fraza: ")))				













# n = [
# 	[1,2,3],
# 	[4,5,6],
# 	[7,8,9],
# 	[0]
# ]

# for row in n:
# 	for col in row:
# 		print(col)
# print(n[0][0])


# def ridica_la_putere(baza,exponent):
# 	result = 1
# 	for i in range(exponent):
# 		result = result*baza
# 	return result	

# print(ridica_la_putere(2,5))



# f = ["gogu", "gigel", "john", "jim", "joe"]
# print(len(f))
# pentru i putem pune orice nume
# for i in f:
# 	print(i)
#sau 
# for i in range(len(f)):
# 	print(f[i])

















# s_word = "gigivandamme"
# guess = ""
# guess_count = 0
# guess_limit = 3
# out_of_guesses = False
# while guess != s_word and not(out_of_guesses):
# 	if guess_count<guess_limit:
# 		guess = input("enter guess: ")
# 		guess_count+=1
# 	else:
# 		out_of_guesses = True	

# if out_of_guesses:
# 	print("you lose")
# else:
# 	print("you win! ")

# i = 1
# while i<= 10:
# 	print(i)
# 	i+=1 

# monthConversion{
# 				"0": "ianuarie",
# 				1: "februarie",
# 				2: "martie",
# 				3: "aprilie",
# 				4: "mai",
# 				5: "iunie",
# 				6: "iulie",
# 				7: "august",
# 				8: "septembrie",
# 				9: "octombrie",
# 				10: "noembrie",
# 				11: "decembrie",
# }

# print(monthConversion.get(1))



# n1 = float(input("nr1:"))
# op = input("nr2:")
# n2 = float(input("nr3:"))

# if op == "+":
# 	print(n1+n2)
# elif op == "-":
# 	print(n1-n2)
# elif op == "/":
# 	print(n1/n2)
# elif op == "*":
# 	print(n1*n2)
# else:
# 	print("invalid operator")				




# def maxNum(n1,n2,n3):
# 	if n1>= n2 and n1>=n3:
# 		return n1
# 	elif n2>=n1 and n2>=n3:
# 		return n2
# 	else:
# 		return n3 
# print(maxNum(12,56,22))			

# tuple:
# coor = (4, 5)
# print(coor[0])

# n = [11,54,765,12,43]
# g = [12, "asd", False, 123, "123asfa"]
# a = ["asd", 123,"gigi", False,"gigi","adi"]
# print(aa)
# g.reverse()
# aa = a.copy()
# print(a.index("gigi"))
# g.append("creed")
# n.insert(1,2222)
# g.remove(123)
# a.clear()
# g.pop()

# print(n)
# print(g)
# print(a)

