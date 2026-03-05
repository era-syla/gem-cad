import cadquery as cq

# Parametric dimensions
# Base block dimensions
base_width = 10.0
base_height = 15.0
base_thickness = 4.0

# Horizontal beam dimensions
h_beam_length = 30.0  # total length
h_beam_height = 5.0
h_beam_thickness = 4.0

# Vertical tower dimensions
tower_height = 25.0
tower_width = 4.0
tower_thickness = 4.0

# Curved arm dimensions
arm_length = 12.0
arm_height = 6.0
arm_thickness = 2.0  # Thinner than main body
arm_radius = arm_height / 2.0

# Small protrusion on tower
knob_size = 3.0
knob_offset_top = 8.0

# Bottom cutout dimensions
cutout_width = 3.0
cutout_height = 6.0
cutout_offset = 5.0

# --- Construction ---

# 1. Main Horizontal Beam
# Create a centered horizontal bar
h_beam = cq.Workplane("XY").box(h_beam_length, h_beam_thickness, h_beam_height)

# 2. Lower Main Body (The block below the beam)
# Positioned somewhat centrally, extending downwards
lower_body = (
    cq.Workplane("XY")
    .workplane(offset=-h_beam_height/2)  # Start at bottom of beam
    .center(0, 0)
    .box(base_width + 4, base_thickness, base_height, centered=(True, True, False))
    .translate((0, 0, -base_height)) # Move it entirely below
)

# 3. Vertical Tower
# Extends upwards from the horizontal beam, offset to the right
tower = (
    cq.Workplane("XY")
    .workplane(offset=h_beam_height/2)  # Start at top of beam
    .center(h_beam_length/6, 0)         # Shift right
    .box(tower_width, tower_thickness, tower_height, centered=(True, True, False))
)

# 4. Curved Arm
# Extends to the left from the tower
# It has a rounded end
arm_sk = (
    cq.Workplane("XZ")
    .workplane(offset=-arm_thickness/2) # Center the thinner arm
    .moveTo(h_beam_length/6 - tower_width/2, h_beam_height/2 + 5) # Start at tower face
    .lineTo(h_beam_length/6 - tower_width/2 - arm_length, h_beam_height/2 + 5)
    .threePointArc(
        (h_beam_length/6 - tower_width/2 - arm_length - arm_radius, h_beam_height/2 + 5 + arm_radius),
        (h_beam_length/6 - tower_width/2 - arm_length, h_beam_height/2 + 5 + arm_height)
    )
    .lineTo(h_beam_length/6 - tower_width/2, h_beam_height/2 + 5 + arm_height)
    .close()
    .extrude(arm_thickness)
)

# 5. Small Knob on Tower
knob = (
    cq.Workplane("YZ")
    .workplane(offset=h_beam_length/6 + tower_width/2) # On the right face of tower (relative to origin, but visual left in ISO)
    # Actually, looking at the image, the knob is on the "front" face relative to the arm
    # Let's place it on the front face (negative Y)
)

knob = (
    cq.Workplane("XZ")
    .workplane(offset=-tower_thickness/2) # Front face
    .center(h_beam_length/6, h_beam_height/2 + 10 + knob_size/2) # Position up the tower
    .box(knob_size, knob_size, 2.0, centered=(True, True, False)) # Extrude out
    .translate((0,0,0)) # dummy
)

# Refine the lower body to match the stepped look
# We'll create the main blocky shape by unioning specific blocks rather than subtracting complexly
# Let's restart the "result" composition for clarity based on visual parsing

# Visual parsing:
# Center origin at the intersection of the main horizontal bar and the vertical tower.

# Main Vertical Post (Tower + downward extension)
vertical_post = cq.Workplane("XY").box(4, 4, 50).translate((5, 0, 5)) 

# Horizontal Bar intersecting
horiz_bar = cq.Workplane("XY").box(30, 4, 6).translate((-5, 0, 0))

# The lower big plate section
lower_plate = cq.Workplane("XY").box(20, 4, 12).translate((-2, 0, -9))

# Combine basics
part = vertical_post.union(horiz_bar).union(lower_plate)

# Add the arm
arm = (
    cq.Workplane("XY")
    .workplane(offset=3) # Start slightly above center
    .moveTo(3, -2)       # Start at side of tower, back face
    .lineTo(-8, -2)      # Go left
    .threePointArc((-11, 0), (-8, 2)) # Round end
    .lineTo(3, 2)        # Back to tower
    .close()
    .extrude(6)          # Height of arm
    .translate((0, 0, 5)) # Move up
)
# The arm in image is thin. Let's fix that.
# Redoing arm with correct orientation (XZ plane extrusion is easier for profile)
arm_geo = (
    cq.Workplane("XZ")
    .moveTo(3, 8)       # At tower wall
    .lineTo(-6, 8)      # Extend left
    .threePointArc((-9, 11), (-6, 14)) # Arc up
    .lineTo(3, 14)      # Back to tower
    .close()
    .extrude(2)         # Thinness
    .translate((0, -1, 0)) # Center on Y (thickness direction)
)

part = part.union(arm_geo)

# Add the small square knob on the tower
knob = (
    cq.Workplane("XY")
    .box(3, 1.5, 3)
    .translate((5, -2.75, 18)) # Position on front face of tower
)
part = part.union(knob)

# Add the tiny tab on top of the arm
tiny_tab = (
    cq.Workplane("XY")
    .box(1, 3, 0.5)
    .translate((-5, 0, 14.25))
)
part = part.union(tiny_tab)


# Cuts
# Bottom slot
part = part.cut(
    cq.Workplane("XY")
    .box(3, 5, 6)
    .translate((-8, 0, -15)) # Left side bottom
)

# Right side notch on the horizontal bar
part = part.cut(
    cq.Workplane("XY")
    .box(4, 5, 4)
    .translate((12, 0, -4)) # Right bottom corner
)

# Slot in the middle of the assembly (where pieces join)
part = part.cut(
    cq.Workplane("XY")
    .box(1, 5, 6)
    .translate((3, 0, -4)) # Vertical slit
)

# Final adjustments to match the specific "staggered" look of the bottom
# Left bottom creates a "foot"
foot_extension = (
    cq.Workplane("XY")
    .box(4, 4, 4)
    .translate((-10, 0, -8))
)
part = part.union(foot_extension)

# Recut the bottom slot more accurately
part = part.cut(
    cq.Workplane("XY")
    .box(2.5, 5, 8)
    .translate((-6, 0, -12))
)

result = part