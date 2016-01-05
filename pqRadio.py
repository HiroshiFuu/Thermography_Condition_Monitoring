import pygame
from pygame.locals import *
from threading import Timer
from math import pi as PI

BD_COLOR = (64,64,64)
BD_SHAD = (128,128,128)
BD_HIGH = (255,255,255)
BG_COLOR = (212,208,200)

class Radio():
	def __init__(self, parent, position, text, state):
		self.rect = pygame.Rect(position[0] - 6, position[1] - 6, 12, 12)
		self.parent = parent
		self.position = position
		self.text = text
		#Widget.__init__(self, parent, rect, style, state)
		self.clicked = state

	def get_clicked(self):
		return self.clicked
		
	def set_clicked(self, state):
		self.clicked = state
		
	def draw_text(self):
		myFont = pygame.font.SysFont("Calibri", 22)
		myText = myFont.render(self.text, 1, (255, 255, 255))
		self.parent.screen.blit(myText, (self.position[0] + 8, self.position[1] - 8))
		
	def draw_click(self):
		if self.get_clicked():
			pygame.draw.circle(self.parent.screen, (0, 0, 0), (self.position[0], self.position[1]), 2)

	def draw(self):
		self.draw_text()
		a = (PI / 4.0)
		pygame.draw.circle(self.parent.screen, (255, 255, 255), (self.position[0], self.position[1]), 5)
		pygame.draw.arc(self.parent.screen, BD_SHAD, ((self.position[0] - 6, self.position[1] - 6),(12,12)), a, 5 * a)
		pygame.draw.arc(self.parent.screen, BD_COLOR, ((self.position[0] - 5, self.position[1] - 5),(10,10)), a, 5 * a)
		pygame.draw.arc(self.parent.screen, BD_HIGH, ((self.position[0] - 6, self.position[1] - 6),(12,12)), 5 * a, 9 * a)
		pygame.draw.arc(self.parent.screen, BG_COLOR, ((self.position[0] - 5, self.position[1] - 5),(10,10)), 5 * a, 9 * a)
		self.draw_click()

	def pressed(self, mouse):
		if mouse[0] > self.rect.topleft[0]:
			if mouse[1] > self.rect.topleft[1]:
				if mouse[0] < self.rect.bottomright[0]:
					if mouse[1] < self.rect.bottomright[1]:
						if not self.get_clicked():
							self.clicked = True
							#print self.get_clicked()
							return True
						else: return False
					else: return False
				else: return False
			else: return False
		else: return False

class RadioGroup(Radio):
	def __init__(self):
		self.radios = []
	
	def add(self, radio):
		self.radios.append(radio)
		
	def check(self, mouse):
		for i in range(0, 3):
			radio = self.radios[i]
			if radio.pressed(mouse):
				for r in self.radios:
					if not r == radio:
						r.set_clicked(False)
						r.draw_click()
				return i
		return -1
