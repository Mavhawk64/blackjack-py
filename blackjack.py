import random
import sys

class Player(object):
	"""docstring for Player"""
	def __init__(self, hand,is_human=False):
		self.hand = hand
		self.is_human = is_human

	def __init__(self,is_human=False):
		self.hand = []
		self.is_human = is_human

	def draw(self):
		card = random.choice(DECK)
		self.hand.append(card)
		DECK.remove(card)
		return card

	def has(self, rank):
		for i in self.hand:
			if rank == i.rank:
				return True
		return False

	def value(self):
		s = 0
		
		# NO ACES

		if not self.has('A'):
			for i in self.hand:
				s += i.value()
			return s
		
		# ACES

		v = 0
		for i in self.hand:
			if i.value() != -1:
				s += i.value()
			else:
				v += 1
				s += 1
		
		# s = non-Ace cards' sum + amt(Aces) -- from which, we can continually add ten to until it is greater than or equal to 21

		for i in range(0,v):
			if s + 10 <= 21:
				s += 10
		return s

	def __str__(self):
		s = ""
		for i in self.hand:
			s += str(i) + ", "
		return s[:-2]

class Card(object):
	"""docstring for Card"""
	def __init__(self, suit, rank):
		self.suit = suit
		self.rank = rank
	
	def value(self):
		if self.rank == 'A':
			return -1
		elif self.rank in ['J','Q','K']:
			return 10
		return int(self.rank)
	
	def __str__(self):
		return self.rank + " of " + self.suit + "s"

def deal_hand(players,cpu):
	for i in range(0,2):
		for player in players:
			# Deal each player in
			player.draw()
		# Deal the Dealer in
		cpu.draw()

def print_all_hands(players,cpu):
	for i in range(0,len(players)):
		print(f"Human #{i+1}'s hand: " + players[i])
	print("Dealer's hand: " + cpu)

DECK = [Card('Club','A'),Card('Club','2'),Card('Club','3'),Card('Club','4'),Card('Club','5'),Card('Club','6'),Card('Club','7'),Card('Club','8'),Card('Club','9'),Card('Club','10'),Card('Club','J'),Card('Club','Q'),Card('Club','K'),Card('Diamond','A'),Card('Diamond','2'),Card('Diamond','3'),Card('Diamond','4'),Card('Diamond','5'),Card('Diamond','6'),Card('Diamond','7'),Card('Diamond','8'),Card('Diamond','9'),Card('Diamond','10'),Card('Diamond','J'),Card('Diamond','Q'),Card('Diamond','K'),Card('Spade','A'),Card('Spade','2'),Card('Spade','3'),Card('Spade','4'),Card('Spade','5'),Card('Spade','6'),Card('Spade','7'),Card('Spade','8'),Card('Spade','9'),Card('Spade','10'),Card('Spade','J'),Card('Spade','Q'),Card('Spade','K'),Card('Heart','A'),Card('Heart','2'),Card('Heart','3'),Card('Heart','4'),Card('Heart','5'),Card('Heart','6'),Card('Heart','7'),Card('Heart','8'),Card('Heart','9'),Card('Heart','10'),Card('Heart','J'),Card('Heart','Q'),Card('Heart','K')]

def main(human_count):
	humans = []
	for i in range(0,human_count):
		humans.append(Player(True))
	cpu = Player(False)
	deal_hand(humans,cpu)
	print(humans[0])

	# Check BlackJacks

	if cpu.value() == 21:
		print("Dealer got a BlackJack!")
		print_all_hands(humans,cpu)
		return
	for i in range(0,human_count):
		human = humans[i]
		if human.value() == 21:
			print(f"Human #{i+1} got a BlackJack!")
			print_all_hands(humans,cpu)
			return

	# Human(s) go(es) first

	for i in range(0,human_count):
		im_still_standing = False
		while not im_still_standing:
			im_still_standing = True
			human = humans[i]
			print(f"Human #{i+1}, your cards are",human)
			if human.value() > 21:
				print("That's a BUST!")
			elif human.value() == 21:
				print("That's 21!")
			else:
				p = int(input("Which of the following would you like to do?\n1. Hit\n2. Stand\n"))
				if p == 1:
					human.draw()
					im_still_standing = False

	# Dealer's turn

	while cpu.value() < 17:
		cpu.draw()

	# Calculate the scores and determine who won!

	scores = []

	# Humans' Scores

	for human in humans:
		scores.append(human)

	# Dealer's score
	
	scores.append(cpu)

	for i in range(0,human_count + 1):
		s = ""
		if i < human_count:
			s += f"Human #{i+1}"
		else:
			s += "Dealer"

		if scores[i].value() > 21:
			s += " BUSTED and"

		s += " had a hand of " + str(scores[i]) + " totaling " + str(scores[i].value())
		print(s)

	# Determine the winner(s)

	max_score = [-1,-1]

	for i in range(0,len(scores)):
		score = scores[i]
		if score.value() <= 21 and score.value() > max_score[0]:
			max_score = [score.value(), i]


	winners = [] # [[player,number],[player,number],...]

	for i in range(0,len(scores)):
		if scores[i].value() == max_score[0]:
			winners.append([scores[i],i+1])

	# Display the winners

	for winner in winners:
		if winner[0].is_human:
			print(f"Human #{winner[1]} Wins!")
		else:
			print("Dealer Wins!")

if __name__ == '__main__':
	x = 1
	try:
		x = int(sys.argv[1])
	except:
		pass
	if type(x) == type(1) and x > 0:
		print(f"There are {x} players and the dealer")
		main(x)