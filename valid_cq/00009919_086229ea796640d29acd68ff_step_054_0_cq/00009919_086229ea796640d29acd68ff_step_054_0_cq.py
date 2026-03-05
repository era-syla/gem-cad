import cadquery as cq

# Parameters
width = 100.0       # Center-to-center horizontal distance between legs
height = 50.0       # Overall height of the handle
thickness = 10.0    # Cross-sectional width and thickness of the handle bar
foot_length = 20.0  # Length of the mounting feet
hole_diameter = 5.0 # Diameter of the mounting holes

# Derived dimensions
outer_width = width + thickness
inner_width = width - thickness
outer_height = height
inner_height = height - thickness

# Create the main handle profile
# We will sketch the path on the XZ plane and sweep or extrude.
# Alternatively, and simpler for this shape: Build it out of primitive shapes or a single sketch extrusion.

# Let's use a 2D profile sketch approach which is robust.
# We'll draw the side profile (an inverted U shape with feet) on the XZ plane
# and extrude it by the thickness.

sketch = (
    cq.Workplane("XZ")
    .moveTo(-width/2 - foot_length, 0) # Start at the outer tip of the left foot
    .lineTo(-width/2 - foot_length, thickness) # Up foot thickness
    .lineTo(-width/2 - thickness, thickness) # Back to the vertical leg
    .lineTo(-width/2 - thickness, height - thickness) # Up the inside of the vertical leg
    .lineTo(-width/2, height - thickness) # Jog in? No, let's rethink. It's a simple bent bar.
)

# Better approach: Path sweep or simple union of boxes.
# Let's try the union of boxes approach for clarity and parametric simplicity.
# It consists of: 1 Top Bar, 2 Vertical Legs, 2 Feet.

# 1. Top Bar
top_bar = cq.Workplane("XY").box(width + thickness, thickness, thickness)
# Move top bar up to correct height
top_bar = top_bar.translate((0, 0, height - thickness/2))

# 2. Vertical Legs
# Left Leg
left_leg = cq.Workplane("XY").box(thickness, thickness, height - thickness)
left_leg = left_leg.translate((-width/2, 0, (height - thickness)/2))

# Right Leg
right_leg = cq.Workplane("XY").box(thickness, thickness, height - thickness)
right_leg = right_leg.translate((width/2, 0, (height - thickness)/2))

# 3. Feet
# Left Foot
left_foot = cq.Workplane("XY").box(foot_length, thickness, thickness)
# Position: The foot extends outwards from the leg.
# Center of foot needs to be offset
foot_center_x = -width/2 - thickness/2 - foot_length/2 + thickness # Overlap slightly or align faces?
# Let's align faces. Leg outer face is at -width/2 - thickness/2.
# Foot starts there and goes left.
left_foot = left_foot.translate((-width/2 - foot_length/2, 0, thickness/2))

# Right Foot
right_foot = cq.Workplane("XY").box(foot_length, thickness, thickness)
right_foot = right_foot.translate((width/2 + foot_length/2, 0, thickness/2))

# Combine all parts
handle = top_bar.union(left_leg).union(right_leg).union(left_foot).union(right_foot)

# Add Holes to the feet
# We need to find the center of the exposed part of the foot.
# The foot sticks out `foot_length` amount (assuming the box definition included the part under the leg? No, let's refine).

# Let's Refine Geometry Construction for cleaner logic using a Polyline extrusion.
# This creates a solid profile and extrudes it. This is usually cleaner in CadQuery.

pts = [
    (-width/2 - foot_length, 0),          # Start bottom-left of left foot
    (-width/2 - foot_length, thickness),  # Top-left of left foot
    (-width/2 - thickness, thickness),    # Top-right of left foot / start of leg inner curve
    (-width/2 - thickness, height - thickness), # Inner corner left
    (width/2 + thickness, height - thickness),  # Inner corner right
    (width/2 + thickness, thickness),     # Top-left of right foot
    (width/2 + foot_length, thickness),   # Top-right of right foot
    (width/2 + foot_length, 0),           # Bottom-right of right foot
    (width/2, 0),                         # Bottom of right leg
    (width/2, height - 2*thickness),      # THIS LOGIC IS GETTING COMPLEX with straight lines.
]

# Let's stick to the most robust method: Constructive Solid Geometry (CSG) with precise coordinates.
# Re-defining parameters to be super clear.

# Dimensions
handle_span = 80.0      # Distance between vertical pillars (inner)
handle_height = 50.0    # Total Z height
bar_section = 10.0      # Square cross section of the bar
foot_extension = 15.0   # How far the foot sticks out past the vertical pillar

