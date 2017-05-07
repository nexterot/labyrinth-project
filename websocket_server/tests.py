import unittest

from game import Game, Player


class GameTest(unittest.TestCase):
    def setUp(self):
        self.game = Game([])

    def test_add_player(self):
        self.game.add_player("Nick")
        self.game.add_player("Mike")
        self.game.add_player("Alice")
        self.assertEqual(self.game.num_players, 3)


class PlayerTest(unittest.TestCase):
    def setUp(self):
        self.game = Game([])
        self.player = Player(self.game, "Alex")

    def test_get_damage(self):
        self.player.get_damage(1)
        self.assertEqual(self.player.health, 2)

    def test_heal(self):
        self.player.get_damage(3)
        self.player.heal()
        self.assertEqual(self.player.health, 3)


def main():
    suite_list = list()
    suite_list.append(unittest.defaultTestLoader.loadTestsFromTestCase(GameTest))
    suite_list.append(unittest.defaultTestLoader.loadTestsFromTestCase(PlayerTest))

    all_suites = unittest.TestSuite(suite_list)
    unittest.TextTestRunner().run(all_suites)

if __name__ == "__main__":
    main()