# init sheep's position randomly, avoid overlap
# init sheep's speed randomly within INIT_SPEED
# sheep move together with a random direction ∆
# sheep can't overlap
# move with updated kdtree to check if overlap

import numpy as np
import math
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from Config import Config
import Grid
import Animal
from Vector import Vector


Animals: list[Animal.Animal] = []
Alignment_Grid: Grid.Grid = None
Chase_Grid: Grid.Grid = None
sheep_points = None
wolf_points = None
leader_points = None
last_wolves_credit_status = []  # init status of wolves credit, to reduce record size
start_time: float = time.time()
step: int = 0  # current iteration step


def alive_animals(animals: list[Animal]) -> list[Animal]:
    return [a for a in animals if a.alive]


def init_animals() -> (list[Animal.Wolf], list[Animal.Sheep]):
    wolves: list[Animal.Wolf] = []
    sheep: list[Animal.Sheep] = []
    rnd = Config().rnd
    number_animals = Config().N_WOLF + Config().N_SHEEP
    positions = [Vector(p[0], p[1]) for p in zip(
        rnd.choice(np.arange(0, Config().MAP_SCOPE / Config().RADIUS_REPEL), size=number_animals, replace=False)
        * Config().RADIUS_REPEL,
        rnd.uniform(0, Config().MAP_SCOPE, number_animals))]

    speed = [Vector(Config().INIT_SPEED * math.cos(angle), Config().INIT_SPEED * math.sin(angle))
             for angle in rnd.uniform(- math.pi, math.pi, number_animals)]
    for i in range(Config().N_WOLF):
        wolves.append(Animal.Wolf(i, pos=positions[i], speed=speed[i], marker="D"))
    for i in range(Config().N_SHEEP):
        sheep.append(Animal.Sheep(Config().N_WOLF + i, pos=positions[Config().N_WOLF + i],
                                  speed=speed[Config().N_WOLF + i], marker="+"))
    return wolves, sheep


def init():
    global sheep_points, wolf_points, leader_points, Alignment_Grid, Chase_Grid, start_time, Animals
    sheep, wolves = init_animals()
    Animals.extend(wolves)
    Animals.extend(sheep)
    Alignment_Grid = Grid.Grid(Config().RADIUS_ALIGNMENT, Config().MAP_SCOPE)
    Chase_Grid = Grid.Grid(Config().RADIUS_SIGHT, Config().MAP_SCOPE)

    if Config().draw_animation:
        shp = np.array([[s.pos.x, s.pos.y] for s in Animals if isinstance(s, Animal.Sheep)])
        sheep_points.set_data(shp.T)
        wlv = np.array([[s.pos.x, s.pos.y] for s in Animals if isinstance(s, Animal.Wolf) and not s.is_leader])
        wolf_points.set_data(wlv.T)
        leaders = np.array([[s.pos.x, s.pos.y] for s in Animals if isinstance(s, Animal.Wolf) and s.is_leader])
        leader_points.set_data(leaders.T)

    now = time.time()
    Config().event_logger.info(f"init costs {now - start_time:.2f}s")
    start_time = now
    return sheep_points, wolf_points, leader_points


def animate(i: int):
    global fig, ax, sheep_points, leader_points, wolf_points, Animals, start_time, last_wolves_credit_status, step

    for j in range(Config().iteration_per_frame):
        Animal.Animal.Distance_Map.clear()
        Alignment_Grid.update_index(Animals)
        Chase_Grid.update_index(Animals)
        step = i * Config().iteration_per_frame + j
        a: Animal
        for a in Animals:
            a.set_step(step)
            a.update_speed(Alignment_Grid, Chase_Grid)
        Animals = alive_animals(Animals)
        for a in Animals:
            a.move(Config().DELTA_T)

        wolves_credit = [(a.id, a.credit) for a in Animals if a.id < Config().N_WOLF]
        if last_wolves_credit_status != wolves_credit:
            Config().leader_logger.info(Config().leader_template.format(step=step, credits=wolves_credit))
            last_wolves_credit_status = wolves_credit

        if len(Animals) - Config().N_WOLF == 0:
            log_end_time()
            exit(0)

    if Config().draw_animation:
        shp = np.array([[s.pos.x, s.pos.y] for s in Animals if isinstance(s, Animal.Sheep)])
        sheep_points.set_data(shp.T)
        wlv = np.array([[s.pos.x, s.pos.y] for s in Animals if isinstance(s, Animal.Wolf) and not s.is_leader])
        wolf_points.set_data(wlv.T)
        leaders = np.array([[s.pos.x, s.pos.y] for s in Animals if isinstance(s, Animal.Wolf) and s.is_leader])
        leader_points.set_data(leaders.T)

    return sheep_points, wolf_points, leader_points


def log_end_time():
    global step, start_time, Animals
    caught_sheep = Config().N_WOLF + Config().N_SHEEP - len(Animals)
    life_time = time.time() - start_time
    Config().event_logger.info(f"{step}, finished in {life_time :.2f}s, caught sheep {caught_sheep}")


def main(config_file="config.yml"):
    config = Config(config_file)
    global fig, ax, sheep_points, wolf_points, leader_points
    if config.draw_animation:
        fig = plt.figure()
        ax = fig.add_subplot(111, xlim=(0, config.MAP_SCOPE), ylim=(0, config.MAP_SCOPE))
        sheep_points, = ax.plot([], [], '+', ms=4)
        wolf_points, = ax.plot([], [], 'D', ms=4)
        leader_points, = ax.plot([], [], 'o', ms=6)
        # interval: Delay between frames in milliseconds.
        ani = animation.FuncAnimation(fig, animate, frames=int(config.MAX_ITERATION / config.iteration_per_frame),
                                      repeat=False, interval=10, blit=True, init_func=init)
        plt.show()
    else:
        init()
        for i1 in range(int(config.MAX_ITERATION / config.iteration_per_frame)):
            animate(i1)
    log_end_time()


def step_draw():
    global fig, ax, sheep_points, wolf_points, leader_points, Animals, Alignment_Grid, Chase_Grid
    with plt.ion():
        fig = plt.figure()
        ax = fig.add_subplot(111, xlim=(0, Config().MAP_SCOPE), ylim=(0, Config().MAP_SCOPE))
        sheep_points, = ax.plot([], [], '+', ms=4)
        wolf_points, = ax.plot([], [], 'D', ms=4)
        leader_points, = ax.plot([], [], 'o', ms=6)
        init()
        plt.draw()
        plt.pause(0.1)

        for i1 in range(1000):
            animate(i1)
            plt.draw()
            plt.pause(0.05)


if __name__ == "__main__":
    main()
    # step_draw()
