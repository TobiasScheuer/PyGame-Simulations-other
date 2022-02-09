import random

def main():
	newlist = [0,1,2,3,4,5,6,7,8]
	print(newlist)
	for i,entry in enumerate(newlist):
		print(i)
		if i == 3:
			newlist.pop(3)
		if i == 5:
			newlist.pop(5-1)
		print(newlist)


	


if __name__ == "__main__":
	main()