import random

r = random.randint
print 'RESTART'
def bombe():
	for I in range(5):
		d = r(1, 10)
		print ' - dif : ' + str(d)
		for i in range(5):
			level = r(0,(d / 2) * 3) # Bon pour les BOMBES
			print ' - - level : ' + str(level)

def time(max=10):
	for i in range(max):
		i += 1
		v = i - 5
		if v < 0:
			v = 0 
		horloge = r(0 + (max / 2 - i), (max - i))
		# horloge = 10 - i
		if horloge < 0:
			horloge = 0
		print i, ':', horloge

def makeBigger(max=10):
	for difficulte in range(max):
		difficulte += 1
		difficulte -= 1

		plusGros = r(-difficulte, max / 3)
		if plusGros < 0:
			plusGros = 0
		if plusGros > 1:
			plusGros = 1
		print difficulte, ': entre', -difficulte, 'et', max / 2, '->', plusGros

makeBigger()
