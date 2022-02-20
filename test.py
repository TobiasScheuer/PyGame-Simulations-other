import random
import time

def main():
	selfimage_index = 2
	target_position = 7
	positions = [1,2,3,4,5,6,7,8]       # 1,2,x,4,5,6,7,8                 # 1,2,3,4,5,6,x
	target_index = positions.index(target_position)
	newindex = None
	left_half = positions[0:target_index]
	right_half = positions[target_index+1:]
	while len(left_half) < 4:
		left_half.append(right_half[-1])
		right_half.pop()
	while len(right_half) < 3:
		right_half.append(left_half[0])
		left_half.pop(0)
	print(left_half)
	print(right_half)
	while newindex != target_position:
		print(newindex)
		if selfimage_index in left_half:
			newindex = selfimage_index + 1
		elif selfimage_index in right_half:
			newindex = selfimage_index - 1
		if newindex == 9 or newindex == 0:
			if target_position <= 5:
				newindex = 1
			else:
				newindex = 8
		print(newindex)
		selfimage_index = newindex
		time.sleep(1)
		



	


if __name__ == "__main__":
	main()