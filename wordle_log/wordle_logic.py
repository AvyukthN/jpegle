def get_yg(key: str, guess: str) -> list:
	g = []
	for i in range(len(key)):
		if key[i] == guess[i]:
			g.append(i)
	
	y = []
	for i in range(len(guess)):
		if (guess[i] in key) and (guess[i] != key[i]):
			y.append(i)

	final_arr = ["_" for _ in key]

	for idx in g:
		final_arr[idx] = "G"	
	for idx in y:
		final_arr[idx] = "Y"	

	return ' '.join(final_arr)


if __name__ == '__main__':
	key = "avyukth"
	guess = "htkuyva"

	yg = get_yg(key, guess)
	print(yg)	