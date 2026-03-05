import cadquery as cq

# -- Parametric Dimensions --
post_height = 1000.0     # Height of the vertical tube
tube_size = 50.0         # Width/Depth of the square tube
wall_thickness = 3.0     # Tube wall thickness
base_width = 100.0       # Width of the square base plate
base_thickness = 8.0     # Thickness of the base plate
corner_radius = 5.0      # Fillet radius for base plate corners
hole_diameter = 10.0     # Diameter of mounting holes
hole_spacing = 75.0      # Distance between hole centers
gusset_height = 50.0     # Height of the triangular reinforcement
gusset_width = 25.0      # Width of the gusset along the base
gusset_thick = 4.0       # Thickness of the gusset plate

# -- 1. Create Base Plate --
# Center the base on the XY plane
base = (
    cq.Workplane("XY")
    .rect(base_width, base_width)
    .extrude(base_thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# Cut holes in the corners of the base plate
base = (
    base.faces(">Z")
    .workplane()
    .rect(hole_spacing, hole_spacing, forConstruction=True)
    .vertices()
    .hole(hole_diameter)
)

# -- 2. Create Vertical Square Tube --
# Extrude the tube upwards from the top face of the base
# We define an outer rectangle and an inner rectangle to create the hollow profile
tube = (
    base.faces(">Z")
    .workplane()
    .rect(tube_size, tube_size)
    .rect(tube_size - 2*wall_thickness, tube_size - 2*wall_thickness)
    .extrude(post_height, combine=True)
)

# -- 3. Create Gusset (Reinforcement Detail) --
# Create a triangular gusset on one side of the post
# We draw on the XZ plane (side view) and extrude symmetrically
# The triangle sits on the base plate (Z=base_thickness) and against the tube wall

# Define triangle points relative to the global origin
p1 = (tube_size / 2, base_thickness)                   # Corner at tube/base junction
p2 = (tube_size / 2 + gusset_width, base_thickness)    # Corner extending onto base
p3 = (tube_size / 2, base_thickness + gusset_height)   # Corner extending up the tube

gusset = (
    cq.Workplane("XZ")
    .polyline([p1, p2, p3])
    .close()
    .extrude(gusset_thick / 2.0, both=True)
)

# -- 4. Final Combination --
result = tube.union(gusset)