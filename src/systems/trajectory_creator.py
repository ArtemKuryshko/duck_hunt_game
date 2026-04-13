import random
import math
from config import SCREEN_HEIGHT, SCREEN_WIDTH


class BirdTrajectory:

    OFFSCREEN_MARGIN = 100
    EDGE_PADDING = 50
    MIN_SPAWN_Y = 420

    def __init__(self, speed: float, spawn_point: tuple | None = None):
        self.sw = SCREEN_WIDTH
        self.sh = SCREEN_HEIGHT
        self.speed = speed


        self.p0 = spawn_point
        self.p3 = self._generate_offscreen_point(opposite_to=self.p0)
        self.p1, self.p2 = self._generate_control_points()
        self.t = 0.0
        self.is_finished = False


    def _extreme_y(self) -> int: # y для точок за екраном 
        return random.randint(self.EDGE_PADDING, self.MIN_SPAWN_Y)

    def _generate_offscreen_point(self, opposite_to: tuple | None = None) -> tuple:
        m = self.OFFSCREEN_MARGIN

        if opposite_to is not None:
            ox, oy = opposite_to
            if ox < 0:
                return (self.sw + m, self._extreme_y())
            else:
                return (-m, self._extreme_y())

        side = random.choice(('left', 'right'))
        if side == 'left':
            return (-160, self._extreme_y())
        else:
            return (self.sw + 160, self._extreme_y())

    def _random_x(self, min_x: int, max_x: int) -> int:
        return random.randint(min_x, max_x)

    def _random_y(self, min_y: int, max_y: int) -> int:
        return random.randint(min_y, max_y)
    
    def _generate_control_points(self) -> tuple[tuple, tuple]:
        half_x = self.sw // 2
        p1 = (self._random_x(self.EDGE_PADDING, half_x), self._random_y(self.EDGE_PADDING, self.MIN_SPAWN_Y))
        p2 = (self._random_x(half_x, self.sw - self.EDGE_PADDING), self._random_y(self.EDGE_PADDING, self.MIN_SPAWN_Y))
        return p1, p2


    def _bezier(self, t: float) -> tuple:
        it = 1.0 - t
        it2 = it * it
        t2 = t * t

        x = (it2 * it * self.p0[0]
             + 3 * it2 * t  * self.p1[0]
             + 3 * it  * t2 * self.p2[0]
             + t2  * t * self.p3[0])

        y = (it2 * it * self.p0[1]
             + 3 * it2 * t  * self.p1[1]
             + 3 * it  * t2 * self.p2[1]
             + t2  * t * self.p3[1])

        return x, y

    def _bezier_derivative(self, t: float) -> tuple:
        it = 1.0 - t
        it2 = it * it
        t2 = t * t

        dx = 3 * (it2 * (self.p1[0] - self.p0[0])
                  + 2 * it * t * (self.p2[0] - self.p1[0])
                  + t2  * (self.p3[0] - self.p2[0]))

        dy = 3 * (it2 * (self.p1[1] - self.p0[1])
                  + 2 * it * t * (self.p2[1] - self.p1[1])
                  + t2  * (self.p3[1] - self.p2[1]))

        return dx, dy


    def get_position(self) -> tuple:
        return self._bezier(self.t)

    def get_rotation_angle(self) -> float:
        dx, dy = self._bezier_derivative(self.t)
        if dx == 0.0 and dy == 0.0:
            return 0.0
        return math.degrees(math.atan2(-dy, dx))

    def update(self) -> None:
        if self.is_finished:
            return
        self.t += self.speed
        if self.t >= 1.0:
            self.t = 1.0
            self.is_finished = True
