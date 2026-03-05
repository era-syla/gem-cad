import cadquery as cq

# ==========================================
# Parametric Dimensions
# ==========================================
height = 160.0          # Total height of the vertical leg
width = 40.0            # Width of the profile (extrusion depth)
base_length = 60.0      # Length of the horizontal base leg
thickness = 6.0         # Thickness of the material

# Square Cutout parameters
sq_hole_size = 25.0
sq_hole_top_margin = 20.0  # Distance from top edge to top of the square hole

# Base Hole parameters
rnd_hole_diam = 6.0
rnd_hole_spacing = 24.0    # Center-to-center spacing
rnd_hole_end_margin = 12.0 # Distance from the end of the base to hole center

# ==========================================
# 3D Modeling
# ==========================================

# 1. Create the main L-shaped body
# Drawn as a profile on the YZ plane and extruded along the X axis.
# Origin (0,0,0) is located at the bottom-outer corner.
result = (
    cq.Workplane("YZ")
    .polyline([
        (0, 0),                     # Bottom-rear corner
        (0, height),                # Top-rear
        (thickness, height),        # Top-front
        (thickness, thickness),     # Inner vertical corner
        (base_length, thickness),   # Inner horizontal corner
        (base_length, 0),           # Front tip
        (0, 0)                      # Close the loop
    ])
    .close()
    .extrude(width / 2.0, both=True) # Extrude symmetrically centered on X axis
)

# 2. Create the Square Cutout on the vertical leg
# Calculating the Z-position of the hole center
hole_z_center = height - sq_hole_top_margin - (sq_hole_size / 2.0)

# We select the back face (at Y=0), create a workplane, and cut through.
# Note: The center of the face is automatically the origin of the new workplane.
# We calculate the offset from the face center to the hole center.
face_z_center = height / 2.0
offset_z = hole_z_center - face_z_center

result = (
    result
    .faces("<Y")            # Select the rear face (Normal pointing -Y)
    .workplane()
    .moveTo(0, offset_z)    # Move vertically relative to face center
    .rect(sq_hole_size, sq_hole_size)
    .cutThruAll()
)

# 3. Create the Mounting Holes on the base
# We select the top face of the horizontal leg (the "shelf").
# We use a point selector to ensure we grab the shelf face (Z=thickness) 
# and not the top of the vertical leg (Z=height).
shelf_target_point = (0, base_length / 2.0, thickness)

# Calculate offset for hole placement relative to the shelf face center.
shelf_center_y = (base_length + thickness) / 2.0
target_hole_y = base_length - rnd_hole_end_margin
offset_y = target_hole_y - shelf_center_y

result = (
    result
    .faces(">Z")                                           # Select upward facing faces
    .faces(cq.NearestToPointSelector(shelf_target_point))  # Filter for the shelf
    .workplane()
    .moveTo(0, offset_y)                                   # Move to the Y-row of the holes
    .pushPoints([
        (-rnd_hole_spacing / 2.0, 0),
        (rnd_hole_spacing / 2.0, 0)
    ])
    .circle(rnd_hole_diam / 2.0)
    .cutThruAll()
)