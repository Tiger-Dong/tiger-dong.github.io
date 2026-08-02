import unittest

import numpy as np

from Vector import Vector
import Config
import math

class MyTestCase(unittest.TestCase):
    def test_distance_in_periodic_map(self):
        self.assertEqual(5, Vector(0, 3).distance(Vector(4, 0)))
        v1 = Vector(1, 1, Config.MAP_SCOPE)
        v2 = Vector(Config.MAP_SCOPE - 2, Config.MAP_SCOPE - 3, Config.MAP_SCOPE)
        self.assertEqual(5, v1.distance(v2))

    def test_move(self):
        pos= Vector(10,10)
        speed = Vector(2, math.pi/2)
        pos.move(speed,1)
        self.assertEqual(pos.x,10)
        self.assertAlmostEqual(pos.y,12)

        pos = Vector(99, 0, 100)
        speed = Vector(10, 0)
        pos.move_angle_speed(speed, 1)
        self.assertEqual(pos.x, 9)
        self.assertEqual(pos.y,0)

        pos = Vector(10, 1, 100)
        speed = Vector(10, -math.pi/2)
        pos.move_angle_speed(speed, 1)
        self.assertEqual(pos.x, 10)
        self.assertEqual(pos.y, 91)

    def test_angle(self):
        p1 = Vector(Config.MAP_SCOPE -10, 20)
        p2 = Vector(2, 20)
        c1 = complex(12, 0)
        self.assertEqual(p1.angle_to_another(p2), np.angle(c1), "on the righ accross boder")
        c2 = complex(-12, 0)
        self.assertEqual(p2.angle_to_another(p1), np.angle(c2), "on the left accross border")

        p1 = Vector(10, 14, 100)
        p2 = Vector(10, 90, 100)
        c1 = complex(0, -24)
        self.assertEqual(p1.angle_to_another(p2), np.angle(c1))
        c2 = complex(0, 24)
        self.assertEqual(p2.angle_to_another(p1), np.angle(c2))


if __name__ == '__main__':
    unittest.main()
