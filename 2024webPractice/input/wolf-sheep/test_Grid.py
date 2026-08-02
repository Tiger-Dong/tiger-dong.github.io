import unittest
from Grid import Grid
import numpy as np
from Vector import Vector
from Animal import Animal


class GridTestCase(unittest.TestCase):
    def test_nearby_0(self):
        grid_size, max_scope = 1, 4
        pts = np.array([[0.4, 0.4], [0.4, 0.6], [0.6, 0.6], [0.6, 0.4]])
        expected_close = [0, 1, 5, 4]
        expected_nearyby = [{0, 1, 3, 4, 5, 7, 12, 13, 15},
                            {0, 1, 2, 4, 5, 6, 12, 13, 14},
                            {0, 1, 2, 4, 5, 6, 8, 9, 10},
                            {0, 1, 4, 5, 8, 9, 3, 7, 11}]
        self.run_case(grid_size, max_scope, pts, expected_close, expected_nearyby)

    def test_nearby_right_edge(self):
        grid_size, max_scope = 1, 4
        pts = np.array([[3.4, 0.4], [3.4, 0.6], [3.6, 0.6], [3.6, 0.4]])
        expected_close = [12, 13, 1, 0]
        expected_nearyby = [{8, 9, 12, 13, 0, 1, 11, 15, 3},
                            {8, 9, 10, 12, 13, 14, 0, 1, 2},
                            {0, 1, 2, 4, 5, 6, 12, 13, 14},
                            {0, 1, 3, 4, 5, 7, 12, 13, 15}]
        self.run_case(grid_size, max_scope, pts, expected_close, expected_nearyby)

    def test_up_left(self):
        grid_size, max_scope = 1, 4
        pts = np.array([[0.4, 3.4], [0.4, 3.6], [0.6, 3.6], [0.6, 3.4]])
        expected_close = [3, 0, 4, 7]
        expected_nearyby = [{2, 3, 0, 6, 7, 4, 14, 15, 12},
                            {0, 1, 3, 4, 5, 7, 12, 13, 15},
                            {0, 1, 4, 5, 8, 9, 3, 7, 11},
                            {2, 3, 0, 6, 7, 4, 10, 11, 8}]
        self.run_case(grid_size, max_scope, pts, expected_close, expected_nearyby)

    def test_up_right(self):
        grid_size, max_scope = 1, 4
        pts = np.array([[3.4, 3.4], [3.4, 3.6], [3.6, 3.6], [3.6, 3.4]])
        expected_close = [15, 12, 0, 3]
        expected_nearyby = [{10, 11, 14, 15, 2, 3, 8, 12, 0},
                            {8, 9, 12, 13, 0, 1, 11, 15, 3},
                            {0, 1, 3, 4, 5, 7, 12, 13, 15},
                            {2, 3, 0, 6, 7, 4, 14, 15, 12}]
        self.run_case(grid_size, max_scope, pts, expected_close, expected_nearyby)

    def test_bigger_up_right(self):
        grid_size, max_scope = 5, 20
        pts = np.array([[17, 17], [17, 19], [19, 19], [19, 17]])
        expected_close = [15, 12, 0, 3]
        expected_nearyby = [{10, 11, 14, 15, 2, 3, 8, 12, 0},
                            {8, 9, 12, 13, 0, 1, 11, 15, 3},
                            {0, 1, 3, 4, 5, 7, 12, 13, 15},
                            {2, 3, 0, 6, 7, 4, 14, 15, 12}]
        self.run_case(grid_size, max_scope, pts, expected_close, expected_nearyby)

    def test_on_middle_or_central(self):
        grid_size, max_scope = 4, 20
        pts = np.array([[2, 2], [2, 3], [3, 2], [1, 2]])
        expected_close = [0, 1, 5, 0]
        expected_nearyby = [{0, 1, 5, 6, 20, 21, 4, 9, 24},
                            {0, 1, 2, 5, 6, 7, 20, 21, 22},
                            {0, 1, 5, 6, 10, 11, 4, 9, 14},
                            {0, 1, 5, 6, 20, 21, 4, 9, 24}]
        self.run_case(grid_size, max_scope, pts, expected_close, expected_nearyby)

    def test_last_row_small_gap(self):
        grid_size, max_scope = 5, 22
        pts = np.array([[1, 1], [4, 21], [21, 2], [21, 3], [21,21]])
        expected_close = [0, 9, 20, 21, 24]
        expected_nearyby = [{0, 1, 3, 4, 5, 6, 8, 9, 15, 16, 18, 19, 20, 21, 23, 24},
                            {0, 1, 3, 4, 5, 6, 8, 9, 10, 11, 13, 14},
                            {0, 1, 3, 4, 5, 6, 8, 9, 15, 16, 18, 19, 20, 21, 23, 24},
                            {0, 1, 2, 5, 6, 7, 15, 16, 17, 20, 21, 22},
                            {0, 1, 3, 4, 5, 6, 8, 9, 15, 16, 18, 19, 20, 21, 23, 24},]
        self.run_case(grid_size, max_scope, pts, expected_close, expected_nearyby)

    def test_60_1000(self):
        grid_size, max_scope = 60, 1000
        pts = np.array([[250,250], [260, 250]])
        expected_close = {72, 72}
        expected_nearby = [{54, 55, 56, 71, 72, 73, 88, 89, 90},
                           {54, 55, 56, 71, 72, 73, 88, 89, 90}
        ]
        self.run_case(grid_size, max_scope, pts, expected_close, expected_nearby)

    def test_100_1000(self):
        grid_size, max_scope = 100, 1000
        pts = np.array([[250,250], [260, 250]])
        expected_close = {22, 32}
        expected_nearby = [{11, 12, 13, 21, 22, 23, 31, 32, 33},
                           {21, 22, 23, 31, 32, 33, 41, 42, 43},
        ]
        self.run_case(grid_size, max_scope, pts, expected_close, expected_nearby)

    def run_case(self, grid_size, max_scope, pts, expected_close, expected_nearyby):
        grid = Grid(grid_size, max_scope)
        Animals = []
        for idx, p in enumerate(pts):
            Animals.append(Animal("sheep", idx, pos=Vector(p[0], p[1])))
        grid.update_index(Animals)

        for a in Animals:
            self.assertEqual(grid.get_nearby_grids(a.id), expected_nearyby[a.id])


if __name__ == '__main__':
    unittest.main()
