import numpy as np


tups = [(0, 1, 2),
		(3, 4, 5),
		(6, 7, 8),
		(0, 3, 6),
		(1, 4, 7),
		(2, 5, 8),
		(0, 4, 8),
		(2, 4, 6)]

check_win_hash = dict()

def check_win(b):
	"""
	Returns 3 if X wins, -3 if O wins, 0 if undecided
	"""
	val = check_win_hash.get(tuple(b), None)
	if val:
		return val
	else:
		for t in tups:
			if all(b[i] == 'X' for i in t):
				check_win_hash[tuple(b)] = 3
				return 3
			elif all(b[i] == 'O' for i in t):
				check_win_hash[tuple(b)] = -3
				return -3
	check_win_hash[tuple(b)] = 0
	return 0

class Player:

	@staticmethod
	def possible_moves(b):
		return [i for i, n in enumerate(b) if n == ' ']

	def __init__(self, p):
		self.p = p

	def move(self, b):
		"""
		Returns position of move to play.
		Should not modify board state.
		"""
		pass

class RandomPlayer(Player):

	def move(self, b):
		return np.random.choice(Player.possible_moves(b))

class PerfectPlayer(Player):

	def move(self, b):
		pmoves = Player.possible_moves(b)
		gmoves = []
		for m in pmoves:
			n = b.copy()
			n[m] = self.p
			val = self.minimax(n, 10, ('O' if self.p == 'X' else 'X'))
			if val == 3 * (1 if self.p == 'X' else -1):
				return m
			elif val == 0:
				gmoves.append(m)
		return np.random.choice(gmoves)

	def minimax(self, node, depth, p):
		val = check_win(node)
		pmoves = Player.possible_moves(node)
		if len(pmoves) == 0 or depth == 0 or val != 0:
			return val
		if p == 'X':
			val = -3
			for m in pmoves:
				n = node.copy()
				n[m] = 'X'
				val = max(val, self.minimax(n, depth - 1, 'O'))
			return val
		else:
			val = 3
			for m in pmoves:
				n = node.copy()
				n[m] = 'O'
				val = min(val, self.minimax(n, depth - 1, 'X'))
			return val


def print_board(b):
	for i in range(0, 9, 3):
		print('|{}|{}|{}|'.format(*b[i:i + 3]))



if __name__ == '__main__':
	

	iboard = [str(i) for i in range(9)]
	board = [' ' for i in range(9)]
	print_board(iboard)
	print()
	print_board(board)
	l = ['X', 'O']
	print('c: Play vs Computer')
	print('h: 2 Humans')
	c = input('> ').lower()
	if c == 'c':
		print('0: Play as X')
		print('1: Play as O')
		p = int(input('> '))
		computer = PerfectPlayer(l[(p + 1) % 2])
		for i in range(9):
			if i % 2 == p:
				print('Your move.')
				while True:
					try:
						n = int(input('> '))
					except ValueError:
						print('Not a valid position. Try again.')
						continue
					if n < 9 and n >= 0 and board[n] == ' ':
						break
					print('Invalid square!')
			else:
				n = computer.move(board)
				print("Computer's move.")
				print('> {}'.format(n))
			board[n] = l[i % 2]
			print_board(board)
			if check_win(board) == 3 * ((((i + 1) % 2) * 2) - 1):
				print('Player {} wins!'.format(l[i % 2]))
				exit(0)
		print("It's a draw!")
	elif c == 'h':
		for i in range(9):
			while True:
				try:
					n = int(input('> '))
				except ValueError:
					print('Not a valid position. Try again.')
					continue
				if n < 9 and n >= 0 and board[n] == ' ':
					break
				print('Invalid square!')
			board[n] = l[i % 2]
			print_board(board)
			if check_win(board) == 3 * ((((i + 1) % 2) * 2) - 1):
				print('Player {} wins!'.format(l[i % 2]))
				exit(0)
		print("It's a draw!")
		

