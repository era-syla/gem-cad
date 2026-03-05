import cadquery as cq

# Parameters
body_height = 80.0       # Total height of the main extrusion
body_width = 30.0        # Width of the stadium profile
body_thickness = 14.0    # Thickness of the stadium profile
disk_diameter = 26.0     # Diameter of the side circular feature
disk_thickness = 2.0     # Thickness of the side circular feature

# Derived parameters
# Radius for stadium ends and top dome (half of thickness)
# Using a tiny epsilon subtraction ensures robust fillet generation in the kernel
fillet_radius = (body_thickness / 2.0) - 0.001

# 1. Create the main body (Stadium/Pill shape)
# Start with a rectangular box centered in XY, sitting on Z=0
result = (
    cq.Workplane("XY")
    .box(body_width, body_thickness, body_height, centered=(True, True, False))
    # Fillet vertical edges to transform rectangle into stadium shape
    .edges("|Z")
    .fillet(fillet_radius)
)

# 2. Create the top dome
# Fillet the top edge loop. Since the profile is a stadium and radius is half-thickness,
# this creates a fully rounded top (semi-cylinder merging into quarter-spheres).
result = result.edges(">Z").fillet(fillet_radius)

# 3. Add the side disk
# Calculate the vertical position for the disk center. 
# We align it with the center of the top dome curvature.
disk_center_z = body_height - (body_thickness / 2.0)

# Calculate the offset relative to the face center (which is at Z = body_height / 2)
face_center_z = body_height / 2.0
offset_z = disk_center_z - face_center_z

result = (
    result
    .faces("<Y")                                   # Select one of the flat faces (e.g., Back)
    .workplane(centerOption="CenterOfBoundBox")    # Set 2D workplane origin at face center
    .center(0, offset_z)                           # Move 2D origin up to the target Z height
    .circle(disk_diameter / 2.0)                   # Sketch the disk
    .extrude(disk_thickness)                       # Extrude outwards
)