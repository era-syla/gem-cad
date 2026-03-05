import cadquery as cq

# Parametric dimensions
width = 100.0          # Plate width
length = 100.0         # Plate length
thickness = 15.0       # Plate thickness
corner_radius = 10.0   # Radius of the rounded corners

# Central hole dimensions (Counterbored)
center_hole_dia = 20.0       # Main central hole diameter (through)
center_cbore_dia = 30.0      # Counterbore diameter
center_cbore_depth = 5.0     # Counterbore depth

# Mounting hole dimensions (Corner holes)
mount_hole_dia = 6.0         # Mounting hole diameter
mount_hole_inset = 10.0      # Distance from edges to center of hole
mount_hole_cbore_dia = 10.0  # Counterbore diameter for mounting holes
mount_hole_cbore_depth = 3.0 # Depth of counterbore for mounting holes

# Create the base plate with rounded corners
# We start with a rectangle, extrude it, and then fillet the vertical edges
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# Add the central counterbored hole
# Workplane is assumed to be the top face for drilling operations
result = (
    result.faces(">Z")
    .workplane()
    .cboreHole(center_hole_dia, center_cbore_dia, center_cbore_depth)
)

# Add the four corner mounting holes
# We calculate the positions based on the plate dimensions and inset
x_pos = (length / 2) - mount_hole_inset
y_pos = (width / 2) - mount_hole_inset

result = (
    result.faces(">Z")
    .workplane()
    .rect(2 * x_pos, 2 * y_pos, forConstruction=True) # Create a construction rectangle for hole centers
    .vertices()
    .cboreHole(mount_hole_dia, mount_hole_cbore_dia, mount_hole_cbore_depth)
)

# If the mounting holes in the image are just countersunk or plain holes, 
# simply replace .cboreHole with .cskHole or .hole respectively.
# The image suggests a slight depression, so cboreHole or cskHole is appropriate.