# Calculation for centers
# Let's place the origin at the center of the span on the ground (Z=0)

# 1. The main U-shape (Top + 2 Vertical legs)
# We can create a solid U-shape by cutting a smaller box from a larger box.
outer_box_width = handle_span + 2 * bar_section
outer_box_height = handle_height

inner_box_width = handle_span
inner_box_height = handle_height - bar_section

u_shape = (
    cq.Workplane("XZ")
    .box(outer_box_width, outer_box_height, bar_section, centered=(True, False, True)) # Create huge block
    .cut(
        cq.Workplane("XZ")
        .workplane(offset=-bar_section) # Move to cut through
        .center(0, 0)
        .box(inner_box_width, inner_box_height, bar_section*3, centered=(True, False, True)) # Cutout
    )
)

# 2. Add the feet
# Left foot
left_foot_center = -handle_span/2 - bar_section - foot_extension/2
left_foot = (
    cq.Workplane("XY")
    .workplane(offset=bar_section/2) # Center Z at half thickness
    .center(left_foot_center + bar_section/2, 0) # Adjust X center
    .box(foot_extension, bar_section, bar_section)
)

# Right foot
right_foot_center = handle_span/2 + bar_section + foot_extension/2
right_foot = (
    cq.Workplane("XY")
    .workplane(offset=bar_section/2)
    .center(right_foot_center - bar_section/2, 0)
    .box(foot_extension, bar_section, bar_section)
)

# Join basic shape
result = u_shape.union(left_foot).union(right_foot)

# 3. Add Holes
# Locate the center of the foot extension area
hole_offset = (handle_span/2 + bar_section + foot_extension/2)

result = (
    result.faces("<Z")
    .workplane()
    .pushPoints([
        (-hole_offset, 0),
        (hole_offset, 0)
    ])
    .hole(hole_diameter)
)

# Refinement: The image shows the foot merging flush with the outer edge of the vertical leg,
# but usually, these handles have the foot extending OUTWARDS from the leg.
# The code above produces feet extending outwards.

# Let's ensure the "U" sits on the ground properly.
# The initial U-shape box was created on XZ plane, centered X, Z starting 0? 
# "centered=(True, False, True)" means X is centered, Y (which is Z in global) starts at 0, Z (which is Y global) is centered.
# Wait, XZ plane: X is global X, Y is global Z.
# Box(w, h, thickness). 
# We want X centered. Y (global Z) starts 0. Thickness (global Y) centered.
# This puts the bottom of the handle at Z=0.

# Corrected U-Shape logic to ensure it's simple and 100% matches image orientation.

# Final Logic Block
total_width = 100.0
total_height = 60.0
section = 12.0
foot_len = 20.0 # Extension beyond the vertical leg

# 1. Create the path for the handle
path = (
    cq.Workplane("XZ")
    .moveTo(-total_width/2, 0)
    .lineTo(-total_width/2, total_height - section/2)
    .lineTo(total_width/2, total_height - section/2)
    .lineTo(total_width/2, 0)
)

# 2. Sweep a square profile along the path
# Note: CadQuery sweep can be finicky with sharp corners without a fillet or disjoint parts.
# Let's go back to the union of blocks, it is fail-safe for this geometry.

# Left Vertical
l_vert = cq.Workplane("XY").box(section, section, total_height).translate((-total_width/2, 0, total_height/2))
# Right Vertical
r_vert = cq.Workplane("XY").box(section, section, total_height).translate((total_width/2, 0, total_height/2))
# Top Bar
top = cq.Workplane("XY").box(total_width + section, section, section).translate((0, 0, total_height - section/2))

# Left Foot (extending outwards)
l_foot = cq.Workplane("XY").box(foot_len, section, section).translate((-total_width/2 - section/2 - foot_len/2, 0, section/2))
# Right Foot (extending outwards)
r_foot = cq.Workplane("XY").box(foot_len, section, section).translate((total_width/2 + section/2 + foot_len/2, 0, section/2))

result = l_vert.union(r_vert).union(top).union(l_foot).union(r_foot)

# Holes
# Calculate center of the foot extension
l_hole_x = -total_width/2 - section/2 - foot_len/2
r_hole_x = total_width/2 + section/2 + foot_len/2

result = (
    result.faces("<Z").workplane()
    .pushPoints([(l_hole_x, 0), (r_hole_x, 0)])
    .hole(hole_diameter)
)