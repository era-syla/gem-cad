import cadquery as cq
import math

# --- Parameters ---
outer_radius = 50.0       # Radius of the outer edge
width = 5.0               # Width of the ring section
thickness = 1.0           # Thickness of the base plate
arc_angle = 240.0         # Total angle of the arc
stud_diameter = 3.0       # Diameter of the small studs
stud_height = 1.0         # Height of the studs above the plate
num_studs = 20            # Number of small cylindrical studs
block_width = 4.0         # Width of the larger block feature
block_height = 4.0        # Height of the larger block feature
block_angle_pos = 0.0     # Angle position of the block (relative to center of arc)

# Calculated parameters
inner_radius = outer_radius - width
mid_radius = (inner_radius + outer_radius) / 2.0

# --- Geometry Construction ---

# 1. Create the base arc (the "C" shape)
# We create a full ring and cut it, or extrude a sketch. Let's extrude a sketch.
# To make the tips pointy/tapered as seen in the image, simple concentric arcs might not be enough.
# Looking closely, the inner and outer arcs seem to have different centers or radii that intersect.
# However, a standard ring sector is a good approximation. Let's refine the "crescent" shape.
# A true crescent is formed by two offset circles.
# Let's try an offset circle approach to get the tapered ends.

# Shift calculation for crescent shape
# If we shift the inner circle, we get a crescent.
shift_amount = width * 0.8
crescent_outer_r = outer_radius
crescent_inner_r = outer_radius - width 

# Create the base plate using a boolean subtraction of cylinders to get the crescent
# Then intersect with a pie wedge to limit the angle.
base_plate = (
    cq.Workplane("XY")
    .circle(crescent_outer_r)
    .extrude(thickness)
    .cut(
        cq.Workplane("XY")
        .center(shift_amount, 0) # Shift the inner cutting cylinder to create tapered ends
        .circle(crescent_inner_r)
        .extrude(thickness)
    )
)

# Now cut the crescent to the specific arc length needed. 
# The image shows an opening.
# A box cut is simplest.
cut_box_size = outer_radius * 2.5
cut_box = (
    cq.Workplane("XY")
    .rect(cut_box_size, cut_box_size)
    .extrude(thickness)
    .translate((-cut_box_size/2 - (inner_radius * 0.2), 0, 0)) # Position to keep the right side
)

# Actually, a more precise way to match the image which looks like a C-ring with tapered ends:
# It looks like a standard ring segment where the ends might just be cut, but the "crescent" logic 
# creates the tapering naturally. Let's stick with the offset circles which creates a nice crescent.
# The image shows the gap is on the left.
result = base_plate.cut(cut_box)

# 2. Add the small cylindrical studs
# They follow the curvature. We need to place them along an arc.
# The path seems to be roughly centered on the crescent.

# Calculate positions
studs = cq.Workplane("XY")

# The arc covers roughly -110 to +110 degrees on the right side.
start_angle = -85
end_angle = 85
angle_step = (end_angle - start_angle) / (num_studs - 1)

for i in range(num_studs):
    # Calculate angle for this stud
    current_angle_deg = start_angle + (i * angle_step)
    current_angle_rad = math.radians(current_angle_deg)
    
    # Calculate radius at this angle for placement
    # Since it's a crescent (offset circles), the "center line" radius varies.
    # Simple approximation: geometric mean or linear interpolation between circle boundaries.
    # Outer circle is at (0,0) radius R_out
    # Inner circle is at (shift, 0) radius R_in
    # We want to be somewhat in the middle.
    
    # Ray casting to find thickness center at this angle:
    # Outer point: (R_out * cos(theta), R_out * sin(theta))
    # We need to ensure we are well inside the solid.
    
    # Let's try placing them on a slightly offset circular path that tracks the visual center.
    r_placement = outer_radius - (width / 2.0) - (shift_amount/2 * math.cos(current_angle_rad))
    
    x = r_placement * math.cos(current_angle_rad)
    y = r_placement * math.sin(current_angle_rad)
    
    # Create the stud
    stud = (
        cq.Workplane("XY")
        .center(x, y)
        .circle(stud_diameter / 2.0)
        .extrude(thickness + stud_height)
    )
    # Add to result (union)
    result = result.union(stud)

# 3. Add the larger block feature
# It looks located near the bottom of the "C" (negative Y), interrupting the studs.
# In the image, there is a distinct block near one end of the stud array.
# Let's place it at a specific angle, say -50 degrees.

block_angle = -55
block_angle_rad = math.radians(block_angle)
r_block = outer_radius - (width / 2.0) - (shift_amount/2 * math.cos(block_angle_rad))
bx = r_block * math.cos(block_angle_rad)
by = r_block * math.sin(block_angle_rad)

# Create the block. It looks like a "D" shape or a rectangular block with a rounded top,
# matching the curvature. Let's make a simple box for robustness.
block_feature = (
    cq.Workplane("XY")
    .center(bx, by)
    .rect(block_width, width * 1.2) # Make it wide enough to cover the width
    .extrude(thickness + block_height)
    .rotate((bx, by, 0), (bx, by, 1), block_angle) # Align with radius
)

# Intersect the block with the base shape extruded higher to ensure it matches the crescent footprint perfectly
# Create a prism of the base shape
base_prism = (
    cq.Workplane("XY")
    .circle(crescent_outer_r)
    .extrude(thickness + block_height)
    .cut(
        cq.Workplane("XY")
        .center(shift_amount, 0)
        .circle(crescent_inner_r)
        .extrude(thickness + block_height)
    )
    .cut(cut_box.faces("<Z").extrude(thickness + block_height)) # Apply the same cut
)

# Create the specific block shape by intersection
shaped_block = base_prism.intersect(block_feature)

result = result.union(shaped_block)

# Optional: Add Fillets if needed, but image looks sharp/low-poly. 
# We leave it sharp as per standard mechanical CAD practice unless specified.

# Export or Display
if 'show_object' in globals():
    show_object(result)