from bs4 import BeautifulSoup
import urllib.request
import sys

def load_page():
	with urllib.request.urlopen('http://www.wclc.com/winning-numbers/lotto-max-extra.htm') as response:
		html = response.read()


	soup = BeautifulSoup(html)

	draws = []

	for draw in soup.find_all(class_="pastWinNum"):

		nums=[]
		for num in draw.find_all(class_="pastWinNumber"):
			nums+=[num.get_text()]

		bonus = draw.find(class_="pastWinNumberBonus").get_text()

		maxs = []

		for maxmillion in draw.find_all(class_="pastWinNumbers"):
			ind_max=[]
			for num in maxmillion.find_all(class_="pastWinNumMM"):
				ind_max+=[num.get_text()]
			maxs +=[ind_max].sort()


		draws+=[{"date":draw.find(class_="pastWinNumDate").get_text().strip(),"numbers":nums, "bonus":bonus[5:], "maxs":maxs}]


	return draws

def pick_day(draws):
	print("Which date would you like?")
	print()
	x=1
	for draw in draws:
		print(str(x)+": "+draw['date'])
		print()
		x+=1

	n = int(input('?: '))

	return(draws[n-1])

def input_ticket():
	answer="n"
	ticket=[]

	while answer!="y":
		print("Type in your numbers: ")
		for i in range(7):
			ticket += [input()]

		print("Is this correct?")
		print(ticket)
		print("y/n?")
		answer = input()
		if answer == 'n':
			ticket=[]

	return ticket

def num_matches(ticket, draw):
	i=0
	for n in ticket:
		if n in draw['numbers']:
			i+=1

	return i

def has_bonus(ticket,draw):
	return(draw['bonus'] in ticket)

def check_max(ticket, draw):
	return ticket.sort() in draw['maxs']

def main():
	while True:
		draws = load_page()
		#draws = test
		draw = pick_day(draws)
		while True:
			ticket = input_ticket()

			if has_bonus(ticket, draw):
				b="got the bonus!"
			else:
				b="no bonus."

			print("You matched "+str(num_matches(ticket,draw))+ " numbers and "+b)
			print()
			if check_max(ticket, draw):
				print("But you won a MaxMillion!!")
			else:
				"Also, no MMs"

			if input('Check another number on the sameday? y/n:')=='n':
				break

		if input('Check another day? y/n:') == 'n':
			break