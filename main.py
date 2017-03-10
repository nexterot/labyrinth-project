import pygame, sys
from pygame.locals import *

class Colors:
	BLACK = (0,0,0)


class Images:
	background = pygame.image.load("sprites/background.png")
	wall = pygame.image.load("sprites/wall.png")
	weapons = pygame.image.load("sprites/weapons.png")
	mine = pygame.image.load("sprites/mine.png")
	teleport = pygame.image.load("sprites/teleport.png")
	teleport_2 = pygame.image.load("sprites/teleport_2.png")
	teleport_3 = pygame.image.load("sprites/teleport_3.png")
	bear = pygame.image.load("sprites/bear.png")
	hospital = pygame.image.load("sprites/aid.png")
	treasure = pygame.image.load("sprites/treasure.png")
	water = pygame.image.load("sprites/water.png")
	grass = pygame.image.load("sprites/grass.png")
	button_menu = pygame.image.load("sprites/button_menu.png")
	button_exit = pygame.image.load("sprites/button_exit.png")
	player_face = pygame.image.load("sprites/player_face.png")
	panel = pygame.image.load("sprites/panel.png")
	weapon_gun = pygame.image.load("sprites/weapon_gun.png")
	weapon_mine = pygame.image.load("sprites/weapon_mine.png")
	player = pygame.image.load("sprites/player.png")
	scale_health = pygame.image.load("sprites/scale_health.png")
	label_nick = pygame.image.load("sprites/label_nick.png")
	fog = pygame.image.load("sprites/fog.png")


class Player(pygame.sprite.Sprite):
	MAX_HEALTH = 3
	
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = Images.player
		self.rect = self.image.get_rect(topleft=(x,y))
		self.location = None
		self.vector = (0,0)
		self.health = Player.MAX_HEALTH
		
	def __vector_to(self, obj):
		shift_x, shift_y = map((lambda x,y: x-y), obj._id, self.location._id)
		return (shift_x, shift_y)
		
	def update(self):
		Game.surface.blit(self.image, self.rect)
		
	def go(self, field):
		field.visible = True
		if isinstance(field, Wall):
			self.vector = (0,0)
			return 
		if Game.bear.location == field:
			self.vector = self.__vector_to(field)
			Game.bear.attack(self)
			return
		self.move(field)
		if isinstance(field, Grass):
			if field.obj == "hospital":
				self.heal()
			elif field.obj == "mine":
				self.get_damage(3)
				field.delete_object()
			elif field.obj in ("tp1","tp2","tp3"):
				field.pair.visible = True
				self.teleport_from(field)
		# flow down (and left) the river
		elif isinstance(field, Water):
			vector = self.vector
			washed_away = False
			while not washed_away:
				next_water_down = Game.fields.at((field._id[0]+1, field._id[1]))
				next_water_left = Game.fields.at((field._id[0], field._id[1]-1))
				if isinstance(next_water_down, Water):
					self.move(next_water_down)
					next_water_down.visible = True
					field = next_water_down
				elif isinstance(next_water_left, Water):
					self.move(next_water_left)
					next_water_left.visible = True
					field = next_water_left
				else:
					washed_away = True
				field.visible = True
			self.vector = vector
				
	def move(self, field):
		self.vector = self.__vector_to(field)
		self.rect = field.rect
		self.location = field
		
	def teleport_from(self, field):
		self.rect = field.pair.rect
		self.location = field.pair
		
	def look(self, field):
		if self.can_look(field):
			field.visible = True
			self.vector = (0,0)
		
	def can_go(self, field):
		shift_x, shift_y = map((lambda x,y: x-y), field._id, self.location._id)
		return abs(shift_x)+abs(shift_y) == 1
		
	def can_look(self, field):
		shift_x, shift_y = map((lambda x,y: x-y), field._id, self.location._id)
		return abs(shift_x)|abs(shift_y) == 1

	def heal(self):
		self.health = Player.MAX_HEALTH;
		
	def get_damage(self, damage):
		self.health -= damage
		if self.health < 0: 
			self.health = 0
	
	def get_pushed(self, by_who):
		...
					
		
