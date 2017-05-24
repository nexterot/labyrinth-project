# -*- coding: utf-8 -*-


"""

Модуль, содержащий классы, описывающие игровые клетки и поле

"""


class Field:
    """ 
    Класс, реализующий логику игровой клетки на поле
    """
    def __init__(self, game, identity, coordinates):
        self.game = game
        self.obj = None
        self.id = identity
        self.coordinates = coordinates
        self.has_treasure = False

    def delete_object(self):
        self.obj = None


class Grass(Field):
    """ 
    Класс, реализующий логику пустой игровой клетки.
    На ней может располагаться клад
    """
    def __init__(self, game, identity, coordinates, obj):
        Field.__init__(self, game, identity, coordinates)
        self.obj = obj
        self.pair = None  # for teleports
        self.exit = False
        self.concrete = False

    def update(self):
        pass

    def delete_object(self):
        self.obj = None


class Water(Field):
    """ 
    Класс, реализующий логику игровой клетки - части реки
    """
    def __init__(self, game, identity, coordinates):
        Field.__init__(self, game, identity, coordinates)


class Wall(Field):
    """ 
    Класс, реализующий логику игровой клетки - стены
    Стена может быть нерушимой - поле indestructible
    """
    def __init__(self, game, identity, coordinates):
        Field.__init__(self, game, identity, coordinates)
        self.indestructible = False


class FieldGroup:
    """ 
    Класс, реализующий логику контейнера игровых клеток - игрового поля
    """
    def __init__(self):
        self.sprites = []
        self.dim = None

    def add(self, field):
        self.sprites.append(field)

    def at(self, coordinates):
        """ 
        Метод для получения объекта игровой клетки по ее координатам
        coordinates - кортеж (x, y)
        """
        return self.sprites[coordinates[0] * self.dim + coordinates[1]]

    def by_id(self, identity):
        """ 
        Метод для получения объекта игровой клетки с номером identity
        Нумерация с 0 до Level.size**2
        """
        return self.sprites[identity]

    def add_teleport(self, tp_field) -> None:
        """ 
        Метод для нахождения пары для телепорта 41-43
        Вызывается при построении уровня в self.initialize_level()
        """
        for field in self.sprites:
            if isinstance(field, Grass) and field.obj == tp_field.obj:
                field.pair = tp_field
                tp_field.pair = field
                break
