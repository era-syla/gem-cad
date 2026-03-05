import cadquery as cq

# --- Parametric Dimensions ---
# Base plate
base_length = 80.0
base_width = 30.0
base_thickness = 2.0

# Central Latch Body
latch_length = 35.0
latch_width = 18.0
latch_height = 12.0
latch_fillet_radius = 2.0

# Side wings (The curvy parts)
wing_length = 15.0
wing_width = latch_width  # Same width as the main body
wing_height = 8.0

# Hinge/Pin details
pin_hole_diameter = 3.0
pin_boss_height = 8.0 # From the base

# Hook detail (the protruding part on the right)
hook_length = 10.0
hook_height = 10.0

# --- Geometry Construction ---

# 1. Base Plate
# Simple rectangular extrusion
base = cq.Workplane("XY").box(base_length, base_width, base_thickness)

# 2. Main Central Body (The boxy part in the middle)
# We'll create this on top of the base.
# It seems slightly raised or separate, but usually, these are molded or welded.
# Let's place it centered relative to width, but offset slightly in length to accommodate wings.
center_body = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness/2)
    .box(latch_length, latch_width, latch_height, centered=(True, True, False))
)

# Add fillets to the top edges of the central body for that smooth look
center_body = center_body.edges("|Z").fillet(1.0)
center_body = center_body.edges(">Z").fillet(1.0)

# Create the side hole in the main body
center_body = (
    center_body.faces(">Y")
    .workplane()
    .hole(pin_hole_diameter)
)

# 3. The "Wavy" Side Wings (Left Side)
# This requires a sketch profile extruded sideways or lengthwise.
# Looking at the profile, it goes up, rounds over, goes down, steps up again.
# Let's sketch it on the XZ plane (side view) and extrude.

def make_wing_profile(length, height_low, height_high):
    # A custom profile for the wavy shape
    pts = [
        (0, 0),
        (0, height_low),
        (length/3, height_low), # First step
        (length/3, height_high), # Rise
        (length*0.8, height_high), # Top flat
        (length, height_low * 0.5), # Slope down
        (length, 0)
    ]
    return cq.Workplane("XZ").polyline(pts).close()

# The left wing seems to be composed of two "fingers" or just a grooved profile.
# Let's model it as a solid block first, then cut the groove.
wing_left_start_x = -latch_length/2
wing_solid = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness/2)
    .center(wing_left_start_x - wing_length/2, 0)
    .box(wing_length, wing_width, wing_height, centered=(True, True, False))
)

# Apply heavy fillets to simulate the organic wavy shape
# We need to fillet the top edges running along Y
wing_solid = wing_solid.edges(">Z and |Y").fillet(3.0)

# Now, create the split in the middle of the wing
wing_split = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness/2)
    .center(wing_left_start_x - wing_length/2, 0)
    .box(wing_length + 2, 2.0, wing_height + 5, centered=(True, True, False)) # Thin cut
)
wing_solid = wing_solid.cut(wing_split)


# 4. The Right Side Hook/Hinge
# This looks like a hook mechanism.
hook_start_x = latch_length/2
hook_solid = (
    cq.Workplane("XZ")
    .workplane(offset=-latch_width/2) # Start at side
    .center(hook_start_x, base_thickness/2)
    .lineTo(5, 0)
    .lineTo(5, 5)
    .threePointArc((8, 8), (10, 5)) # The hook curve
    .lineTo(10, 0)
    .close()
    .extrude(latch_width)
)

# 5. Assemble and Refine
# Combine all parts
part = base.union(center_body).union(wing_solid).union(hook_solid)

# Add the specific "Overhang" detail on the main body
# The main body seems to have a thin shell overlapping the side wings.
# We will simulate this by creating a slightly larger shell and intersecting or unioning.
shell_thickness = 1.0
top_plate = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness/2 + latch_height)
    .box(latch_length + 4, latch_width + 1.0, 1.0, centered=(True,True,False)) # Thin top plate
)
# Add side flaps to the top plate
side_flap_Right = (
     cq.Workplane("YZ")
     .workplane(offset=latch_length/2)
     .center(0, base_thickness/2 + latch_height/2)
     .box(latch_width + 1.0, latch_height, 1.0, centered=(True, True, True))
)
side_flap_Left = (
     cq.Workplane("YZ")
     .workplane(offset=-latch_length/2 - 2) # Slightly offset to cover the wing start
     .center(0, base_thickness/2 + latch_height/2 - 2)
     .box(latch_width + 1.0, latch_height - 4, 1.0, centered=(True, True, True))
)

part = part.union(top_plate)

# Final fillets to smooth transitions where possible without breaking geometry
# Select edges near the base connection
try:
    part = part.edges(f"(>Z[{base_thickness-0.1}] and <Z[{base_thickness+0.1}])").fillet(0.5)
except:
    pass # Skip if selection is tricky

# Create the final result variable
result = part