import cadquery as cq

# Define parametric dimensions
base_diameter = 50.0
height = 50.0
top_dome_radius = 6.0
base_flare_radius = 5.0
main_body_curvature_factor = 0.5  # Adjusts the bulge of the main body

# Calculate derived dimensions
base_radius = base_diameter / 2.0
top_neck_radius = top_dome_radius * 0.9  # Where the body meets the dome

# Create the profile for revolution
# We will construct a profile in the XZ plane and revolve it around Z

# Points for the profile
p0 = (base_radius + base_flare_radius, 0) # Outer rim of the base flare
p1 = (base_radius, 0) # Bottom of the main body start
p_top_body = (top_neck_radius, height - top_dome_radius) # Top of main body
p_top_dome = (0, height) # Very top tip

# Construct the profile wire
# 1. Start at the outer rim
# 2. Create the base flare (a small arc or spline up to the main body start)
#    Actually, looking at the image, it looks like a continuous curve.
#    Let's model it as a spline that goes from the base rim, curves up, and meets the top.

# Let's try a more segmented approach to match the visual features:
# A. A small spherical cap at the top.
# B. A main body that looks like an ogive or a large arc.
# C. A flared base.

# Method: Create a sketch and revolve it.

# Top Dome: Semicircle or partial circle
# Center of top dome sphere approx at (0, height - top_dome_radius)
dome_center = (0, height - top_dome_radius)

# Main Body Profile
# It connects (base_radius, slightly_above_0) to (top_neck_radius, height - top_dome_radius)
# The image shows a smooth transition from a flared base.

# Let's define the points for a spline to capture the organic shape
# P_base_outer: The outermost point at Z=0
p_base_outer = (base_radius + 5, 0)

# P_inflection: A point slightly up and in, where the flare turns into the main body
p_inflection = (base_radius, 5)

# P_neck: Where the body meets the top dome
p_neck = (top_neck_radius, height - top_dome_radius * 0.8) 

# P_top: The top tip
p_top = (0, height)

# We will create a single edge or a set of tangent edges.
# The image has a distinct "seam" or transition line where the top dome sits on the body, 
# and another near the base. Let's look closer.
# Actually, it looks like three distinct sections:
# 1. A top spherical cap.
# 2. A main conical/ogive section.
# 3. A flared base rim.

result = (
    cq.Workplane("XZ")
    # 1. The top dome
    .moveTo(0, height)
    .lineTo(0, height - top_dome_radius) # Center line down
    .lineTo(top_dome_radius, height - top_dome_radius) # Horizontal out
    .threePointArc((top_dome_radius * 0.707, height - top_dome_radius + top_dome_radius * 0.707), (0, height)) # Arc back to top
    .close()
    .revolve()
)

# 2. The main body
# Let's use a loft or a revolve of a specific curve.
# It looks like a convex curve.
main_body_height = height - top_dome_radius
body_bottom_z = 3.0 # Start a bit above 0 to leave room for the flare

body_profile = (
    cq.Workplane("XZ")
    .moveTo(0, body_bottom_z)
    .lineTo(base_radius, body_bottom_z)
    .threePointArc((base_radius * 0.7, body_bottom_z + main_body_height * 0.4), (top_dome_radius * 0.95, height - top_dome_radius))
    .lineTo(0, height - top_dome_radius)
    .close()
    .revolve()
)

# 3. The flared base
# Connects the bottom of the main body to a wider rim on the floor
flare_profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(base_radius + 4.0, 0) # Wider base
    # Concave arc for the flare
    .threePointArc((base_radius + 1.0, body_bottom_z * 0.3), (base_radius, body_bottom_z))
    .lineTo(0, body_bottom_z)
    .close()
    .revolve()
)

# Combine the parts
result = result.union(body_profile).union(flare_profile)

