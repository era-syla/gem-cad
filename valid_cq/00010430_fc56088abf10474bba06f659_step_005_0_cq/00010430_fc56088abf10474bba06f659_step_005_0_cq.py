import cadquery as cq
import math

# --- Parameters ---
base_width = 15.0
base_depth = 20.0
base_height = 8.0

vertical_height = 80.0
thickness = 6.0
rib_thickness = 3.0
rib_height = 30.0

top_angle = 30.0  # Angle of the top bent part
top_length = 15.0

hole_diameter = 4.0
hole_center_offset = 6.0  # From front edge

fillet_radius = 1.0
top_fillet = 1.5

# --- Construction ---

# 1. Base Block
# We start by building the L-shape profile from the side view and extruding it
# Or we can build components and union them. Let's do the vertical arm + base.

# Define the vertical beam
vertical_beam = (
    cq.Workplane("XY")
    .box(base_width, thickness, vertical_height, centered=(True, False, False))
)

# Define the base protruding forward
base_extension = (
    cq.Workplane("XY")
    .workplane(offset=0) # Reset to ground
    .center(0, thickness) # Move to front of beam
    .box(base_width, base_depth - thickness, base_height, centered=(True, False, False))
)

# Combine base parts
main_body = vertical_beam.union(base_extension)


# 2. Angled Top Section
# We need to add material at the top at an angle.
# We'll create a sketch on the top face of the vertical beam and extrude along a vector or loft.
# Easier method: Create a new workplane at the top, rotate it, and extrude.

# Find the top face center point
top_face_center = (0, thickness/2.0, vertical_height)

angled_top = (
    cq.Workplane("XZ")
    .transformed(offset=(0, vertical_height, -thickness/2.0)) # Position at top back corner
    .transformed(rotate=(0, -top_angle, 0)) # Rotate coordinates (CadQuery rotation axis logic can be tricky, testing visualization mental model)
    # Let's try a simpler approach: Draw the profile of the top bent part on the side plane (YZ) and extrude.
)

# Alternative approach for the whole L-shape + Angle:
# Draw side profile on YZ plane.
pts = [
    (0, 0),
    (base_depth, 0),
    (base_depth, base_height),
    (thickness, base_height), # Inner corner of L
    (thickness, vertical_height),
    # Calculate top point based on angle
    (thickness + top_length * math.sin(math.radians(top_angle)), vertical_height + top_length * math.cos(math.radians(top_angle))),
    # Go back by thickness (perpendicular to the angle)
    # This is getting complex mathematically. Let's stick to constructive solid geometry (CSG).
]

# Let's go back to the top piece construction.
# Create a plane at the top of the vertical beam.
top_plane = (
    main_body.faces(">Z").workplane()
    .transformed(rotate=(top_angle, 0, 0)) # Rotate around X axis to tilt forward/backward
)

# Since the rotation is likely around the front or back edge, let's be specific.
# The bend creates a "knee".
# Let's create the angled top as a separate box and unite/position it.

# Calculate geometry for the angled top
# We want it to tilt "forward" (towards -Y relative to the back face, or +Y depending on orientation).
# Looking at the image, the base sticks out "forward". The top tilts "backward" (away from the base direction) or "forward"?
# Image analysis: The base has ribs. The vertical part goes up. The top tilts in the OPPOSITE direction of the base extension.
# Base extends +Y (relative to back wall). Top tilts -Y.

# Let's refine the coordinate system:
# Origin: Bottom center of the back face.
# X: Width
# Y: Depth (Forward)
# Z: Height

main_body = (
    cq.Workplane("XY")
    .box(base_width, thickness, vertical_height, centered=(True, False, False)) # Vertical wall
    .faces("<Y").workplane() # Front face (actually this is the back face if Y is depth, let's fix centering)
)

# Re-orient:
# X: Left/Right
# Y: Front/Back (Positive is Front)
# Z: Up/Down

# Vertical spine
spine = cq.Workplane("XY").box(base_width, thickness, vertical_height, centered=(True, False, False))

# Base "foot" extending forward (+Y)
foot = (
    cq.Workplane("XY")
    .center(0, thickness/2.0) # Start from front face of spine
    .box(base_width, base_depth - thickness/2.0, base_height, centered=(True, False, False))
)

structure = spine.union(foot)

# Angled top
# It bends "backwards" (towards -Y)
# Create a workplane on the top face of the spine
top_stub = (
    cq.Workplane("YZ")
    .workplane(offset=base_width/2.0)
    .moveTo(thickness/2.0, vertical_height)
    .lineTo(-thickness/2.0, vertical_height)
    .lineTo(-thickness/2.0 - top_length * math.sin(math.radians(top_angle)), vertical_height + top_length * math.cos(math.radians(top_angle)))
    .lineTo(thickness/2.0 - top_length * math.sin(math.radians(top_angle)), vertical_height + top_length * math.cos(math.radians(top_angle)))
    .close()
    .extrude(-base_width)
)

structure = structure.union(top_stub)

# 3. Ribs (Triangular supports)
# Two ribs connecting the vertical spine to the base foot.
# They are thin walls on the left and right sides.

rib_shape = (
    cq.Workplane("YZ")
    .moveTo(thickness/2.0, base_height)
    .lineTo(thickness/2.0 + (base_depth - thickness), base_height)
    .lineTo(thickness/2.0, base_height + rib_height)
    .close()
    .extrude(rib_thickness) # Extrude creates volume in X
)

# Position Rib 1 (Left)
rib1 = rib_shape.translate((-base_width/2.0, 0, 0))

# Position Rib 2 (Right) - needs to be moved to the other side
# Since extrude goes positive normal, rib1 is sticking out from -width/2 towards center.
# We want it flush with the edge.
rib1 = rib_shape.translate((-base_width/2.0, 0, 0))
rib2 = rib_shape.translate((base_width/2.0 - rib_thickness, 0, 0))

structure = structure.union(rib1).union(rib2)


# 4. Hole
# Hole is in the base foot, centered between ribs.
hole_y_pos = thickness/2.0 + (base_depth - thickness)/2.0
# Actually, looking at the image, the hole is near the front edge.
hole_y_pos = (thickness/2.0) + (base_depth - thickness) - hole_center_offset

structure = (
    structure.faces(">Z").workplane()
    .center(0, hole_y_pos) # This coordinate depends heavily on face selection logic, safer to use absolute
)

# Re-do hole with absolute coordinates on base plane
structure = (
    structure.cut(
        cq.Workplane("XY")
        .center(0, (base_depth - thickness/2.0) - hole_center_offset + thickness/2.0) # Absolute Y
        .circle(hole_diameter/2.0)
        .extrude(base_height * 2) # Cut through
    )
)

# 5. Fillets
# Top of the angled piece is rounded
structure = structure.edges(">Z").fillet(top_fillet)

# Optional: Fillet the bend connection to make it smoother like the image
# Find the edge at Z=vertical_height
try:
    structure = structure.edges(cq.selectors.BoxSelector(
        (-base_width, -thickness*2, vertical_height - 1),
        (base_width, thickness*2, vertical_height + 1)
    )).fillet(fillet_radius)
except:
    pass # Skip if selection is tricky

result = structure