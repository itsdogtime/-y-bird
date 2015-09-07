#!/usr/bin/env python

# (c) Cameron Bland
# http://github.com/itsdogtime/-y-bird

import os
import sys
from random import randint
from time import sleep
import curses

if sys.version_info.major >= 3:
	xrange = range

class CursesScreen():
	def __enter__(self):
		self.stdscr = curses.initscr()
		curses.cbreak()
		curses.noecho()
		self.stdscr.keypad(1)
		self.stdscr.nodelay(1)
		return self.stdscr

	def __exit__(self,a,b,c):
		curses.nocbreak()
		self.stdscr.keypad(0)
		stdscr.clear()
		stdscr.refresh()
		curses.echo()
		curses.endwin()

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

		self.y += self.vel

	def flap(self):
		self.vel = -3

	def gravity(self):
		self.vel += 1

class Walls():
	def __init__(self,res,player_x):
		self.res = res
		self.tile = "|"
		self.space_size = 15
		self.hole_size = 2
		self.edge_buffer = 2 + self.hole_size
		self.generate_walls(player_x)
		self.step = 0

	def __getitem__(self,i):
		return self.walls[i]

	def generate_wall(self):
		return randint(self.edge_buffer,self.res["h"]-self.edge_buffer)

	def generate_walls(self,p_x): # sets self.walls as list of ints. the list[pos] is the wall itself, the number is height of the hole
		self.walls = [self.generate_wall() if x % self.space_size == 0 and x > p_x + self.space_size else 0 for x in xrange(0,self.res["w"])]

	def update(self):
		self.step += 1
		self.walls.pop(0)

		if self.step >= self.space_size:
			self.walls.append(self.generate_wall())
			self.step = 0
		else:
			self.walls.append(0)

def get_res():
	h,w = stdscr.getmaxyx()
	return {"w" : w, "h": h}


def draw_map(res, player, walls):

	mapstring = []

	for y in xrange(res['h']):
		for x in xrange(res['w']):

			if y == res['h'] - 1 and x == res['w'] - 1: 
				break # Do not write to last character in screen or curses will abort (ERR)
			if x == 2 and y == res['h'] / 2:
				mapstring.append("Score: %03d" % player.score) # print the score
			elif x > 2 and x < 12 and y == res['h'] / 2: #don't print 9 chars to account for adding 10 in the score
				pass
			elif player.x == x and player.y == y:
				mapstring.append(player.tile)
			elif walls[x]:
				if y < walls[x] - walls.hole_size or y > walls[x] + walls.hole_size:
					mapstring.append(walls.tile)
				else:
					mapstring.append(' ')
			else:
				mapstring.append(' ')

	return "".join(mapstring)


def collision_detect(player,walls):
	collision = False
	if walls[player.x]: # only check on non-zero value (a wall)
		if player.y < walls[player.x] - walls.hole_size or player.y > walls[player.x] + walls.hole_size:
			collision = True # if player is not in walls.hole_size
		else:
			player.score += 1
	return collision


def main_loop(fps):
	player = Player()
	res = get_res()
	walls = Walls(res,player.x)


	while True:

		p_input = stdscr.getch()

		if p_input == ord('q') or p_input == ord('Q'):
			exit(0)
		elif p_input == ord('r') or p_input == ord('R'):
			player = Player()
			walls = Walls(res,player.x)
		elif p_input == ord(' '):
			player.move(True)
		else:
			player.move(False)

		if not player.dead:
			walls.update()
			player.dead = collision_detect(player,walls)
			frame = draw_map(res, player, walls)
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
	with CursesScreen() as stdscr:
		fps = .1
		curses.wrapper(main_loop(fps))