import cadquery as cq

L = 150
W = 100
T = 3
inner_M = 10

tab_w = 10
tab_t = 2
tab_h = 1.5
tab_x_offset = 37.5

hole_d = 3
hole_x = 25
hole_y = W/2 - 15

sq_sz = 6
sq_x = -L/2 + 15
sq_y = -W/2 + 15

slot1_w = 20
slot1_h = 4
slot1_x = 0
slot1_y = -W/2 + 15

slot2_w = 15
slot2_h = 4
slot2_x = L/2 - 25
slot2_y = -W/2 + 20

result = cq.Workplane("XY").rect(L, W).extrude(T)

# Central rectangular cutout
result = result.faces(">Z").workplane().rect(L - 2*inner_M, W - 2*inner_M).cutThruAll()

# Two small circular holes near top edge
result = result.faces(">Z").workplane().pushPoints([(-hole_x, hole_y), (hole_x, hole_y)]).circle(hole_d/2).cutThruAll()

# Square hole near bottom left
result = result.faces(">Z").workplane().pushPoints([(sq_x, sq_y)]).rect(sq_sz, sq_sz).cutThruAll()

# Two rectangular slots near bottom
result = result.faces(">Z").workplane().pushPoints([(slot1_x, slot1_y)]).rect(slot1_w, slot1_h).cutThruAll()
result = result.faces(">Z").workplane().pushPoints([(slot2_x, slot2_y)]).rect(slot2_w, slot2_h).cutThruAll()

# Two small tabs on the top edge
result = result.faces(">Y").workplane().pushPoints([
    (-tab_x_offset, T/2 + tab_h/2),
    ( tab_x_offset, T/2 + tab_h/2),
]).rect(tab_w, tab_h).extrude(tab_t)