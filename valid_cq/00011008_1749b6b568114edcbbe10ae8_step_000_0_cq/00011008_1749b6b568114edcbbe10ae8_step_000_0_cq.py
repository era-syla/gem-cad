import cadquery as cq

# --- Parameter Definitions ---
# Overall block dimensions
block_length = 80.0
block_width = 20.0
block_height = 15.0

# Hole parameters
hole_diameter = 14.0
hole_spacing = 20.0  # Center-to-center distance
num_holes = 4

# Bottom Hook/Clip parameters
hook_width = 15.0  # Width of the U-shape piece
hook_thickness = 5.0 # Thickness of the plate material
hook_drop = 15.0   # Distance from bottom of main block to bottom of hook
hook_opening_radius = 6.0 # Radius of the cutout
hook_vertical_offset = 20.0 # Vertical distance between top block and hook center roughly

# --- Derived Parameters ---
# Calculate starting position for the first hole to center the pattern
start_offset = (block_length - (num_holes - 1) * hole_spacing) / 2.0
# The hooks seem aligned with the holes
hook_centers = [(start_offset + i * hole_spacing - block_length/2, 0) for i in range(num_holes)]

# --- Modeling ---

# 1. Create the main top block
main_block = cq.Workplane("XY").box(block_length, block_width, block_height)

# 2. Add the holes to the main block
# We shift the workplane to the top face
main_block = main_block.faces(">Z").workplane()

# Create points for the holes centered along the X-axis
hole_points = [(start_offset + i * hole_spacing - block_length/2, 0) for i in range(num_holes)]

# Cut the holes
main_block = main_block.pushPoints(hole_points).hole(hole_diameter)

# 3. Create a single "Hook" element
# We will sketch the profile of the hook on the YZ plane (side view) or XZ plane (front view).
# Based on orientation, let's draw it on the YZ plane and extrude along X, or better yet,
# draw the U-shape profile on the XZ plane and extrude along Y (width).

# Let's define the U-shape profile on the XZ plane.
# It looks like a rectangle with a semi-circle cut out of the top.
u_shape_width = 16.0 # Width of the U-block itself (along Y)
u_shape_height = 12.0 # Height of the U-block
u_shape_thickness = 4.0 # Thickness of the U-block (along X)

# Refined approach for the hooks:
# They look like rectangular plates hanging down, with a semi-circular cutout on top.
# Let's model one hook unit.
hook_plate_width = 18.0  # Dimension along Y
hook_plate_height = 12.0 # Dimension along Z
hook_plate_thickness = 4.0 # Dimension along X
cutout_radius = 6.0
vertical_gap = 10.0 # Gap between top block and hook top

def create_hook():
    # Create the rectangular body
    h = cq.Workplane("XY").box(hook_plate_thickness, hook_plate_width, hook_plate_height)
    
    # Create the cutout
    # The cutout is on the top face (+Z), going through in X direction? 
    # No, looking at the image:
    # The main block is along X.
    # The hooks are plates perpendicular to X.
    # The cutout is a semi-circle on the top edge of these plates.
    
    h = (h.faces(">Z").workplane()
         .circle(cutout_radius)
         .cutBlind(-hook_plate_height)) # Cut all the way down or just enough
    
    return h

# Create a single hook object
hook = cq.Workplane("XY").box(hook_plate_thickness, hook_plate_width, hook_plate_height)
# Select the top face of the hook to cut the U-shape
hook = hook.faces(">Z").workplane().circle(cutout_radius).cutThruAll()

# 4. Assemble/Combine
# We need to position these hooks underneath the main block, aligned with the holes.
# The main block is centered at Z=0 for the box creation?
# box(l,w,h) creates a box centered at (0,0,0). So Z goes from -h/2 to h/2.
# We want the main block to be the top part.
main_block = main_block.translate((0, 0, 0)) # Keep as is.

# Determine Z position for hooks
# Main block bottom is at -block_height/2
# Let's leave a gap.
hook_z_center = -block_height/2 - vertical_gap - hook_plate_height/2

# Union all parts
result = main_block

for pt in hole_points:
    # Copy the hook geometry
    current_hook = hook.translate((pt[0], pt[1], hook_z_center))
    result = result.union(current_hook)

# Re-orienting to match the isometric view roughly
# (Not strictly necessary for the geometry but helps visualization)
# The default result is fine.

# 5. Adding the vertical connectors (Stems)
# The image shows thin stems connecting the main block to the hooks.
stem_diameter = 6.0 # Slightly smaller than the hole or hook thickness
stem_length = vertical_gap + block_height/2 + hook_plate_height/2 # Distance to bridge center to center roughly
# Actually, let's just create cylinders from the bottom of the block to the top of the hooks.

# Bottom of block: Z = -block_height/2
# Top of hook: Z = -block_height/2 - vertical_gap
stem_top_z = -block_height/2
stem_bottom_z = stem_top_z - vertical_gap

# Actually, looking closely at the image, there are no stems. 
# The objects are floating separately or implied to be connected by an invisible mechanism/assembly.
# However, standard "part" requests usually imply a single solid unless it's an assembly view.
# Looking VERY closely at the provided image:
# The top block and the bottom hooks are distinct. The hooks are aligned perfectly under the holes.
# There is NO visible connecting rod in the shadow or geometry.
# It looks like an "exploded view" or a component set.
# BUT, typically for a "generate CAD model" prompt, making a multi-body object is acceptable.

# WAIT, looking closer at the crop 4 (bottom right):
# There is clearly empty space between the top block and the U-shaped clips.
# I will generate the code to produce the disjoint bodies in a single result object.

# Final check on dimensions to match proportions:
# Block looks about 4x1x1 roughly. (80, 20, 15 fits okay)
# Holes look large, almost touching edges. (14mm dia in 20mm width is tight, looks right).
# Clips look like they match the block width approximately.

# If the user wants a single printable part, there usually would be connectors, 
# but I must faithfully reproduce the image. The image shows floating parts.

pass