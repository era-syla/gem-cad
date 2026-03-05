import cadquery as cq

# --- Parameters ---
num_u = 42                  # Number of Rack Units (e.g., 42U standard rack)
u_height = 44.45            # 1.75 inches in mm (Standard 1U height)
rail_width = 30.0           # Width of the mounting face
rail_depth = 30.0           # Depth of the structural leg
thickness = 2.5             # Material thickness
hole_size = 9.5             # Size of square cage nut holes (approx 3/8")
total_height = num_u * u_height

# EIA-310 Standard Hole Pattern
# Holes are spaced 0.25", 0.625", 0.625" within a unit.
# Offsets from the start of the unit are:
offsets_mm = [x * 25.4 for x in [0.25, 0.875, 1.50]]

# --- Geometry Construction ---

# 1. Create the base L-profile extrusion
# We draw the profile on the XY plane and extrude along Z.
result = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(rail_width, 0)
    .lineTo(rail_width, thickness)
    .lineTo(thickness, thickness)
    .lineTo(thickness, rail_depth)
    .lineTo(0, rail_depth)
    .close()
    .extrude(total_height)
)

# 2. Calculate hole positions
# We will place holes on the face at Y=0 (the rail_width face).
# Coordinates are calculated relative to the center of that face for the workplane.
hole_points = []
face_center_z = total_height / 2.0

for u in range(num_u):
    base_z = u * u_height
    for offset in offsets_mm:
        # Calculate absolute Z height of the hole center
        abs_z = base_z + offset
        
        # Convert to workplane local coordinates
        # Local X: 0 (Centered on the face width)
        # Local Y: Relative Z from center of face
        loc_y = abs_z - face_center_z
        hole_points.append((0, loc_y))

# 3. Cut the square holes
result = (
    result
    .faces("<Y")                                 # Select the front face (normal -Y)
    .workplane(centerOption="CenterOfBoundBox")  # Set workplane to center of face
    .pushPoints(hole_points)                     # Push all calculated hole centers
    .rect(hole_size, hole_size)                  # Sketch square holes
    .cutThruAll()                                # Cut through the material
)