class FieldGroup(pygame.sprite.Group):
	teleports = pygame.sprite.Group()
	
	def at(self, _id) -> 'Field':
		for field in self.sprites():
			if field._id == _id:
				return field
				
	def at_coords(self, x, y) -> 'Field':
		for field in self.sprites():
			if field.rect.collidepoint(x,y):
				return field
		
	def update(self):
		for field in self.sprites():
			field.update()
			
	def add_teleport(self, tp_field):
		for field in self.sprites():
			if isinstance(field, Grass) and field.obj == tp_field.obj:
				field.pair = tp_field
				tp_field.pair = field
				break

		
class Field(pygame.sprite.Sprite):
	def __init__(self, x, y, _id=None):
		pygame.sprite.Sprite.__init__(self)
		self._id = _id
		self.visible = False
		self.fog_image = Images.fog
	
	def update(self):
		if self.visible:
			Game.surface.blit(self.image, self.rect)
		else:
			Game.surface.blit(self.fog_image, self.rect)
			
	def delete_object(self):
		self.obj = None
	
		
class Grass(Field):
	def __init__(self, x, y, obj=None, _id=None):
		Field.__init__(self, x,y, _id)
		self.obj = obj
		self.pair = None # for teleports
		if obj == "tp1":
			self.obj_image = Images.teleport
		elif obj == "tp2":
			self.obj_image = Images.teleport_2
		elif obj == "tp3":
			self.obj_image = Images.teleport_3
		elif obj == "hospital":
			self.obj_image = Images.hospital
		elif obj == "ammo":
			self.obj_image = Images.weapons
		elif obj == "mine":
			self.obj_image = Images.mine
		elif obj == "treasure":
			self.obj_image = Images.treasure
		
		self.image = Images.grass
		self.rect = self.image.get_rect(topleft=(x,y))
		
	def update(self):
		Field.update(self)
		if self.obj and self.visible:
			Game.surface.blit(self.obj_image, self.rect)
		

class Water(Field):
	def __init__(self, x, y, _id=None):
		Field.__init__(self, x, y, _id)
		self.image = Images.water
		self.rect = self.image.get_rect(topleft=(x,y))


class Wall(Field):
	def __init__(self, x, y, _id):
		Field.__init__(self, x, y, _id)
		self.image = Images.wall
		self.rect = self.image.get_rect(topleft=(x,y))


