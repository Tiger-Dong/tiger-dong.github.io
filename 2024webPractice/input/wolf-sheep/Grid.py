import math
from scipy import spatial
import numpy as np
# import Animal


class Grid:
    def __init__(self, grid_size=1, max_scope=10):
        self._grid_size = grid_size
        self._max_scope = max_scope
        self._row = math.ceil(max_scope * 1.0 / grid_size)
        self._col = self._row
        last_gap = max_scope % grid_size
        self.is_last_row_close_to_border = 0 < last_gap < grid_size / 2.0

        x, y = np.mgrid[0:(self._row), 0:(self._col)]
        self.ktree_data = list(zip(x.ravel() , y.ravel()))
        self._KDTree = spatial.KDTree(np.array(self.ktree_data) * grid_size)
        self.neighbors = self.init_neighbors()
        self.index_a2g = {}  # index animal -> grid
        self.index_g2a = {}  # index grid -> animal

    def init_neighbors(self):
        neighbors = {}
        for c, r in self.ktree_data:
            nearby_points = set()
            x, y = np.mgrid[-1:2, -1:2]
            for i_r, i_c in list(zip(x.ravel(), y.ravel())):
                new_r = (r + self._row + i_r) % self._row
                new_c = (c + self._col + i_c) % self._col
                nearby_points.add(int(new_c * self._row + new_r))

            if self.is_last_row_close_to_border:
                if c == 0:
                    new_c = self._col - 2
                elif c == self._col - 1:
                    new_c = 1
                for i in range(-1, 2):
                    temp_r = (r + self._row + i) % self._row
                    nearby_points.add(int(new_c * self._row + temp_r))

                if r == 0:
                    new_r = self._row - 2
                elif r == self._row - 1:
                    new_r = 1
                for i in range(-1, 2):
                    temp_c = (c + self._col + i) % self._col
                    nearby_points.add(int(temp_c * self._row + new_r))
                nearby_points.add(int(new_c * self._row + new_r))  # this is the corner of new added cell

            neighbors[int(c * self._row + r)] = nearby_points
        return neighbors

    def update_index(self, animals: []):
        pos = np.array([(s.pos.x, s.pos.y) for s in animals])
        _, nearby = self._KDTree.query(pos)
        self.index = {}
        for ani, idx in zip(animals, nearby):
            c = 0 if ani.pos.x - self._KDTree.data[idx][0] > self._grid_size / 2 \
                else idx // self._row
            r = 0 if ani.pos.y - self._KDTree.data[idx][1] > self._grid_size / 2 \
                else idx % self._row
            idx_1 = c * self._row + r
            self.index_a2g[ani.id] = idx_1
            if (idx_1, ani.type) in self.index_g2a:
                self.index_g2a[(idx_1, ani.type)].add(ani)
            else:
                self.index_g2a[(idx_1, ani.type)] = {ani}

    def get_nearby_grids(self, animal_id: int):
        return self.neighbors[self.index_a2g[animal_id]]

    def get_animals_neary(self, grid_idx: int, animal_type: str):
        return self.index_g2a.get((grid_idx, animal_type), set())
