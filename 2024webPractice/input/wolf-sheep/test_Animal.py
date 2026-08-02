import unittest
from Vector import Vector
import Animal
import Grid
import math


class TC1(unittest.TestCase):


    def test_chase(self):
        max_scope = 1000
        align_dist = 60
        chase_dist = 100
        caught_dist = 5
        const_speed = 2
        delta_t = 1

        Alignment_Grid = Grid.Grid(align_dist, max_scope)
        Chase_Grid = Grid.Grid(chase_dist, max_scope)

        positions = [Vector(250, 250, max_scope), Vector(260, 250, max_scope)]
        speed = [Vector(0, 0), Vector(0, 0)]



        Wolves: [Animal.Animal] = [Animal.Animal("wolf", 0, pos=positions[0], speed=speed[0], marker="D")]
        Sheep: [Animal.Animal] = [Animal.Animal("sheep", 1, pos=positions[1], speed=speed[1], marker="+")]
        Animals: [Animal.Animal] = [Sheep[0], Wolves[0]]

        Alignment_Grid.update_index(Animals)
        Chase_Grid.update_index(Animals)

        Wolves[0].set_grid(Alignment_Grid, Chase_Grid)
        Sheep[0].set_grid(Alignment_Grid, Chase_Grid)

        Wolves[0].update_speed_chase(chase_dist**2, caught_dist**2, 1)
        self.assertAlmostEqual(Wolves[0].chase_speed.x, 0.01, msg="w0 x speed")
        self.assertAlmostEqual(Wolves[0].chase_speed.y, 0, msg="w0 y speed")

        Sheep[0].update_speed_chase(chase_dist**2, caught_dist**2, 1)
        self.assertAlmostEqual(Sheep[0].chase_speed.x, 0.01, msg="s0 x speed")
        self.assertEqual(Sheep[0].chase_speed.y, 0, "s0 y speed")

        Wolves[0].move(delta_t, const_speed)
        self.assertEqual(Wolves[0].pos.x, 252)
        self.assertEqual(Wolves[0].pos.y, 250)

        Sheep[0].move(delta_t, const_speed)
        self.assertEqual(Sheep[0].pos.x, 262)
        self.assertEqual(Sheep[0].pos.y, 250)


if __name__ == '__main__':
    unittest.main()
