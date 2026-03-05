import cadquery as cq

# Define parametric dimensions
cylinder_radius = 25.0
cylinder_thickness = 10.0
block_width = 15.0
block_height = 30.0
block_length = 20.0

# Calculate offsets to position the block relative to the cylinder
# The block appears to be attached tangentially or near the edge, 
# centered vertically relative to the cylinder's face axis?
# Looking at the image:
# The cylinder is flat like a wheel.
# The block is attached to the "bottom-left" quadrant.
# Let's align the cylinder center at (0,0,0).

# Create the main disc (cylinder)
# Creating it on the YZ plane makes the flat face point along X, 
# or XY plane makes it flat along Z. 
# Let's assume the flat face is on the YZ plane (axis along X) based on typical isometric views.
disc = cq.Workplane("YZ").circle(cylinder_radius).extrude(cylinder_thickness)

# Create the rectangular block
# It needs to be positioned.
# Let's place it such that it protrudes from the side.
# X-position: 0 to cylinder_thickness (flush with the cylinder thickness) or protruding? 
# In the image, the block seems to stick out from the face.
# Let's construct the block separately and union it.

# Position of the block:
# It's located at the bottom left relative to the center.
# Let's say center is at (-radius, -radius) roughly.
block_x_center = cylinder_thickness / 2  # Centered on the cylinder's thickness
block_y_center = -cylinder_radius * 0.5  # Shifted down
block_z_center = cylinder_radius * 0.8   # Shifted forward (since we used YZ plane)

# Actually, let's restart orientation to match the image better.
# Image shows the flat face of the disc facing somewhat right-up.
# The block is to the left-down of the disc.

# Let's try this standard orientation:
# Cylinder axis is along Y. 
# Disc lies in XZ plane.
disc = cq.Workplane("XZ").circle(cylinder_radius).extrude(cylinder_thickness)

# Now the block. It is attached to the -X, -Z side.
# Let's attach it to the side face of the cylinder or just intersect them.
# The block looks like it's intersecting the cylinder.

# Let's define the block center relative to the cylinder center (0,0,0 local to Workplane).
# Since we extruded along Y (normal to XZ), the cylinder goes from Y=0 to Y=10.
# The block looks like it stands vertically (Z axis) and protrudes in -X.

# Block dimensions
b_width = 20.0  # Dimension along X
b_thick = 15.0  # Dimension along Y (thickness matching or close to cylinder)
b_height = 35.0 # Dimension along Z

# Create the block geometry
# We need to position it so its right face touches or intersects the cylinder.
block = (cq.Workplane("XY")
         .box(b_width, b_thick, b_height, centered=(True, True, True))
         # Move it to the left (-X) and down (-Z)
         .translate((-cylinder_radius + b_width/4, cylinder_thickness/2, -cylinder_radius/2))
         )

# Refined approach for cleaner code:
# 1. Create Cylinder
# 2. Create Box
# 3. Union

# Cylinder parameters
c_rad = 30.0
c_thk = 10.0

# Box parameters
b_w = 20.0 # Width (x)
b_d = 20.0 # Depth (y - same direction as cylinder axis)
b_h = 40.0 # Height (z)

# Create the Cylinder
# Oriented with circular face on XY plane for simplicity, then rotated if needed.
# But looking at the isoview, let's model it directly in position.
# Let's assume the circular face is parallel to the YZ plane.
cylinder = cq.Workplane("YZ").circle(c_rad).extrude(c_thk)

# Create the Box
# It sits to the side. 
# X-position: It needs to be offset so it barely touches or slightly intersects the cylinder.
# Y-position: It looks centered with the cylinder's thickness.
# Z-position: It extends downwards.
box = (cq.Workplane("XY")
       .box(b_w, c_thk, b_h) # Width, Thickness (matched to cylinder), Height
       .translate((-c_rad + 2, c_thk/2, -b_h/3)) # Initial centered creation, then shift
       )

# Let's refine the translation to match the visual proportions
# The box connects to the "rim" of the cylinder at roughly the 7 o'clock position if viewing the face.
# However, usually these simple CAD primitives are aligned to axes.
# It looks like the box is attached to the *side* (-X direction) and extends *down* (-Z direction).

c_r = 25.0
c_w = 10.0

b_len = 20.0 # Dimension sticking out to the left
b_wid = 15.0 # Dimension matching the cylinder thickness
b_ht = 35.0  # Vertical dimension

result = (
    cq.Workplane("YZ")
    .circle(c_r)
    .extrude(c_w)
)

# Add the box
# We create a box on the XY plane (Front view essentially)
# We position it so its right face is inside the cylinder, and it extends down.
box_geo = (
    cq.Workplane("XY")
    .box(b_len, b_wid, b_ht, centered=(False, True, False)) 
    # centered=(False, True, False) -> X starts at 0 and goes +X, Y is centered, Z starts at 0 and goes +Z
    # We want X to go -X from the intersection point.
    # Let's just create centered and translate.
    .workplane()
    .box(b_len, b_wid, b_ht)
    .translate((-c_r - b_len/2 + 5, c_w/2, -b_ht/2 - 10))
)

# Final adjustment to match image specifically:
# Image: Cylinder is upright. Box is attached to the left side, slightly lower than center.
# The box thickness (depth) seems slightly wider than the cylinder or equal. Let's make it equal.

final_c_radius = 30.0
final_c_thick = 12.0
final_b_width = 20.0  # Size along X axis
final_b_height = 40.0 # Size along Z axis
final_b_thick = 20.0  # Size along Y axis (thicker than cylinder in image? Hard to tell, looks rectangular prism)

# Re-evaluating image: The rectangular prism looks distinct. 
# Let's construct:
# 1. Cylinder with axis along a normal vector (lets say X axis).
# 2. Box shifted in Y and Z.

result = cq.Workplane("YZ").circle(final_c_radius).extrude(final_c_thick)

# Calculate box position
# Box is to the "left" (negative Y if we view from +X) and "down" (negative Z).
# But wait, YZ plane means X is the extrusion axis.
# So Y is horizontal, Z is vertical on the screen.
# The box is to the left (-Y) and down (-Z).

box = (
    cq.Workplane("XY") # This gives us Z-up, but we need to align with the cylinder extruded along X.
    .box(final_b_thick, final_b_width, final_b_height) # x, y, z
    # Box X dimension corresponds to Cylinder thickness direction (X).
    # Box Y dimension corresponds to Cylinder radial direction (Horizontal).
    # Box Z dimension corresponds to Cylinder radial direction (Vertical).
    .translate((final_c_thick/2, -final_c_radius, -final_c_radius*0.5))
)

# Let's try a pure Union approach which is more robust
r_cyl = 25.0
t_cyl = 8.0
w_box = 15.0 # X-direction length
d_box = 15.0 # Y-direction thickness (matches cylinder)
h_box = 35.0 # Z-direction height

# Cylinder centered at origin, axis along Y
cyl = cq.Workplane("XZ").circle(r_cyl).extrude(t_cyl)

# Box attached to the side
# It sits at -X relative to cylinder center
# It sits at -Z relative to cylinder center
bx = (
    cq.Workplane("XY")
    .box(w_box, t_cyl, h_box)
    .translate((-r_cyl + 2, t_cyl/2, -r_cyl + 5))
)
# The image shows the box top face is below the cylinder top, 
# and box bottom face is below cylinder bottom.
# Box side is tangent-ish to cylinder side.

result = cyl.union(bx)