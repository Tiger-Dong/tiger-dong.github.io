from __future__ import annotations
import numpy as np
import math
from functools import reduce
import Grid
from Config import Config
from Vector import Vector


class Animal:
    Distance_Map = {}

    def __init__(self, ani_type: str, _id: int, **kwargs):
        self.type: str = ani_type  # wolf or sheep
        self.chaser_type: str = "sheep" if (ani_type == "wolf") else "wolf"
        self.chase_direction: int = 1  # toward the target
        self.id: int = _id
        self.credit = 1
        self.alive: bool = True
        self.pos: Vector = kwargs["pos"]  # this is a vector, and must have, throw exception of not set
        self.speed: Vector = kwargs.get("speed", Vector(Config().INIT_SPEED, 0))  # this is a vector
        self.align_grid: Grid.Grid = None
        self.chase_grid: Grid.Grid = None
        self.align_speed: Vector = Vector(0, 0)
        self.repel_speed: Vector = Vector(0, 0)
        self.chase_speed: Vector = Vector(0, 0)
        self.omega = 0
        self.sight_2 = Config().RADIUS_SIGHT_SQUARE
        self.caught_2 = Config().RADIUS_CAUGHT_SQUARE
        self.step = 0  # for logging, in which step an action is taken
        self._check_speed(self.speed, "born")

    def set_step(self, i: int):
        self.step = i

    def square_distance(self, other):
        if self.id == other.id:
            return 0
        key = (min(self.id, other.id), max(self.id, other.id))
        if key not in Animal.Distance_Map:
            Animal.Distance_Map[key] = self.pos.square_distance(other.pos)
        return Animal.Distance_Map[key]

    def distance(self, other: Animal):
        return math.sqrt(self.square_distance(other))

    def get_nearby_herd(self):
        nearby_grids = self.align_grid.get_nearby_grids(self.id)
        raw_nearby_herd = set()
        for idx in nearby_grids:
            raw_nearby_herd = set.union(raw_nearby_herd, self.align_grid.get_animals_neary(idx, self.type))
        return [h for h in raw_nearby_herd
                if h.alive and self.square_distance(h) <= Config().RADIUS_ALIGNMENT_SQUARE]

    def update_speed_in_herd(self) -> list[Animal]:
        nearby_herd = self.get_nearby_herd()
        if len(nearby_herd) < 2:  # include itself, so at least 1
            return []
        avg_speed = np.mean([(h.speed.x * h.credit, h.speed.y * h.credit)
                             for h in nearby_herd], axis=0) * Config().ALPHA
        self.align_speed = Vector(avg_speed[0], avg_speed[1])
        self._check_speed(self.align_speed, "align", ids=[h.id for h in nearby_herd])
        return nearby_herd

    def update_speed_repel(self, nearby_herd, repel_dist_2=0):
        repel_dist_2 = Config().RADIUS_REPEL_SQUARE if repel_dist_2 == 0 else repel_dist_2
        repel_herd = [n for n in nearby_herd if self.id != n.id and
                      self.square_distance(n) <= repel_dist_2]
        if len(repel_herd) == 0:
            return
        for n in repel_herd:
            dist_2 = self.square_distance(n)
            if dist_2 < 0.81 * repel_dist_2:
                msg_str = Config().event_template.format(step=self.step, id=self.id,
                                                         msg=f"too close {n.id} {dist_2 ** 0.5}")
                Config().event_logger.warning(msg_str)
        self.repel_speed = self.forces_speed(Config().BETA, -1, repel_herd)
        self._check_speed(self.repel_speed, "repel", ids=[r.id for r in repel_herd])

    def get_chase_caught_heard(self) -> (list[Animal], list[Animal]):
        raw_chase_herd = set()
        nearby_grids = self.chase_grid.get_nearby_grids(self.id)
        for idx in nearby_grids:
            raw_chase_herd = set.union(raw_chase_herd, self.chase_grid.get_animals_neary(idx, self.chaser_type))
        chase_herd = [h for h in raw_chase_herd
                      if h.alive and self.square_distance(h) <= self.sight_2]
        caught_herd = [c for c in chase_herd if self.square_distance(c) <= self.caught_2]
        return chase_herd, caught_herd

    def handle_caught(self, chase_herd: list[Animal], caught_herd: list[Animal]):
        raise "not implemented"

    def continue_update_chase_speed(self, chase_herd, scalar: float):
        if not self.alive:
            return
        self.chase_speed = self.forces_speed(scalar, self.chase_direction, chase_herd)

    # set the default values in parameter to enable change it unit test
    def update_speed_chase(self):
        chase_herd, caught_herd = self.get_chase_caught_heard()
        if len(chase_herd) == 0:
            return
        if len(caught_herd) > 0:
            self._check_speed(self.chase_speed, "caught", ids=[c.id for c in caught_herd])
            self.handle_caught(chase_herd, caught_herd)
        if len(chase_herd) == 0:
            return
        self.continue_update_chase_speed(chase_herd, Config().Gamma)
        self._check_speed(self.chase_speed, "chase", ids=[c.id for c in chase_herd])

    def forces_speed(self, scalar: float, direction: int, herd: list[Animal]) -> Vector:
        forces = [(scalar / self.square_distance(n) * direction,
                   self.pos.angle_to_another(n.pos)) for n in herd]
        speed = np.sum([[f[0] * math.cos(f[1]), f[0] * math.sin(f[1])]
                        for f in forces], axis=0)
        return Vector(speed[0], speed[1])

    def set_grid(self, align_grid: Grid.Grid, chase_grid: Grid.Grid):
        self.align_grid = align_grid
        self.chase_grid = chase_grid

    def update_speed(self, align_grid: Grid.Grid, chase_grid: Grid.Grid):
        if not self.alive:
            return
        self.set_grid(align_grid, chase_grid)
        nearby_herd = self.update_speed_in_herd()
        if len(nearby_herd) > 0:
            self.update_speed_repel(nearby_herd)
        self.update_speed_chase()

    def _check_speed(self, speed: Vector, event: str, ids=[]):
        v = (speed.x ** 2 + speed.y ** 2) ** 0.5
        msg = Config().log_template.format(step=self.step, id=self.id, pos_x=self.pos.x, pos_y=self.pos.y, speed=v,
                                           speed_x=speed.x, speed_y=speed.y, event=event, ids=ids)
        if event in ["born"]:
            Config().chase_logger.info(msg)
        else:
            Config().chase_logger.debug(msg)

    def move(self, delta_t: float, const_speed=0):
        const_speed = Config().INIT_SPEED if const_speed == 0 else const_speed
        # v = np.sum([self.speed.toarray(), self.align_speed.toarray(),
        v = np.sum([self.align_speed.toarray(),
                    self.repel_speed.toarray(), self.chase_speed.toarray()], axis=0)
        v_len: float = (v[0] ** 2 + v[1] ** 2) ** .5
        if v_len > 0:
            self.speed = Vector(const_speed * v[0] / v_len, const_speed * v[1] / v_len)
        self.pos.move(self.speed, delta_t)
        self._check_speed(self.speed, "move")
        self.align_speed = Vector(0, 0)
        self.repel_speed = Vector(0, 0)
        self.chase_speed = Vector(0, 0)


