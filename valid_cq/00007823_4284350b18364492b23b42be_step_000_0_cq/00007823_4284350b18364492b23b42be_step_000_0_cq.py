import cadquery as cq

# Parametric dimensions
# Base Cone (leftmost part)
base_radius_outer = 15.0
base_radius_inner = 8.0
base_height = 10.0

# Middle Section (large cone + spherical cap/fillet)
mid_cone_radius_start = 8.0
mid_cone_radius_end = 16.0
mid_cone_height = 20.0
mid_cap_radius = 16.0 # Radius of the sphere creating the rounded top of the middle section
mid_cap_height_offset = 5.0 # How much the spherical part protrudes

# Neck
neck_radius = 5.0
neck_length = 5.0

# Head Section (mushroom shape)
head_radius = 10.0
head_thickness = 8.0 # Approximate height of the curved part

# Tip (pyramid/prism)
tip_side_length = 8.0
tip_height = 8.0

# Construction
# 1. Base Flared Cone
# Creating a truncated cone. We can use `cq.Solid.makeCone` or revolve a sketch.
# Let's stack operations on the Z axis.

# Start with the leftmost part: The flared base
# It looks like a cone expanding outwards to the left.
base_cone = cq.Workplane("XY").circle(base_radius_outer).workplane(offset=base_height).circle(base_radius_inner).loft(combine=True)

# 2. Middle Cone
# It connects to the small end of the base cone and expands
middle_cone = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .circle(mid_cone_radius_start)
    .workplane(offset=mid_cone_height)
    .circle(mid_cone_radius_end)
    .loft(combine=True)
)

# 3. Rounded top of the middle section
# It looks like a sphere or ellipsoid cut. Let's create a sphere and intersect/union it.
# Center of sphere needs to be calculated to match tangency or just placed visually.
# Placing a sphere at the end of the middle cone.
sphere_center_z = base_height + mid_cone_height
middle_cap = (
    cq.Workplane("XY")
    .workplane(offset=sphere_center_z - (mid_cone_radius_end * 0.5)) # Shift down so it merges well
    .sphere(mid_cone_radius_end)
)
# We only want the top part, but since we are unioning, a full sphere submerged works fine if cleaned up.
# However, the image shows a distinct "shoulder". 
# Let's refine: The middle section looks like a cone that transitions into a spherical surface.
# Simpler approach: Create the cone, then add a sphere at the end, then cut the neck.

# Let's rebuild the logic as a single revolved profile or a stack of primitives.
# Stacking primitives is usually more robust in code without a drawing.

# Re-evaluating the stack based on Z-heights:
current_z = 0

# Part A: The "Dish" or Flared Base
# It's a cone with R_base at Z=0 and R_waist at Z=h1
waist_radius = 8.0
dish_outer_radius = 18.0
dish_height = 12.0

part_a = cq.Workplane("XY").circle(dish_outer_radius).workplane(offset=dish_height).circle(waist_radius).loft()
current_z += dish_height

# Part B: The Main Body Cone
# Starts at R_waist, expands to R_shoulder
shoulder_radius = 15.0
body_height = 20.0

part_b = cq.Workplane("XY").workplane(offset=current_z).circle(waist_radius).workplane(offset=body_height).circle(shoulder_radius).loft()
current_z += body_height

# Part C: The Rounded Shoulder
# This looks like a sphere segment.
shoulder_sphere_radius = shoulder_radius
# We place a sphere such that its equator is roughly at current_z
part_c = cq.Workplane("XY").workplane(offset=current_z).sphere(shoulder_sphere_radius)

# Note: The sphere will bulge downwards too. We need to union this carefully or cut it.
# Let's create the stack and then union.

# Part D: The Neck
# A cylinder connecting the shoulder to the head.
neck_r = 5.0
neck_h = 8.0
# The neck starts slightly inside the shoulder sphere
neck_start_z = current_z + (shoulder_sphere_radius * 0.3) 
part_d = cq.Workplane("XY").workplane(offset=neck_start_z).cylinder(neck_h, neck_r)
current_z = neck_start_z + neck_h

# Part E: The Head (Mushroom cap shape)
# Looks like a partial sphere or ellipsoid.
head_r = 11.0
part_e = cq.Workplane("XY").workplane(offset=current_z).sphere(head_r)

# Part F: The Tip (Triangular Prism/Pyramid)
# It sits on top of the head.
tip_h = 10.0
tip_base_w = 8.0 # width of triangle
# Construct a triangular pyramid
part_f = (
    cq.Workplane("XY")
    .workplane(offset=current_z + head_r - 2.0) # Embed slightly in the head
    .polygon(3, tip_base_w)
    .workplane(offset=tip_h)
    .polygon(3, 0.1) # Go to a point (almost)
    .loft()
)

# Combine everything
# We build a composite object.
# To make it clean, we should union them step by step or all at once.

# Re-doing with a single Revolve operation for the main body to ensure smooth continuity
# and correct "lathe" look, except for the triangular tip.

# Profile Points (r, z)
# 1. Start at top left of the dish (18, 0)
# 2. Go to waist (8, 12)
# 3. Go to shoulder (15, 32)
# 4. Round over shoulder (arc)
# 5. Neck (5, z_neck)
# 6. Head (sphere arc)

def create_model():
    # 1. Create the main rotational body using a sketch/spline/polyline
    # It's easier to compose primitives for the specific 'sharp' transitions seen in the image
    
    # Base Cone (inverted)
    p1 = cq.Workplane("XY").circle(18).workplane(offset=12).circle(8).loft()
    
    # Main widening cone
    p2 = cq.Workplane("XY").workplane(offset=12).circle(8).workplane(offset=20).circle(16).loft()
    
    # Shoulder (Spherical Cap)
    # We place a sphere at the top of p2
    p3 = cq.Workplane("XY").workplane(offset=32).sphere(16)
    # Cut the bottom of the sphere to make it a cap sitting on the cone? 
    # Actually, a simple intersection or just letting it merge is fine, 
    # but we need to trim the bottom of the sphere that protrudes into the cone if we want clean geometry.
    # However, for a visual model, simple union works.
    
    # We need a neck coming out of the sphere.
    # Sphere center is at Z=32. Radius 16. Top of sphere is Z=48.
    # We want the neck to emerge around Z=42 maybe?
    p4 = cq.Workplane("XY").workplane(offset=44).circle(5).extrude(6)
    
    # The Head (Another spherical shape)
    # Center at end of neck
    p5 = cq.Workplane("XY").workplane(offset=50).sphere(10)
    
    # Join rotational parts
    body = p1.union(p2).union(p3).union(p4).union(p5)
    
    # The Triangular Spike
    # Located at the 'top' (far right in the image).
    # The head sphere is at Z=50, radius 10. Apex is at Z=60.
    # The spike should protrude from the sphere surface.
    
    # Create a triangular pyramid
    # Orientation: The image shows the triangle pointing along the axis.
    spike = (
        cq.Workplane("XY")
        .workplane(offset=58) # Start just inside the sphere surface
        .polygon(3, 10)       # Equilateral triangle base
        .workplane(offset=10) # Height of spike
        .polygon(3, 0.1)      # Point
        .loft()
    )
    
    # The image shows the spike is rotated relative to the default polygon orientation
    # Default polygon point is usually at 0 degrees (X axis).
    # We might need to rotate it to match exactly, but generic is fine.
    
    final_obj = body.union(spike)
    
    # Rotate to match image orientation roughly (Side view)
    final_obj = final_obj.rotate((0,0,0), (0,1,0), -90)
    
    return final_obj

result = create_model()