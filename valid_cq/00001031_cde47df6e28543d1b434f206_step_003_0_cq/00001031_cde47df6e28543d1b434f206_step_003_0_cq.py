import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions
length = 80.0
width_outer = 30.0
height_outer = 12.0
wall_thickness = 1.5

# Main arc calculations
radius_outer = 20.0 # Curvature of the shell

# Internal structure positions
septum_offset = 10.0 # From the center, where the solid wall divides the two sections
boss_pos_x = 20.0    # Position of the screw boss
catch_pos_x = 32.0   # Position of the latch mechanism

# Screw Boss dimensions
boss_outer_r = 3.0
boss_inner_r = 1.2
boss_height = 6.0

# Latch/Hook dimensions
latch_block_w = 4.0
latch_block_l = 6.0
latch_block_h = 5.0
latch_hole_r = 2.0

# --- Geometry Construction ---

# 1. Base Shell (The curved main body)
# We'll create a profile and extrude it.
# The profile is an arc with thickness.

def make_shell_profile(radius, thickness, width):
    """Creates the 2D cross-section of the curved shell."""
    # Calculate angles or height based on width and radius
    # Assuming a segment of a circle
    
    # We will create a sketch that is an arc offset by thickness
    s = (
        cq.Sketch()
        .arc((0, 0), radius, 0.0, 180.0) # Start with a full half-circle for simplicity
        .offset(thickness)
    )
    
    # Now we need to trim it to the specific width/height we want. 
    # Instead of complex trimming, let's build it by cutting a solid block with a cylinder.
    return None # Strategy shift: Boolean operations are easier for this shape.

# Strategy Shift: Create a solid block, cut the bottom curve, shell it or cut the inner curve.

# Step 1: Create the main outer shape
# It looks like a semi-cylindrical shape but flattened.
# Let's create a cylinder sector.

# Create a solid block representing the bounding box first
# Then cut away the material to form the arch.
outer_profile = (
    cq.Workplane("YZ")
    .moveTo(width_outer/2, 0)
    .threePointArc((0, height_outer), (-width_outer/2, 0))
    .close()
    .extrude(length)
)

# Step 2: Hollow out the inside to create the shell
# We subtract a slightly smaller version of the profile.
inner_profile = (
    cq.Workplane("YZ")
    .moveTo(width_outer/2 - wall_thickness, 0)
    .threePointArc((0, height_outer - wall_thickness), (-(width_outer/2 - wall_thickness), 0))
    .lineTo(-(width_outer/2 - wall_thickness), -10) # Extend down to ensure cut
    .lineTo(width_outer/2 - wall_thickness, -10)
    .close()
    .extrude(length)
)

shell = outer_profile.cut(inner_profile)

# Center the shell on the origin for easier feature placement
shell = shell.translate((-length/2, 0, 0))

# Step 3: Add the septum (divider wall)
# The image shows a wall dividing the smooth part from the detailed part.
septum_plane_offset = 0 # Adjust based on visual proportion, looks slightly off-center
septum = (
    cq.Workplane("YZ")
    .moveTo(width_outer/2, 0)
    .threePointArc((0, height_outer), (-width_outer/2, 0))
    .lineTo(-width_outer/2, -5) # Go below
    .lineTo(width_outer/2, -5)
    .close()
    .extrude(wall_thickness)
    .translate((septum_plane_offset, 0, 0))
)

# Intersect septum with the inner profile logic to ensure it fits perfectly inside
# Actually, just intersecting it with the outer profile is enough, 
# then we union it with the shell.
septum_shape = outer_profile.translate((-length/2, 0, 0)).intersect(septum)
result = shell.union(septum_shape)


# Step 4: The Screw Boss
# Located in the "right" half (positive X relative to center in this setup)
boss = (
    cq.Workplane("XY")
    .workplane(offset=0) # Base level
    .center(boss_pos_x, 0)
    .circle(boss_outer_r)
    .extrude(boss_height)
)

# Cut the hole in the boss
boss_hole = (
    cq.Workplane("XY")
    .center(boss_pos_x, 0)
    .circle(boss_inner_r)
    .extrude(boss_height)
)
boss = boss.cut(boss_hole)

# Add fillets/chamfers to boss base for strength (visual approximation)
boss = boss.faces("<Z").edges().fillet(0.5)

# Trim the boss so it doesn't stick out the bottom of the curved shell if the shell curves up
# Since our shell is concave up (like a bowl), the boss stands on the bottom. 
# We need to make sure the boss starts "from the shell surface".
# The easiest way is to extend the boss downwards and cut it with the shell's underside.
# Re-creating boss with correct logic:
boss_solid = (
    cq.Workplane("XY")
    .center(boss_pos_x, 0)
    .circle(boss_outer_r)
    .extrude(height_outer) # Make it tall enough to reach the top
)

