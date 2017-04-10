from trilateration import *

p1 = point(0.81, 1.2)
p2 = point(1.21, 0.69)
p3 = point(0.87, 0.84)

c1 = circle(p1, 0.70)
c2 = circle(p2, 0.51)
c3 = circle(p3, 0.63)

circle_list = [c1, c2, c3]

point_obj = do_trilateration(circle_list)
print(point_obj.x, point_obj.y)

