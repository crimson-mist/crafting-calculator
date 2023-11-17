#!/usr/bin/env python3

import math
import string
import sys
from recipes import recipes

req_items = {}
intermediaries = {}
spares = {}
numwewant = 1

def update_intermediaries(input: str, update: int = 1):
	if not recipes[input]["base"]:
		if input in intermediaries:
			temp = intermediaries.pop(input, None) + update
			intermediaries[input] = temp
		else:
			intermediaries[input] = 1

def print_analytics(input):
	print()
	print(input)
	print(req_items)
	print(spares)

def _craft(input: str):
	update_intermediaries(input)

	if input not in recipes:
		print(f"Item not found: {input}")
		exit()

	if recipes[input]["base"]:
		if input in req_items:
			req_items[input] = req_items[input] + 1
			return False

		req_items[input] = 1
		return False

	if input in spares and spares[input]:
		spares[input] = spares[input] - 1
		return False

	for component in list(recipes[input]["subcomponents"]):
		successful_last_craft = False
		currentcomponentsneeded = recipes[input]["subcomponents"][component]
		if component in spares and spares[component]:
			if currentcomponentsneeded > spares[component]:
				currentcomponentsneeded = currentcomponentsneeded - spares[component]
				update_intermediaries(component, spares[component])
				spares[component] = 0
			else:
				update_intermediaries(component, currentcomponentsneeded)
				spares[component] = spares[component] - currentcomponentsneeded
				currentcomponentsneeded = 0

		for _ in range(math.ceil(currentcomponentsneeded / recipes[component]["quantity"])):
			if component in spares and spares[component]:
				spares[component] = spares[component] - 1
				continue
			successful_last_craft = _craft(component)
		if successful_last_craft and currentcomponentsneeded % recipes[component]["quantity"]:
			if component in spares:
				spares[component] = spares[component] + recipes[component]["quantity"] - currentcomponentsneeded % recipes[component]["quantity"]
			else:
				spares[component] =                     recipes[component]["quantity"] - currentcomponentsneeded % recipes[component]["quantity"]

	return True

def craft(input: str, num_crafts: int):
	for _ in range(num_crafts):
		_craft(input)

def main():
	if len(sys.argv) == 1:
		print("crafting_tree.py [number of desired crafts] [desired items to craft]")
		exit()

	if sys.argv[1][0] in string.digits:
		desired_num = int(sys.argv[1])

		desired_craft = " ".join(sys.argv[2:])
	else:
		desired_num = 1
		desired_craft = " ".join(sys.argv[1:])

	craft(desired_craft, desired_num)

	print(desired_num, f"{desired_craft}", ":", req_items, spares)
	print(intermediaries)

if __name__ == "__main__":
	main()
