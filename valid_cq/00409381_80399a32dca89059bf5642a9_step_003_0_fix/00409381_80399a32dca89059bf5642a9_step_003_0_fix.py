import cadquery as cq
import math

th = 6
r_left = 6
r_right = 20
r_small_hole = 3
r_center_hole = 6
bolt_r = 1.75
bolt_pattern_r = 12
bolt_count = 4
left_center = (-40, 0)
right_center = (30, 0)

rect_length = right_center[0] - r_right - left_center[0] - r_left
rect_width = r_left * 2

# Create the left disc, right disc, and connecting bar solids
left_sol = cq.Workplane("XY").center(left_center[0], left_center[1]).circle(r_left).extrude(th)
right_sol = cq.Workplane("XY").center(right_center[0], right_center[1]).circle(r_right).extrude(th)
bar_center_x = left_center[0] + r_left + rect_length / 2
bar_sol = cq.Workplane("XY").center(bar_center_x, 0).rect(rect_length, rect_width).extrude(th)

# Union them into one solid
result = left_sol.union(bar_sol).union(right_sol)

# Cut the left small hole
result = result.faces(">Z").workplane().center(left_center[0], left_center[1]).hole(r_small_hole * 2)
# Cut the central hole
result = result.faces(">Z").workplane().center(0, 0).hole(r_center_hole * 2)
# Cut the bolt holes around the center
for i in range(bolt_count):
    angle = i * 360.0 / bolt_count
    x = bolt_pattern_r * math.cos(math.radians(angle))
    y = bolt_pattern_r * math.sin(math.radians(angle))
    result = result.faces(">Z").workplane().center(x, y).hole(bolt_r * 2)