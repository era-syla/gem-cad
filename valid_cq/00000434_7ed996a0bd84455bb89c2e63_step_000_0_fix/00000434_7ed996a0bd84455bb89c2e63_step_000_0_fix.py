import cadquery as cq
import math

# Parameters
main_r = 10
main_w = 20
throw_r = 8
throw_w = 20
throw_offset = 10
cw_r = 20
cw_w = 10
positions_main = [0, 50, 100]
positions_throw = [25, 75]
front_pos = 110
flange_r = 15
flange_th = 5
hole_r = 2.5
hole_c = 10
hole_count = 6

# Build main journals
result = None
for x in positions_main:
    trans_x = x - main_w/2
    part = cq.Workplane('YZ').circle(main_r).extrude(main_w).translate((trans_x, 0, 0))
    result = part if result is None else result.union(part)

# Build throws
for x in positions_throw:
    trans_x = x - throw_w/2
    upper = cq.Workplane('YZ').circle(throw_r).extrude(throw_w).translate((trans_x, 0, throw_offset))
    lower = cq.Workplane('YZ').circle(throw_r).extrude(throw_w).translate((trans_x, 0, -throw_offset))
    result = result.union(upper).union(lower)

# Add counterweights
for x in positions_throw:
    trans_x = x - cw_w/2
    cw = cq.Workplane('YZ').circle(cw_r).extrude(cw_w).translate((trans_x, 0, 0))
    result = result.union(cw)

# Front flange with bolt holes
trans_x = front_pos - flange_th/2
flange = cq.Workplane('YZ').circle(flange_r).extrude(flange_th).translate((trans_x, 0, 0))
# Prepare hole positions on flange face
angles = [i * (360.0 / hole_count) for i in range(hole_count)]
points = [(hole_c * math.cos(math.radians(a)), hole_c * math.sin(math.radians(a))) for a in angles]
flange_holes = flange.faces('>X').workplane(centerOption='CenterOfBoundBox').pushPoints(points).circle(hole_r).cutThruAll()

result = result.union(flange_holes)