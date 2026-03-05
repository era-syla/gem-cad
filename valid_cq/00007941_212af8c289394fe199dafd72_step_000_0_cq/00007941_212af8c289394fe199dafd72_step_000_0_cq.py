import cadquery as cq

# Parametric dimensions
base_diameter = 20.0  # Diameter of the wider bottom section
base_height = 40.0    # Height of the wider bottom section
neck_diameter = 8.0   # Diameter of the narrower top section
neck_height = 30.0    # Height of the narrower top section
wall_thickness = 1.0  # Thickness of the wall (making it hollow)

# Create the base cylinder
base = cq.Workplane("XY").circle(base_diameter / 2).extrude(base_height)

# Create the neck cylinder on top of the base
# We select the top face of the base, draw a circle, and extrude
neck = (
    base.faces(">Z")
    .workplane()
    .circle(neck_diameter / 2)
    .extrude(neck_height)
)

# Combine into a single solid so far
part = neck

# Hollow out the entire shape to create the tube-like appearance
# We assume the object is hollow all the way through or at least from the top.
# The image shows a clear opening at the top. Let's make it a shell.
# We select the top face to be open.
result = part.faces(">Z").shell(-wall_thickness)

# Alternatively, if only the top part is a tube and the bottom is solid (less likely for this geometry style):
# result = part.faces(">Z").hole(neck_diameter - 2*wall_thickness, depth=neck_height) 
# But the image suggests a uniform thin-walled structure typical of a casing or connector. 
# The shell() operation is the most robust way to achieve the "thin wall" look consistent with the top opening.