# Intersect with the inner volume of the shell to trim the bottom, 
# but wait, it grows FROM the shell.
# Let's boolean union a cylinder and then cut the hole.
result = result.union(boss)
result = result.cut(boss_hole)


# Step 5: The Latch Mechanism
# This looks like a block with a U-shape cut and a hole.
latch_x = catch_pos_x
latch_h = height_outer - 2.0 # Slightly lower than rim

latch_geo = (
    cq.Workplane("XY")
    .center(latch_x, 0)
    .rect(latch_block_l, width_outer/2 - wall_thickness) # extend to center
    .extrude(latch_h)
)

# The latch specific shape: A block with a rounded end and a hole
# Refined Latch Shape
latch_center = (catch_pos_x, 0)
latch_base = (
    cq.Workplane("XY")
    .center(latch_center[0], latch_center[1])
    # Create the blocky part
    .rect(6, 8) 
    .extrude(6)
)

# The U-shaped catch loop
catch_outer_r = 3.5
catch_inner_r = 2.0
catch_center_x = catch_pos_x + 2
catch_center_y = -3 # Offset from center line

catch_structure = (
    cq.Workplane("XY")
    .center(catch_center_x, catch_center_y)
    .circle(catch_outer_r)
    .extrude(6)
)

catch_hole = (
    cq.Workplane("XY")
    .center(catch_center_x, catch_center_y)
    .circle(catch_inner_r)
    .extrude(6)
)

# A small rectangular arm connecting the catch to the wall/center
arm_geo = (
    cq.Workplane("XY")
    .center(catch_center_x - 3, catch_center_y + 1.5)
    .rect(6, 3)
    .extrude(6)
)

# Combine latch parts
latch_complex = catch_structure.union(arm_geo).cut(catch_hole)

# Position it correctly inside the shell
# We need to clip it to the shell boundaries
result = result.union(latch_complex)

# Step 6: Side notches/cutouts
# There are small rectangular cutouts on the rim of the shell near the divider.
cutout_width = 3.0
cutout_depth = 2.0 # How far down from the rim
cutout_pos_x = septum_plane_offset # Aligned with septum

# Cutout on +Y side
cutout1 = (
    cq.Workplane("XY")
    .workplane(offset=height_outer - cutout_depth)
    .center(cutout_pos_x, width_outer/2)
    .rect(cutout_width * 2, 5) # Wide enough to cut through wall
    .extrude(cutout_depth * 2)
)

# Cutout on -Y side
cutout2 = (
    cq.Workplane("XY")
    .workplane(offset=height_outer - cutout_depth)
    .center(cutout_pos_x, -width_outer/2)
    .rect(cutout_width * 2, 5)
    .extrude(cutout_depth * 2)
)

result = result.cut(cutout1).cut(cutout2)

# Step 7: Final Cleanup - Trimming components that protrude outside the shell
# Use the intersection with the original outer profile extrusion to ensure 
# nothing sticks out of the convex hull of the object (bottom side)

# Re-create the solid outer volume for intersection
outer_solid_volume = (
    cq.Workplane("YZ")
    .moveTo(width_outer/2, 0)
    .threePointArc((0, height_outer), (-width_outer/2, 0))
    .close()
    .extrude(length)
    .translate((-length/2, 0, 0))
)

# To define the "inside" correctly for the boolean, we want to keep everything that is 
# essentially within the outer boundary.
result = result.intersect(outer_solid_volume)

# Add small hole on the side of the latch
side_hole = (
    cq.Workplane("XZ")
    .center(catch_center_x - 2, 3) # Approx height
    .circle(0.8)
    .extrude(20) # Through the side wall
    .translate((0, -10, 0)) # Position in Y
)

result = result.cut(side_hole)

# Rotate for better viewing angle matching the image
result = result.rotate((0,0,0), (0,0,1), 180) # Flip it so open side is up in default view? 
# The default view usually looks down Z. The current model is built on XY plane, opening up Z. 
# This matches.

# Refine boss height relative to shell floor
# The boss currently goes to Z=0. The shell floor is curved.
# The boss creates a flat bottom artifact if not careful.
# Since we did a union with a boss extruding from Z=0 and then intersected with outer shell,
# the bottom face fits the curve perfectly.

# Final Fillets
# Fillet the sharp edges of the septum contact
try:
    result = result.edges("|Y").filter(lambda e: abs(e.midpoint().x - septum_plane_offset) < 1.0).fillet(0.5)
except:
    pass # Skip if selection is tricky

# Export logic (optional, for verification)
# cq.exporters.export(result, "model.step")