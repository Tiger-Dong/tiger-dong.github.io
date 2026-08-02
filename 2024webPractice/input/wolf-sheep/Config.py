import logging
from numpy.random import default_rng, Generator
from ruamel import yaml
import os
from Logger import init_logger


def singleton(cls):
    _instance = {}

    def inner(*args, **kw):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kw)
        return _instance[cls]
    return inner


@singleton
class Config:
    def __init__(self, config_file=""):
        # will raise exception if not set config_file, which avoid being used accidentally before load config
        # if set, this instance can be conveniently used as Config() in the Singleton pattern
        with open(config_file, "r") as f:
            configs = yaml.load(f, Loader=yaml.Loader)
        self.N_WOLF = configs.get("N_WOLF", 10)  # number of  many wolves
        self.N_SHEEP = configs.get("N_SHEEP", 10)  # number of  many sheep
        self.ALPHA = configs.get("ALPHA", 0.2)  # 取向力系数
        self.BETA = configs.get("BETA", 500)  # 排斥力系数
        self.Gamma = configs.get("Gamma", 500)  # 狼羊 吸引力系数
        self.OMEGA = configs.get("OMEGA", 2)  # 领导力每次增加倍数
        self.LEADER_RATIO = configs.get("LEADER_RATIO", 9)  # 领导狼占总狼群 比例，e.g 1/9
        self.MAP_SCOPE = configs.get("MAP_SCOPE", 1000)  # 地图大小
        self.INIT_SPEED = configs.get("INIT_SPEED", 5)  # 5m/s",18km/h, 狼羊初始化速度
        self.RADIUS_ALIGNMENT = configs.get("RADIUS_ALIGNMENT", 100)  # 取向力半径
        self.RADIUS_REPEL = configs.get("RADIUS_REPEL", 5)  # 排斥力半径
        self.RADIUS_CAUGHT = configs.get("RADIUS_CAUGHT", 10)  # 狼抓住羊的距离
        self.RADIUS_SIGHT = configs.get("RADIUS_SIGHT", self.RADIUS_ALIGNMENT * 2)  # 狼羊吸引力半径

        self.ANGLE_DIRECTION = configs.get("ANGLE_DIRECTION",
                                           20)  # !!! 0 for debugging math.pi/18 # +- 10 degrees  普通狼扰动角度
        self.DELTA_T = configs.get("DELTA_T", 0.05)  # set as 1 for debugging, normally should be 0.01 or less
        self.MAX_ITERATION = configs.get("MAX_ITERATION", 80000)  # 最大迭代次数
        self.iteration_per_frame = configs.get("iteration_per_frame",
                                               50)  # run n steps then draw next frame # 每一帧图像跑多少次迭代

        self.Wolf_normal_speed_ratio = configs.get("Wolf_normal_speed_ratio", 1.1)  # 普通狼速度与 INIT_SPEED 比值
        self.Wolf_normal_sight_ratio = configs.get("Wolf_normal_sight_ratio", 0.6)  # 普通狼视野范围 比例 与 RADIUS_SIGHT

        self.draw_animation = configs.get("draw_animation", False)

        # 以下平方数 为了简化计算，预先求值
        self.RADIUS_ALIGNMENT_SQUARE = self.RADIUS_ALIGNMENT ** 2
        self.RADIUS_REPEL_SQUARE = self.RADIUS_REPEL ** 2
        self.RADIUS_CAUGHT_SQUARE = self.RADIUS_CAUGHT ** 2
        self.RADIUS_SIGHT_SQUARE = self.RADIUS_SIGHT ** 2

        self.seed: int = configs.get("seed", 1000)  # fix the random series 随机数种子，确定某一值会固定狼和羊的初始化位置，速度。正式运行时 设置为0
        self.rnd: Generator = default_rng(self.seed)  # 随机数生成器

        # event in {born, align, repel, chase, caught}
        self.log_template: str = \
            "{step}, {id}, {event}, {speed:.2f}, {speed_x:.2f}, {speed_y:.2f}, {pos_x:.2f}, {pos_y:.2f}, {ids}"
        self.leader_template: str = "{step}, {credits}"
        self.event_template: str = "{step}, {id}, {msg}"
        self.log_path = os.path.join(os.path.dirname(os.path.abspath(config_file)), "log")
        self._chase_logger = init_logger("chase", base_dir=self.log_path, log_file_name="chase.log",
                                         file_handler_level=logging.DEBUG)
        self._leader_logger = init_logger("leader", base_dir=self.log_path, log_file_name="leader.log")
        self._event_logger = init_logger("event", base_dir=self.log_path, log_file_name="event.log")

    @property
    def chase_logger(self) -> logging.Logger:
        return self._chase_logger

    @property
    def event_logger(self) -> logging.Logger:
        return self._event_logger

    @property
    def leader_logger(self) -> logging.Logger:
        return self._leader_logger
