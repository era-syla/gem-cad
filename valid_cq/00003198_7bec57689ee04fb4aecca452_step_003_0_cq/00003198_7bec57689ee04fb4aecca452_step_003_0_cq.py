import cadquery as cq

# Parameters
# Main plate dimensions
plate_height = 100.0
plate_width = 80.0
plate_thickness = 10.0
corner_radius = 15.0  # Radius for the rounded corner

# Face mounting holes (countersunk) parameters
face_hole_spacing_x = 50.0  # Horizontal distance between holes
face_hole_spacing_y = 50.0  # Vertical distance between holes
face_hole_diameter = 5.0    # Through-hole diameter
face_cbore_diameter = 10.0  # Countersink/Counterbore diameter
face_cbore_angle = 82.0     # Angle for countersink

# Top edge mounting holes parameters
top_hole_spacing = 40.0
top_hole_diameter = 3.0
top_hole_depth = 15.0

# Construction
# 1. Create the base plate centered on XY plane for convenience
# We start with a box
base_plate = cq.Workplane("XY").box(plate_width, plate_height, plate_thickness)

# 2. Add the rounded corner
# Looking at the image, if the plate is standing up, the bottom right corner is rounded.
# If we assume the view is looking at the XY plane, and X is right, Y is up:
# The rounded corner appears to be on the bottom-right relative to the face.
# Let's select the vertical edge at (X_positive, Y_negative).
result = base_plate.edges(">X and <Y").fillet(corner_radius)

# 3. Add the 4 countersunk holes on the face
# We need to position them. Assuming they are centered on the face.
# We select the top face (Z positive)
result = (
    result.faces(">Z")
    .workplane()
    .rect(face_hole_spacing_x, face_hole_spacing_y, forConstruction=True)
    .vertices()
    .cskHole(face_hole_diameter, face_cbore_diameter, face_cbore_angle)
)

# 4. Add the 2 holes on the top edge
# We select the top face relative to the standing orientation (Y positive edge)
result = (
    result.faces(">Y")
    .workplane()
    # We want two holes centered along the X axis of this new workplane
    .pushPoints([(-top_hole_spacing / 2, 0), (top_hole_spacing / 2, 0)])
    .hole(top_hole_diameter, top_hole_depth)
)

# Rotate the result to match the isometric view in the image better (standing up)
result = result.rotate((0, 0, 0), (1, 0, 0), 90)