from __future__ import annotations
from Config import Config
import numpy as np
from math import cos, sin, sqrt, fmod, copysign


class Vector:
    def __init__(self, x: float, y: float, max_scope=0):
        if max_scope == 0:
            config = Config()  # works because of singleton
            max_scope = config.MAP_SCOPE
        self.x: float = x
        self.y: float = y
        self.max_scope = max_scope

    def toarray(self):
        return np.array([self.x, self.y])

    def __mul__(self, scaler: float):
        self.x *= scaler
        self.y *= scaler

    def change_direction(self, degree:float):
        theta = np.deg2rad(degree)
        rot = np.array([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])
        self.x, self.y = np.dot(rot, [self.x, self.y])

    def square_distance(self, another_one) -> float:
        x_dis = abs(self.x - another_one.x)
        y_dis = abs(self.y - another_one.y)
        return (min(x_dis, self.max_scope - x_dis) ** 2 +
                min(y_dis, self.max_scope - y_dis) ** 2)

    def distance(self, another_one: Vector) -> float:
        return sqrt(self.square_distance(another_one))

    def angle_to_another(self, another: Vector) -> float:
        x = another.x - self.x
        y = another.y - self.y
        return np.angle(complex(x if abs(x) <= self.max_scope/2 else x + copysign(self.max_scope, -x),
                       y if abs(y) <= self.max_scope/2 else y + copysign(self.max_scope, -y)))

    def add(self, another: Vector) -> Vector:
        return Vector(self.x + another.x, self.y + another.y)

    def move_line_speed(self,speed:Vector, delta_t: float) -> None:  # speed is also a vector
        self.x = (self.x + speed.x * delta_t) % self.max_scope  # periodic boundary
        self.y = (self.y + speed.y * delta_t) % self.max_scope  # periodic boundary

    def move_angle_speed(self, speed: Vector, delta_t: float) -> None:  # speed is also a vector
        self.x = (self.x + speed.x * cos(speed.y) * delta_t) % self.max_scope  # periodic boundary
        self.y = (self.y + speed.x * sin(speed.y) * delta_t) % self.max_scope  # periodic boundary

    def move(self, speed:Vector, delta_t: float) -> None:  # speed is also a vector
        return self.move_line_speed(speed,delta_t)