class Bear(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = Images.bear
		self.rect = self.image.get_rect(topleft=(x,y))
		self.location = None
		
	def attack(self, obj):
		obj.get_damage(2)
		obj.get_pushed(self)
		
	def update(self):
		if self.location.visible:
			Game.surface.blit(self.image, self.rect)
		
	def go(self):
		field = Game.fields.at((self.location._id[0]-Game.player.vector[0], 
								self.location._id[1]-Game.player.vector[1]))
		if not field or isinstance(field, Wall):
			return 
		elif isinstance(field, Grass) and field.obj in ("tp1","tp2","tp3"):
			self.move(field.pair)
			return
		elif isinstance(field, Grass) and field.obj == "mine":
			field.delete_object()
		if Game.player.location == field:
			self.attack(Game.player)
			return
		self.move(field)
		# flow down (and left) the river
		if isinstance(field, Water):
			washed_away = False
			while not washed_away:
				next_water_down = Game.fields.at((field._id[0]+1, field._id[1]))
				next_water_left = Game.fields.at((field._id[0], field._id[1]-1))
				if isinstance(next_water_down, Water):
					self.move(next_water_down)
					field = next_water_down
				elif isinstance(next_water_left, Water):
					self.move(next_water_left)
					field = next_water_left
				else:
					washed_away = True
					
	def move(self, field):
		self.rect = field.rect
		self.location = field


class Game:
	surface = None
	player = None
	bear = None
	fields = FieldGroup()
	clock = pygame.time.Clock()
	screen_size = (900,650)
	sprite_size = 50
	font = None
	
	@staticmethod
	def update():
		Game.fields.update()
		Game.player.update()
		Game.bear.update()
		
		Game.surface.blit(Images.scale_health, (30,365))
		Game.surface.blit(Game.font.render("{}".format(Game.player.health), 1, Colors.BLACK), (100,375))
		
	@staticmethod
	def render_interface():
		Game.surface.blit(Images.background, (0,0))
		Game.surface.blit(Images.player_face, (25,25))
		Game.surface.blit(Images.panel, (25,275))
		Game.surface.blit(Images.label_nick, (30,320))
		Game.surface.blit(Images.weapon_gun, (30,410))
		Game.surface.blit(Images.weapon_mine, (145,410))
		Game.surface.blit(Images.button_menu, (30,515))
		Game.surface.blit(Images.button_exit, (30,570))
		
	@staticmethod
	def initialize_level():
		for row in range(Level.size):
			for col in range(Level.size):
				_id = (row, col)
				x,y = 275 + col*Game.sprite_size, 25 + row*Game.sprite_size
				if Level.mask[row][col] == 1:
					Game.fields.add(Wall(x,y,_id))
				elif Level.mask[row][col] == 9:
					Game.fields.add(Water(x,y,_id))
				else:
					if Level.mask[row][col] == 0:
						Game.fields.add(Grass(x,y,_id=_id))
					elif Level.mask[row][col] == 2:
						g = Grass(x,y,_id=_id)
						g.visible = True
						Game.fields.add(g)
						Game.player = Player(x,y)
						Game.player.location = g
					elif Level.mask[row][col] == 3:
						Game.fields.add(Grass(x,y,obj="ammo",_id=_id))
					elif Level.mask[row][col] > 40:
						if Level.mask[row][col] == 41:
							tpX = "tp1"
						elif Level.mask[row][col] == 42:
							tpX = "tp2"
						elif Level.mask[row][col] == 43:
							tpX = "tp3"
						else:
							raise Exception("Error!")
						g = Grass(x,y,obj=tpX,_id=_id)
						Game.fields.add_teleport(g)
						Game.fields.add(g)
					elif Level.mask[row][col] == 5:
						g = Grass(x,y,_id=_id)
						Game.fields.add(g)
						Game.bear = Bear(x,y)
						Game.bear.location = g
					elif Level.mask[row][col] == 6:
						Game.fields.add(Grass(x,y,obj="treasure",_id=_id))
					elif Level.mask[row][col] == 7:
						Game.fields.add(Grass(x,y,obj="mine",_id=_id))
					elif Level.mask[row][col] == 8:
						Game.fields.add(Grass(x,y,obj="hospital",_id=_id))

	
class Level:
	size = 12
	# 0 - empty, 1 - wall, 2 - player, 3 - weapons, 41-43 - tp, 5 - bear, 6 - treasure, 7 - mine, 8 - aid, 9 - water
	mask = [[1,1,1,1,1,1,1,0,1,1,1,1],
			[1,3,0,0,0,0,1,0,1,42,0,1],
			[1,0,0,0,0,0,7,0,1,7,41,1],
			[1,1,1,1,1,0,0,0,1,1,1,1],
			[1,0,0,0,0,0,0,0,0,0,0,1],
			[1,0,0,5,0,1,0,2,0,7,0,0],
			[1,0,1,1,0,0,0,0,0,0,0,1],
			[1,0,41,1,0,0,9,1,1,1,1,1],
			[1,1,1,1,0,0,9,1,42,0,0,1],
			[1,7,0,0,0,8,9,1,0,0,0,1],
			[0,0,0,9,9,9,9,1,0,0,6,1],
			[1,1,1,1,1,1,1,1,1,1,1,1]]


def main():
	pygame.init()
	pygame.display.set_caption('python')
	Game.surface = pygame.display.set_mode(Game.screen_size)
	Game.font = pygame.font.SysFont("Arial", size=34)
	
	Game.render_interface()
	Game.initialize_level()
	
	player = Game.player
	bear = Game.bear
	while True: # main game loop
		Game.clock.tick(25) # 25 Frames per second
		for event in pygame.event.get():
			if event.type == MOUSEBUTTONDOWN:
				# move to field by pressing left mouse button
				if event.button == 1:
					field = Game.fields.at_coords(*event.pos)
					if field and player.can_go(field):
						player.go(field)
						# move bear just after player
						bear.go()
				# discover field by pressing right mouse button
				elif event.button == 3:
					field = Game.fields.at_coords(*event.pos)
					if field and Game.player.can_look(field):
						player.look(field)
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
				
		Game.update()	
		pygame.display.flip()

if __name__ == "__main__":
	main()