class Sheep(Animal):
    def __init__(self, _id: int, **kwargs):
        super(Sheep, self).__init__("sheep", _id, **kwargs)
        self.chase_direction: int = -1  # away from the target
        self.predator_id = -1  # no wolf chases me
        self.is_caught = False

    def handle_caught(self, chase_herd: list[Animal], caught_herd: list[Animal]):
        msg_str = Config().event_template.format(step=self.step, id=self.id,
                                                 msg=f"caught_by {[c.id for c in caught_herd]}")
        Config().event_logger.info(msg_str)
        w: Wolf
        for w in chase_herd:
            if self.predator_id == w.id:
                w.increase_credit()
                msg_str = Config().event_template.format(step=self.step, id=self.id, msg=f"add_credit -> {w.id}")
                Config().event_logger.info(msg_str)
        # sheep die in 2 steps to allow each other
        # to handle caught event
        self.alive = self.is_caught
        self.is_caught = True

    def get_chase_caught_heard(self):
        chase_herd, caught_herd = super().get_chase_caught_heard()
        if len(chase_herd) == 0:
            return chase_herd, caught_herd

        predator = [w for w in chase_herd if self.predator_id == w.id]
        if len(predator) > 0:
            msg_str = Config().event_template.format(step=self.step, id=self.id,
                                                     msg=f"can see predator -> {self.predator_id}")
            Config().event_logger.debug(msg_str)
        elif self.predator_id != -1:
            msg_str = Config().event_template.format(step=self.step, id=self.id,
                                                     msg=f"no longer seen by predator <- {self.predator_id}")
            Config().event_logger.info(msg_str)
            self.predator_id = -1
        else:
            msg_str = Config().event_template.format(step=self.step, id=self.id, msg="saw wolves but not be seen")
            Config().event_logger.debug(msg_str)

        return chase_herd, caught_herd


class Wolf(Animal):
    def __init__(self, _id: int, **kwargs):
        # speed 1.0 - 1.1
        # sight 1.0 - 0.6
        super(Wolf, self).__init__("wolf", _id, **kwargs)
        self.chase_direction: int = 1
        self.has_target = False
        if self.id % Config().LEADER_RATIO == 0:
            self.is_leader = True
            self.wolf_speed = 1.0
        else:
            self.is_leader = False
            self.wolf_speed = Config().Wolf_normal_speed_ratio
            self.sight_2 = self.sight_2 * (Config().Wolf_normal_sight_ratio ** 2)

    def get_chase_caught_heard(self) -> (list[Animal], list[Animal]):
        chase_herd, caught_herd = super().get_chase_caught_heard()
        s: Sheep
        target = [s for s in chase_herd if s.predator_id == self.id]
        if len(target) == 0:
            self.has_target = False

        target_candidates = [s for s in chase_herd if s.predator_id == -1]
        for s in target_candidates:
            s.predator_id = self.id
            msg_str = Config().event_template.format(step=self.step, id=self.id, msg=f"aimed {s.id}")
            Config().event_logger.info(msg_str)
            self.has_target = True

        return chase_herd, caught_herd

    def handle_caught(self, chase_herd: list[Animal], caught_herd: list[Animal]):
        s: Sheep
        for s in caught_herd:
            msg_str = Config().event_template.format(step=self.step, id=self.id, msg=f"caught -> {s.id}")
            Config().event_logger.info(msg_str)
            # sheep die in 2 steps to allow each other
            # to handle caught event
            s.alive = s.is_caught
            s.is_caught = True

    def continue_update_chase_speed(self, chase_herd, scalar: float):
        chase_herd = [
            reduce(lambda a, b: a if self.square_distance(a) < self.square_distance(b) else b, chase_herd)]
        super().continue_update_chase_speed(chase_herd, scalar)
        if not self.is_leader:
            self.chase_speed.change_direction(Config().ANGLE_DIRECTION * Config().rnd.uniform(-1.0, 1))

    def move(self, delta_t: float, const_speed=0):
        const_speed = Config().INIT_SPEED if const_speed == 0 else const_speed
        if self.is_leader and self.has_target:
            self.align_speed = Vector(0, 0)
        super().move(delta_t, const_speed * self.wolf_speed)

    def increase_credit(self):
        self.credit *= Config().OMEGA