# Smooth the transitions if needed, though the image shows somewhat sharp transitions 
# between the flare and body, and body and dome.
# Let's fillet the neck slightly to blend it like in the image (it looks like a small step or seam, so maybe no fillet or very small)
# The image actually shows a bit of an overhang/bead for the top dome. 
# Let's adjust the code to make a single cleaner profile revolution which is more robust.

# Refined approach: Single Revolution of a Spline/Polyline
p_tip = (0, 50)
p_dome_base = (6, 46)
p_body_top = (6, 46) # Continuity point
p_body_mid = (20, 20) # Control point for bulge
p_body_bot = (25, 5) # Bottom of main curve
p_flare_edge = (28, 0) # Flare out

# Let's build it piece-wise to ensure the sharp creases visible in the rendering
# The rendering shows a distinct line between the top cap and the body, and the body and the base.

# Top Cap (Sphere-like)
p_cap_center = (0, 45)
cap_radius = 6.5
# Determine intersection with vertical axis for exact height
# x^2 + (z-45)^2 = 6.5^2 -> at x=0, z = 45+6.5 = 51.5. Let's adjust to match height=50 approx
cap = cq.Workplane("XY").transformed(offset=(0,0,44)).sphere(6)

# Main Body (Convex Hull)
# We want a shape that is roughly R=6 at top, R=25 at bottom, height ~40
# We can revolve a spline.
body_sk = (
    cq.Workplane("XZ")
    .moveTo(0, 4)
    .lineTo(24, 4)
    .spline([(6, 45)], tangents=[(0, 5), (0, 1)], includeCurrent=True)
    .lineTo(0, 45)
    .close()
    .revolve()
)

# Base Flare (Concave)
base_sk = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(28, 0)
    .spline([(24, 4)], tangents=[(1, 0), (0, 1)], includeCurrent=True)
    .lineTo(0, 4)
    .close()
    .revolve()
)

# Union everything
result = base_sk.union(body_sk).union(cap)

# Apply a fillet to the base transition to make it smooth like a continuous surface with a ridge?
# Looking at the image, the line at the bottom looks like a sharp transition from convex body to concave flare.
# The line at the top looks like the sphere is slightly larger than the neck of the body, creating a small lip.

# Refined code generation based on visual inspection:
# 1. Base Flare: Concave arc revolute.
# 2. Main Body: Convex arc revolute.
# 3. Top Cap: Sphere or revolved arc, slightly overhanging the body neck.

result = (
    cq.Workplane("XY")
    # Base Flare
    .parametricCurve(lambda t: (
        (28 - 4*t + t**2 * 1) if t < 1 else 0, # Rough radial function approximation logic won't work well directly in basic CQ without creating edge
        0, 
        0
    ))
)

# Let's stick to standard sketch operations.

# Create the profile for the main body
main_body = (
    cq.Workplane("XZ")
    .moveTo(0, 4)
    .lineTo(22, 4)  # Base of main body
    .threePointArc((15, 25), (5.5, 43)) # Convex curve up to neck
    .lineTo(0, 43)
    .close()
    .revolve()
)

# Create the flared base
flare = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(26, 0) # Outer rim
    .threePointArc((23.5, 1.5), (22, 4)) # Concave flare up to meet body
    .lineTo(0, 4)
    .close()
    .revolve()
)

# Create the top cap
# It looks like a slightly squashed sphere or just a sphere
cap = (
    cq.Workplane("XY")
    .workplane(offset=43)
    .sphere(5.5)
)
# Move cap up slightly so center is right
# If radius is 5.5, and we want tip at ~48-50
# Center at 43 + z_offset. 
cap = cq.Workplane("XZ").moveTo(0, 43).lineTo(0, 48.5).lineTo(0.1, 48.5).threePointArc((5.5, 43), (0.1, 37.5)).close().revolve()
# Easier to just use a sphere and cut/union
cap = cq.Workplane("XY").transformed(offset=(0,0,43)).sphere(5.8)

# Union them
result = flare.union(main_body).union(cap)

# Clean up
result = result.clean()