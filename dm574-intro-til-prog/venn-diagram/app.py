#Code has some problems with floating point imprecision

import math

class Point:
    def __init__(self, x:float, y:float, r:float):
        self.x = x
        self.y = y
        self.r = r


def distance(p1:Point, p2:Point) -> float:
    return math.sqrt((p1.x - p2.x)**2 + (p1.y + p2.y)**2)

def venn_diagram(points:list[Point]) -> bool:
    if len(points) < 2:
        return True

    base_dist = distance(points[0], points[1])
    base_radius = points[0].r

    l,r = 0,1
    while r <= len(points) - 1:
        p1 = points[l]
        p2 = points[r]

        dist = distance(p1,p2)
        radius = p2.r

        if not(math.isclose(dist, base_dist)):
            print(dist)
            print(base_dist)
            return False

        if not(math.isclose(radius,  base_radius)):
            return False

        if dist > radius * 2:
            return False

        if dist <= radius:
            return False

        l += 1
        r += 1

    return True



point_1 = Point(0.0, 0.0, 1.0)
point_2 = Point(1.5, 0.0, 1.0)
point_3 = Point(0.75, (math.sqrt(3) / 2) * 1.5, 1.0)

print(venn_diagram([point_1,point_2,point_3]))
