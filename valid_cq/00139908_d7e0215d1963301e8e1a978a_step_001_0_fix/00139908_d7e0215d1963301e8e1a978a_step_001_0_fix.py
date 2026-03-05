import cadquery as cq

# Parameters
thk = 5            # plate thickness
width = 20         # depth of bracket (into the screen)
base_length = 80   # length of the bottom flange
side_height = 40   # height of the side flanges
hole_dia = 6       # diameter of mounting holes
hole_offset = 15   # inset of the outer holes from the ends on the bottom flange

# Build bottom flange
result = cq.Workplane("XY").rect(base_length, width).extrude(thk)

# Build right side flange (attached at X = +base_length/2)
result = result.faces(">X").workplane().rect(width, side_height).extrude(thk)

# Build left side flange (attached at X = -base_length/2)
result = result.faces("<X").workplane().rect(width, side_height).extrude(thk)

# Drill three through-holes in the bottom flange
result = result.faces(">Z").workplane().pushPoints([
    (-base_length/2 + hole_offset, 0),
    (0, 0),
    ( base_length/2 - hole_offset, 0)
]).hole(hole_dia)

# Drill one through-hole in the right side flange
result = result.faces(">X").workplane().hole(hole_dia)

# Drill one through-hole in the left side flange
result = result.faces("<X").workplane().hole(hole_dia)