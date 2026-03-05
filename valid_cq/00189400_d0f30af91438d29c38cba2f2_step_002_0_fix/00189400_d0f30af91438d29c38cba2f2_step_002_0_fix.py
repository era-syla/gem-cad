import cadquery as cq

# Parameters
length = 120.0
thickness = 10.0
height = 15.0
end_clearance_r = 7.5
end_hole_r = 2.5
small_hole_r = 1.5
small_hole_count = 10
small_hole_spacing = 10.0
slot_length = 100.0
slot_height = 4.0
slot_depth = 2.0

# Base bar
result = cq.Workplane("XY").box(length, thickness, height)

# Concave end profiles (cylindrical cuts to approximate semicircles)
result = result.faces("<X").workplane().circle(end_clearance_r).cutThruAll()
result = result.faces(">X").workplane().circle(end_clearance_r).cutThruAll()

# Small through holes at each end
result = result.faces("<X").workplane().circle(end_hole_r).cutThruAll()
result = result.faces(">X").workplane().circle(end_hole_r).cutThruAll()

# Rectangular slot on front face
result = result.faces(">Y").workplane().rect(slot_length, slot_height).cutBlind(-slot_depth)

# Row of small holes on top face
x_start = -((small_hole_count - 1) * small_hole_spacing) / 2.0
points = [(x_start + i * small_hole_spacing, 0) for i in range(small_hole_count)]
result = result.faces(">Z").workplane().pushPoints(points).circle(small_hole_r).cutThruAll()