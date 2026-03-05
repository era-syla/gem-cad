import cadquery as cq

# Parametric dimensions
# Main Cylinder (the thicker part)
cylinder_dia = 20.0
cylinder_length = 150.0

# Piston Rod (the thinner part)
rod_dia = 10.0
rod_length = 150.0

# End Fittings (Eyes)
eye_outer_dia = 16.0
eye_hole_dia = 8.0
eye_thickness = 12.0
eye_offset_from_end = eye_outer_dia / 2.0  # Center of the eye hole from the end of the rod/cylinder

# Create the main cylinder body
cylinder = cq.Workplane("XY").circle(cylinder_dia / 2.0).extrude(cylinder_length)

# Create the piston rod
# We start from the top face of the cylinder and extrude upwards
rod = (
    cylinder.faces(">Z")
    .workplane()
    .circle(rod_dia / 2.0)
    .extrude(rod_length)
)

# Combine cylinder and rod
body = rod

# --- Create the bottom eye (attached to cylinder) ---
# We need to orient it correctly. The image shows the eyes are perpendicular to the main axis.
# Let's place it at the bottom of the cylinder (Z=0)
bottom_eye = (
    cq.Workplane("XZ")
    .workplane(offset=-eye_thickness / 2.0)  # Center the thickness
    .center(0, -eye_offset_from_end)  # Move down slightly so the circle merges well
    .circle(eye_outer_dia / 2.0)
    .extrude(eye_thickness)
    .faces(">Y") # Select the face parallel to XZ plane
    .workplane()
    .hole(eye_hole_dia)
)

# Move the bottom eye to merge with the bottom of the cylinder
# The cylinder starts at Z=0 and goes to Z=cylinder_length.
# Currently the eye is centered at (0, -eye_offset, 0) relative to origin.
# We want it at the bottom end.
# Actually, let's just create it directly at the origin and union it.
# The previous construction placed it slightly below Z=0 on the Y axis in the local plane, 
# which corresponds to Z axis in global because of the XZ plane selection? 
# Let's be more precise with locations.

# Re-doing Bottom Eye Strategy:
# Create a standalone cylinder for the eye, rotate and move it.
eye_shape = (
    cq.Workplane("XY")
    .circle(eye_outer_dia / 2.0)
    .extrude(eye_thickness)
    .faces(">Z")
    .workplane()
    .hole(eye_hole_dia)
)

# Rotate so the hole axis is Y (or X), and the flat faces are XZ (or YZ)
# The image shows the eye axis is perpendicular to the tube axis.
bottom_eye_placed = (
    eye_shape
    .rotate((0,0,0), (1,0,0), 90) # Rotate around X to make hole axis Y-aligned
    .translate((0, 0, -eye_offset_from_end + (eye_outer_dia/4))) # Shift down to just touch/overlap slightly
)

# --- Create the top eye (attached to rod) ---
top_eye_placed = (
    eye_shape
    .rotate((0,0,0), (1,0,0), 90)
    .translate((0, 0, cylinder_length + rod_length + eye_offset_from_end - (eye_outer_dia/4)))
)

# Combine everything
result = body.union(bottom_eye_placed).union(top_eye_placed)

# Optional: Add a small chamfer/fillet where the rod meets the cylinder for realism
# Select the edge at the junction. Z height is cylinder_length.
try:
    result = result.edges(cq.NearestToPointSelector((0, rod_dia/2, cylinder_length))).fillet(1.0)
except:
    pass # Skip if selection fails, just a cosmetic detail

# Export or visualization
if 'show_object' in globals():
    show_object(result)