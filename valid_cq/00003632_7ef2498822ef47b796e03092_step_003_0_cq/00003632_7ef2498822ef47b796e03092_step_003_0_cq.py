import cadquery as cq

# Parameters
plate_width = 100.0   # Width of the square plate
plate_thickness = 10.0 # Thickness of the plate
center_hole_dia = 40.0 # Diameter of the large central hole
corner_radius = 2.0    # Chamfer/Fillet radius on the corners (visual approximation)

# Mounting hole parameters
bolt_hole_spacing = 80.0 # Distance between centers of mounting holes
bolt_hole_dia = 6.0      # Diameter of the through hole
cbore_dia = 12.0         # Counterbore diameter
cbore_depth = 4.0        # Counterbore depth

# Recess/Pocket parameters (the shallow rectangular indentation)
recess_width = 25.0
recess_length = 15.0
recess_depth = 1.0     # Very shallow depth based on visual
recess_offset_x = 30.0 # Offset from center along X axis
recess_offset_y = 0.0  # Centered along Y axis relative to the side, or offset from center

# Create the base plate
result = (
    cq.Workplane("XY")
    .box(plate_width, plate_width, plate_thickness)
)

# Add corner chamfers
# Select vertical edges on the corners
result = result.edges("|Z").chamfer(corner_radius)

# Create the central hole
result = result.faces(">Z").workplane().hole(center_hole_dia)

# Create the mounting holes (counterbored)
# Define the locations for the 4 holes
hole_locs = [
    (bolt_hole_spacing/2, bolt_hole_spacing/2),
    (-bolt_hole_spacing/2, bolt_hole_spacing/2),
    (-bolt_hole_spacing/2, -bolt_hole_spacing/2),
    (bolt_hole_spacing/2, -bolt_hole_spacing/2)
]

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_locs)
    .cboreHole(bolt_hole_dia, cbore_dia, cbore_depth)
)

# Create the shallow rectangular recess connected to the center hole
# Based on the image, it looks like a tag or label area extending from the hole rim
# towards one of the corners or sides. Let's approximate it as a rectangle 
# merged with the center hole or just a pocket near it. 
# Looking closely, it cuts into the top face.

recess_sketch = (
    cq.Workplane("XY")
    .workplane(offset=plate_thickness/2) # Work on top surface
    .center(recess_offset_x, recess_offset_y) # Position relative to center
    .rect(recess_width, recess_length)
)

# We cut this shape into the main body
# To make it look like the image where it connects to the hole:
# It seems to be a rectangular relief situated on the X-axis edge of the hole.
# Let's adjust positioning to overlap the hole edge.
recess_center_dist = (center_hole_dia/2) + (recess_width/2) - 2.0 # -2.0 overlap

result = (
    result.faces(">Z")
    .workplane()
    .center(recess_center_dist, 0)
    .rect(recess_width, recess_length)
    .cutBlind(-recess_depth)
)

# Apply a small chamfer to the top edges for a realistic look
result = result.faces(">Z").edges().chamfer(0.5)