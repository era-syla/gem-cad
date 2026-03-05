import cadquery as cq

# Parametric dimensions
length = 100.0   # Total length of the racetrack shape
width = 60.0     # Total width of the racetrack shape
height = 30.0    # Height of the band
thickness = 2.0  # Wall thickness

# Derived dimensions
radius = width / 2.0
straight_section = length - width

# Create the outer profile path (a racetrack shape)
path = (
    cq.Workplane("XY")
    .moveTo(-straight_section / 2.0, -radius)
    .lineTo(straight_section / 2.0, -radius)
    .threePointArc((straight_section / 2.0 + radius, 0), (straight_section / 2.0, radius))
    .lineTo(-straight_section / 2.0, radius)
    .threePointArc((-straight_section / 2.0 - radius, 0), (-straight_section / 2.0, -radius))
    .close()
)

# Extrude the base shape
# We create a solid block first, then hollow it out
base_solid = path.extrude(height)

# Create the final hollow shape using shell
# A positive thickness adds material outwards, negative inwards. 
# Since we defined outer dimensions, let's shell inwards.
# We select the top and bottom faces to be removed to create an open tube.
result = base_solid.faces("<Z or >Z").shell(-thickness)

# Alternatively, using a 2D offset approach for a more explicit wall:
# sketch_outer = path
# sketch_inner = path.wires().toPending().offset2D(-thickness)
# result = sketch_outer.extrude(height).cut(sketch_inner.extrude(height))
# But shell is more idiomatic for "thin walled open shapes".

# Ensure the result is exported/assigned
if 'show_object' in globals():
    show_object(result)