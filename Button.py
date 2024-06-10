import pygame as p

class Button():
	def __init__(self, pos, text_input, font, base_color, hovering_color):
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		self.width = self.text.get_width()
		self.height = self.text.get_height()
		self.rect = p.Rect(self.x_pos - self.width/2, self.y_pos - self.height/2,self.width,self.height)

	def update(self, screen,position):
		if self.rect.collidepoint(position):
			p.draw.rect(screen, "Black" , self.rect )
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			p.draw.rect(screen, "White", self.rect)
			self.text = self.font.render(self.text_input, True, self.base_color)
		screen.blit(self.text, self.rect)

	def checkForInput(self, position):
		if self.rect.collidepoint(position):
			return True
		return False