#!/usr/bin/env python

# (c) Cameron Bland
# http://github.com/itsdogtime/-y-bird

import os
from random import randint
from time import sleep
import curses

class Player():
	def __init__(self):
		self.tile = "@"
		self.x = 16
		self.y = 12
		self.vel = 0
		self.vcap = 3
		self.score = 0
		self.dead = False

	def move(self,flap):
		if flap:
			self.flap()
		else:
			self.gravity()
			if self.vcap > 3:
				self.vel = 3

		player.y += player.vel

	def flap(self):
		player.vel = -3

	def gravity(self):
		self.vel += 1

class Walls():
	def __init__(self):
		self.tile = "|"
		self.space_size = 15
		self.hole_size = 2
		self.edge_buffer = 2 + self.hole_size
		self.walls = []
		self.generate_walls()

		# Check how far into space_size we should be initially
		self.step = 0
		for i in self.walls[::-1]:
			if i:
				break
			self.step += 1

	def __getitem__(self,i):
		return self.walls[i]

	def generate_walls(self): # returns a list of ints. the list[pos] is the wall itself, the number is the hole
		self.walls = [randint(2,res["h"]-self.edge_buffer) if x % self.space_size == 0 else 0 for x in xrange(0,res["w"])]

	def increment_walls(self):
		self.step += 1
		self.walls.pop(0)

		if self.step == self.space_size:
			self.walls.append(randint(self.edge_buffer,res["h"]-self.edge_buffer))
			self.step = 0
		else:
			self.walls.append(0)

def get_res():
	h,w = stdscr.getmaxyx()
	return {"w" : w, "h": h}

def build_map(res):
	line = [" " for x in xrange(res["w"])]
	cmap = [line for x in xrange(res["h"])]
	return cmap

def print_map(cmap, walls):
	max_height = len(cmap)
	max_width = len(cmap[0])

	mapstring = []

	for i_y,y in enumerate(cmap): # iter over y
		for i_x,x in enumerate(y):# iter over x

			if i_y == max_height - 1 and i_x == max_width - 1: 
				break # Do not write to last character in screen or curses will abort (ERR)

			if i_x == 2 and i_y == 12:
				mapstring.append("Score: %03d" % player.score) # print the score
			elif i_x > 2 and i_x < 12 and i_y == 12: #don't print 9 chars to account for adding 10 in 1 iter
				pass
			elif player.x == i_x and player.y == i_y:
				mapstring.append(player.tile)
			elif walls[i_x]:
				if i_y < walls[i_x] - walls.hole_size or i_y > walls[i_x] + walls.hole_size:
					mapstring.append(walls.tile)
				else:
					mapstring.append(x)
			else:
				# stdscr.addstr(x)
				mapstring.append(x)

	return "".join(mapstring)


def collision_detect():
	collision = False
	if walls[player.x]:
		if player.y < walls[player.x] - walls.hole_size or player.y > walls[player.x] + walls.hole_size:
			collision = True # if player is not in walls.hole_size
		else:
			player.score += 1
	return collision


def main(fps):
	global player
	global walls
	cmap = build_map(res)

	while True:

		p_input = stdscr.getch()

		if p_input == ord('q') or p_input == ord('Q'):
			stdscr.clear()
			stdscr.refresh()
			exit(0)
		elif p_input == ord('r') or p_input == ord('R'):
			player = Player()
			walls = Walls()
		elif p_input == ord(' '):
			player.move(True)
		else:
			player.move(False)

		if not player.dead:
			walls.increment_walls()
			player.dead = collision_detect()
			frame = print_map(cmap, walls)
		else:
			frame = ["Game Over. Thanks Obama.\n",
			"Final score = %03d\n"% player.score,
			"Press 'r' to reset.\n",
			"Press 'q' to quit."]
			frame = "".join(frame)

		stdscr.clear()
		stdscr.addstr(frame)
		stdscr.refresh()

		sleep(fps)


if __name__ == "__main__":

	stdscr = curses.initscr()
	stdscr.keypad(1)
	stdscr.nodelay(1)

	fps = .1
	res = get_res()
	walls = Walls()
	player = Player()
	main(fps)
