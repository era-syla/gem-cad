import cadquery as cq

# --- Parametric Dimensions ---
frame_width = 120.0
frame_height = 80.0
thickness = 8.0  # Thickness of the frame arms/struts
depth = 25.0     # Depth of the extrusions (arms)

# Dimensions for the central mounting block
mount_block_width = 40.0
mount_block_height = 20.0
mount_block_depth = 25.0
mount_hole_diam = 4.0
mount_hole_spacing = 20.0

# Dimensions for the side arms extending forward
side_arm_depth = 30.0  # How far they stick out
side_arm_hole_diam = 5.0

# --- Geometry Construction ---

# 1. Base Sketch for the main frame (Front View profile)
# This includes the outer rectangle, the top bar, and the two vertical legs
# We will create the general shape and then cut out the insides.
# Looking at the image, it's essentially a rectangular frame with an internal structure.

# Let's define the overall bounding box and cut away material.
# Or, build it up from lines/rectangles. Let's use a "constructive" approach with a sketch.

# Create the main frame sketch on the XY plane
main_frame = (
    cq.Workplane("XY")
    .sketch()
    # Outer boundary
    .rect(frame_width, frame_height)
    # Inner cutout for the main window (top section is a bar, sides are bars)
    .rarray(frame_width - 2*thickness, frame_height - 2*thickness, 1, 1)
    .rect(frame_width - 2*thickness, frame_height - 2*thickness, mode='s')
    .finalize()
    .extrude(thickness) # This creates just a generic rectangular frame first
)

# Actually, looking closer at the image, the structure is more complex.
# It has a "back plate" or "back frame" and parts sticking out in Z.
# Let's redesign the strategy:
# Part A: The Top Bar and Side Verticals (The "Goal Post" shape)
# Part B: The Bottom Horizontal extensions (Feet)
# Part C: The Internal hanging structure with the block.

# Strategy 2: Draw the profile on the Front Plane (XZ or XY) and extrude.
# The profile is a "U" shape upside down, plus the internal structure.
# But the depth varies. The top bar and sides seem to have uniform depth.
# The feet stick out. The central block sticks out.

# Let's model the "Skeleton" first (The flat shape against the wall).
# Then add the protrusions.

# --- Corrected Strategy ---
# 1. Create the Top Bar
top_bar = cq.Workplane("XY").box(frame_width, thickness, thickness).translate((0, frame_height/2 - thickness/2, 0))

# 2. Create the Side Verticals
left_leg = cq.Workplane("XY").box(thickness, frame_height, thickness).translate((-frame_width/2 + thickness/2, 0, 0))
right_leg = cq.Workplane("XY").box(thickness, frame_height, thickness).translate((frame_width/2 - thickness/2, 0, 0))

# 3. Create the Bottom "Feet" extensions
# These extend in the +Z direction (relative to the front face we are building) or +Y depending on orientation.
# Let's assume the frame is lying on the XY plane for now, and "depth" is Z.
# The feet extend from the bottom of the legs.
foot_length = 30.0
left_foot = (
    cq.Workplane("XY")
    .box(thickness, thickness, foot_length)
    .translate((-frame_width/2 + thickness/2, -frame_height/2 + thickness/2, foot_length/2 - thickness/2))
)
right_foot = (
    cq.Workplane("XY")
    .box(thickness, thickness, foot_length)
    .translate((frame_width/2 - thickness/2, -frame_height/2 + thickness/2, foot_length/2 - thickness/2))
)

# 4. The Internal Structure
# It hangs from the top bar. There are two small vertical struts connecting to a horizontal-ish structure.
# But looking closely, it looks like a single continuous "M" or "W" shape or a bracket.
# Let's trace the internal path:
# It comes down from the top bar (2 points), goes down, then connects to the central block.
# Then from the central block sides, it goes down and forward to form the inner lower arms.

# Let's simplify.
# Frame:
frame = top_bar.union(left_leg).union(right_leg).union(left_foot).union(right_foot)

