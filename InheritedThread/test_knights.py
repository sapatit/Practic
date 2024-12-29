import unittest
from knights import Enemy

class TestEnemy(unittest.TestCase):
    def test_reduce_enemies(self):
        enemy = Enemy(100)
        remaining = enemy.reduce_enemies(10)
        self.assertEqual(remaining, 90)

    def test_reduce_enemies_below_zero(self):
        enemy = Enemy(10)
        remaining = enemy.reduce_enemies(20)
        self.assertEqual(remaining, 0)

if __name__ == '__main__':
    unittest.main()
