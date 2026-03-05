import cadquery as cq

# --- Parameter Definitions ---
# Overall dimensions
post_height = 30.0
post_diameter = 16.0
flange_height = 8.0
flange_diameter = 26.0
base_height = 25.0
base_width = 30.0  # Length along the slots axis
base_thickness = 10.0 # Thickness perpendicular to slots

# Threaded hole details (simulated with a simple hole for standard CAD without threading kernels)
hole_diameter = 8.0
hole_depth = 20.0

# Base slot details
slot_width = 6.0
slot_length = 10.0  # Center-to-center length approx
slot_z_offset = -12.0 # From the bottom of the flange
slot_spacing = 14.0 # Distance between slot centers

# Ribs/Tabs details (small protrusions on the flange and base interface)
rib_width = 2.0
rib_protrusion = 1.5

# --- Modeling ---

# 1. Create the cylindrical post
post = cq.Workplane("XY").circle(post_diameter / 2).extrude(post_height)

# 2. Create the flange (centered on the same axis, at the base of the post)
flange = cq.Workplane("XY").circle(flange_diameter / 2).extrude(flange_height)

# 3. Create the threaded hole (subtractive)
# Note: CadQuery core doesn't generate cosmetic threads easily, 
# so we create the pilot hole.
post_with_hole = post.faces(">Z").workplane().hole(hole_diameter, hole_depth)

# 4. Create the rectangular base
# We need to position it below the flange.
# Let's align the top of the base with the bottom of the flange.
# The base looks offset relative to the center cylinder axis in the image.
# Looking at the image, the cylinder seems centered on the thickness of the block,
# but the block extends primarily to one side or is centered. Let's assume centered for now
# but shifted in Z.
base = (
    cq.Workplane("XY")
    .workplane(offset=-base_height) # Start at bottom
    .box(base_width, base_thickness, base_height, centered=(True, True, False))
)

# 5. Create the slots in the base
# The slots go through the base_thickness (Y-axis in our current orientation)
# We sketch on the XZ plane (side of the block)
slot_sketch = (
    cq.Workplane("XZ")
    .workplane(offset=base_thickness/2 + 1) # Position sketch plane outside the block
    .center(0, -base_height/2) # Move origin to roughly center of block face vertically
)

# Left slot
slot1 = (
    slot_sketch
    .center(-slot_spacing/2, 0)
    .slot2D(slot_length, slot_width, angle=0)
)

# Right slot
slot2 = (
    slot_sketch
    .center(slot_spacing/2, 0)
    .slot2D(slot_length, slot_width, angle=0)
)

# Cut the slots
base_with_slots = base.cut(
    cq.Workplane("XZ")
    .workplane(centerOption="CenterOfMass", offset=0) # Reset to origin
    .center(-slot_spacing/2, -base_height/2)
    .slot2D(slot_length, slot_width)
    .extrude(base_thickness * 2, both=True) # Cut through everything
).cut(
    cq.Workplane("XZ")
    .workplane(centerOption="CenterOfMass", offset=0)
    .center(slot_spacing/2, -base_height/2)
    .slot2D(slot_length, slot_width)
    .extrude(base_thickness * 2, both=True)
)


# 6. Add the small locator ribs/tabs
# There appear to be small rectangular tabs at the junction of the flange and base.
# One on the side, one on the "back" (relative to the slots).
# Let's add a small rib feature on the side.

rib_shape = (
    cq.Workplane("XY")
    .workplane(offset=flange_height - 2.0) # Slightly below top of flange
    .rect(flange_diameter + rib_protrusion*2, rib_width)
    .extrude(- (flange_height + 2.0)) # Extrude down into the base
)

# There is also a distinct T-shaped feature or step on top of the block next to the flange
# visible in the image. Let's approximate that structural detail.
connector_block = (
    cq.Workplane("XY")
    .workplane(offset=0) # At flange bottom level
    .center(base_width/2 - 2, 0)
    .box(4, base_thickness + 2, flange_height/2, centered=(True, True, False))
)

# 7. Combine all parts
# Move the base to touch the bottom of the flange (z=0)
# Currently base was built from -25 up to 0.
# Flange is 0 to 8. Post is 0 to 30.
# We need to unite them.

# First, combine the main bodies
main_body = post_with_hole.union(flange).union(base_with_slots)

# Add the small details (ribs)
# The image shows ribs at 0, 90, 180 degrees roughly.
# Let's add the specific T-feature detail seen on the right side of the image.
t_feature = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .center(flange_diameter/2, 0)
    .box(5, 6, 4, centered=(False, True, False)) # Small block sticking out
)

# Refine the T-feature to match image (vertical rib + horizontal tab)
v_rib = (
    cq.Workplane("YZ")
    .workplane(offset=flange_diameter/2)
    .center(0, 2)
    .rect(2, 4)
    .extrude(4)
)


result = main_body.union(t_feature).union(rib_shape)

# Fillet the transition between post and flange for realism (optional but good)
result = result.faces(cq.selectors.NearestToPointSelector((0,0,flange_height))).fillet(1.0)

# Apply the result
show_object(result) if 'show_object' in locals() else None