# Central Hanging Assembly
# Vertical drops from top bar
drop_offset = 20.0 # Distance from center line
drop_height = 25.0
left_drop = cq.Workplane("XY").box(thickness, drop_height, thickness).translate((-drop_offset, frame_height/2 - thickness - drop_height/2, 0))
right_drop = cq.Workplane("XY").box(thickness, drop_height, thickness).translate((drop_offset, frame_height/2 - thickness - drop_height/2, 0))

# Horizontal bar connecting drops
cross_bar_y = frame_height/2 - thickness - drop_height + thickness/2
cross_bar = cq.Workplane("XY").box(drop_offset*2 + thickness, thickness, thickness).translate((0, cross_bar_y, 0))

# The Central Block
# Attached to the front of the cross_bar
block = (
    cq.Workplane("XY")
    .box(mount_block_width, mount_block_height, mount_block_depth)
    .translate((0, cross_bar_y, mount_block_depth/2 - thickness/2))
)

# Holes in Central Block
block = (
    block.faces(">Y")
    .workplane()
    .pushPoints([(-mount_hole_spacing/2, 0), (mount_hole_spacing/2, 0)])
    .hole(mount_hole_diam)
)

# The Inner Lower Arms
# These come down from the sides of the central structure and extend forward.
# Originating from the cross_bar ends.
inner_arm_drop_height = 35.0
inner_arm_x = drop_offset
inner_arm_y_start = cross_bar_y
inner_arm_y_end = cross_bar_y - inner_arm_drop_height

left_inner_vertical = (
    cq.Workplane("XY")
    .box(thickness, inner_arm_drop_height, thickness)
    .translate((-inner_arm_x, inner_arm_y_start - inner_arm_drop_height/2 + thickness/2, 0))
)

right_inner_vertical = (
    cq.Workplane("XY")
    .box(thickness, inner_arm_drop_height, thickness)
    .translate((inner_arm_x, inner_arm_y_start - inner_arm_drop_height/2 + thickness/2, 0))
)

# Inner Feet Extensions
inner_foot_length = 30.0
left_inner_foot = (
    cq.Workplane("XY")
    .box(thickness, thickness, inner_foot_length)
    .translate((-inner_arm_x, inner_arm_y_end + thickness/2, inner_foot_length/2 - thickness/2))
)

right_inner_foot = (
    cq.Workplane("XY")
    .box(thickness, thickness, inner_foot_length)
    .translate((inner_arm_x, inner_arm_y_end + thickness/2, inner_foot_length/2 - thickness/2))
)

# Holes in the 4 feet (Outer Left/Right, Inner Left/Right)
# The holes are on the front faces (Z faces)
feet_hole_diam = 4.0

# Combine everything first to make hole operations easier or do them individually.
# Let's combine geometry.
structure = (
    frame
    .union(left_drop)
    .union(right_drop)
    .union(cross_bar)
    .union(block)
    .union(left_inner_vertical)
    .union(right_inner_vertical)
    .union(left_inner_foot)
    .union(right_inner_foot)
)

# Add chamfers/fillets to refine the look as per image
# The ends of the feet look flat, but let's ensure holes are placed correctly.
# The holes go into the ends of the extending arms (along the Y axis in local coords, Z in global construction).

# Select faces at the tips of the feet extensions (highest Z)
result = (
    structure
    .faces(">Z")
    .workplane()
    .hole(feet_hole_diam, depth=15.0) # Blind holes
)

# Adding fillets to internal corners for strength/aesthetics (optional but makes it look like the image)
# The image shows some rounded corners, particularly on the main frame.
# Let's fillet the outer vertical edges of the main frame.
try:
    result = result.edges("|Z").filter_by(lambda e: e.center().z < 5 and abs(e.center().y) < frame_height/2).fillet(1.0)
except:
    pass # Skip if selection is tricky

# Ensure the orientation matches the isometric view
result = result.rotate((0,0,0), (1,0,0), -90) # Rotate to stand up

# Final Export
if __name__ == "__main__":
    try:
        from cadquery import exporters
        # exporters.export(result, "bracket.step")
        pass
    except ImportError:
        pass