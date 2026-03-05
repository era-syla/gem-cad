import cadquery as cq

# --- Parameters ---
# Main block dimensions
base_width = 42.0
base_height = 35.0 # Total height roughly
base_thickness = 14.0
flange_height = 6.0 # Height of the side mounting flanges

# Center hole (shaft support)
center_bore_diam = 20.0
center_bore_depth = 8.0 # Recess depth
through_hole_diam = 8.0

# Mounting holes
mount_hole_spacing = 32.0
mount_hole_diam = 5.5
counterbore_diam = 9.0
counterbore_depth = 4.0

# Chamfers
top_chamfer = 2.0
side_chamfer = 1.0

# --- Geometry Construction ---

# 1. Create the main profile
# We'll sketch the front face profile and extrude it.
# The profile looks like a rectangle with "shoulders".

# Calculate half-width for symmetry
w_half = base_width / 2.0
h_total = base_height
h_flange = flange_height

# Define the points for the main outline
pts = [
    (-w_half, 0),             # Bottom left
    (w_half, 0),              # Bottom right
    (w_half, h_flange),       # Flange top right
    (w_half * 0.5, h_flange), # Shoulder right (approximate width for central block)
    (w_half * 0.5, h_total),  # Top right
    (-w_half * 0.5, h_total), # Top left
    (-w_half * 0.5, h_flange),# Shoulder left
    (-w_half, h_flange)       # Flange top left
]

# Create the base solid
base = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(base_thickness)
)

# 2. Add Chamfers
# The top edges of the central block are chamfered.
# Find edges at the top Z level and filter by Y position to get the top corners.
result = (
    base
    .edges("|Y") # Select edges parallel to Y axis (extrusion direction was Z, but sketch was XY, wait...)
    # Let's re-orient. Sketch on XY, extruded in Z.
    # The "top" of the part in the image corresponds to +Y in the sketch.
    # The chamfered edges are the ones at the very top of the geometry.
    .edges(">Y") # Edges at the max Y coordinate
    .chamfer(top_chamfer)
)

# 3. Create the center bore
# The image shows a large circular recess and a smaller through hole.
# We'll work on the front face (min Z in our current orientation, or max Z depending on preference).
# Let's assume the sketch was on Z=0 and we extruded to +Z=14. The "front" is Z=14.
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, h_total/2.0) # Move center roughly to the middle of the main block part. 
                            # Actually, typically these are centered on a specific shaft height.
                            # Let's center it vertically relative to the main block section.
    .moveTo(0, 0) # Relative to workplane center.
    # Let's position it absolutely. Center of block is Y = h_total/2 roughly? 
    # Usually SK blocks have a specific shaft height 'h'. Let's pick a reasonable one based on geometry.
    # Let's assume the center is at Y = 20.0 from bottom.
    .center(0, - (h_total/2.0) + 21.0) # Adjusting workplane center to specific height
    .circle(center_bore_diam / 2.0)
    .cutBlind(-center_bore_depth)
)

# 4. Create the center through hole
result = (
    result
    .faces(">Z")
    .workplane()
    # Need to find that center again. The previous workplane stack is tricky.
    # Easiest to reference absolute coordinates.
    .moveTo(0, 21.0) 
    .hole(through_hole_diam)
)

# 5. Create mounting holes on the flanges
# These are on the side flanges (height ~6mm).
# They need counterbores.
result = (
    result
    .faces(">Z")
    .workplane()
    .moveTo(-mount_hole_spacing/2.0, h_flange/2.0)
    .cboreHole(mount_hole_diam, counterbore_diam, counterbore_depth)
    .moveTo(mount_hole_spacing/2.0, h_flange/2.0)
    .cboreHole(mount_hole_diam, counterbore_diam, counterbore_depth)
)

# 6. Apply remaining fillets/chamfers to match image style
# There is a slight chamfer/fillet on the vertical edges of the central block
# that transition to the flanges.
# Let's add a small chamfer to the outer vertical edges.
result = (
    result
    .edges("|Z")  # Vertical edges
    .filter(lambda e: e.Center().y > h_flange + 0.1) # Only the upper block part
    .chamfer(side_chamfer)
)

# Rotate for better viewing orientation matching the image
# (The image shows the part standing up, Z-up, front face towards -Y or similar)
# Our model was built flat on XY. Let's rotate it to stand up.
result = result.rotate((0,0,0), (1,0,0), 90)