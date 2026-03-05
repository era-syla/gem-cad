import cadquery as cq

# Parametric dimensions
thickness = 5.0
hole_diameter = 4.0
fillet_radius = 4.0

# Define key coordinates for the profile
# We will create a sketch based on points and then extrude.
# The shape looks like an angled bracket with two "ears".
# Let's approximate the points to define the hull.

# Bottom-left ear center
p1 = (0, 0)
# Top-left ear center
p2 = (5, 35)
# Top-right corner area
p3 = (25, 25)
# Bottom-right corner area
p4 = (20, 5)

# Instead of complex arcs, it's often cleaner to define the main body via a hull of circles
# or a polygon with fillets. Looking at the image, it seems composed of two main lobes
# and a connecting body. Let's try a polyline approach that defines the outer contour.

# Define the points for a closed wire
pts = [
    (0, 0),       # Bottom-left point
    (15, 0),      # Bottom-right
    (28, 25),     # Top-right
    (13, 38),     # Top-left peak
    (0, 28),      # Top-left inner start
    (8, 18),      # Inner curve mid-point approximation (will handle with fillet)
    (0, 10)       # Bottom-left inner start
]

# Let's refine the strategy. It looks like a "V" shape or angled plate with rounded ends.
# A robust way is to union shapes or use the hull of circles.
# Let's try the hull of a few circles approach for the main body lobes, which guarantees smooth tangency.

# Circle 1: Bottom left lobe
c1_center = (0, 0)
c1_radius = 6.0

# Circle 2: Top left lobe
c2_center = (5, 30)
c2_radius = 6.0

# Circle 3: Top right area (part of the angled arm)
c3_center = (20, 20)
c3_radius = 6.0

# Circle 4: Bottom right area (part of the angled arm)
c4_center = (15, 5)
c4_radius = 6.0

# The shape is a bit more specific. It has a cutout.
# Let's define it as a sketch with segments.

sketch = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(20, 0)
    .lineTo(32, 28)
    .lineTo(12, 38)
    .lineTo(0, 28)
    # The inner cutout
    .lineTo(10, 18) 
    .close()
)

# This creates a sharp polygon. Now we extrude and fillet.
# However, the image shows a very specific "C" shape with an inner radius.
# A better approach for this specific geometry might be defining the outer loop and inner loop? No, it's a solid with a cutout.

# Let's try defining the shape by its distinct features:
# 1. A bottom arm
# 2. A top arm
# 3. An angled connecting beam

# Let's construct it from a base plate with specific vertices.
# Coordinates estimation based on visual proportions:
# Assume bottom-left hole is at (0,0) for reference.
# Bottom ear width approx 12-15mm.
# Vertical span approx 40mm.
# Horizontal span approx 30mm.

# Let's build the 2D profile.
result = (
    cq.Workplane("XY")
    .moveTo(-5, -5)       # Start bottom-left corner of the bounding box
    .lineTo(15, -5)       # Bottom edge
    .lineTo(30, 25)       # Right angled edge
    .lineTo(20, 40)       # Top edge
    .lineTo(0, 30)        # Top-left edge (ear)
    .lineTo(10, 18)       # Inner corner (the "crook" of the C)
    .lineTo(-5, 8)        # Left edge leading to bottom ear
    .close()
    .extrude(thickness)
)

# Now apply fillets to round off the sharp polygon corners
# We need to select edges carefully. All vertical edges should be filleted.
result = result.edges("|Z").fillet(fillet_radius)

# Now add the holes.
# There are 4 holes visible.
# 1. Bottom-left
# 2. Bottom-right (angled area)
# 3. Top-right (angled area)
# 4. Top-left

# Let's place the holes on the faces.
# Coordinates need to be inside the shape we just drew.
# Based on the polygon created:
# Bottom-left approx (0,0)
# Bottom-right approx (12, 2)
# Top-right approx (22, 28)
# Top-left approx (8, 32)

hole_centers = [
    (0, 0),     # Bottom ear
    (14, 2),    # Bottom of angled part
    (21, 22),   # Top of angled part
    (9, 31)     # Top ear
]

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_centers)
    .hole(hole_diameter)
)

# Refine the shape logic because the simple polygon + fillet might distort the inner curve too much or too little.
# A cleaner geometric construction:
# Define the plate as a hull of three main circles/regions minus an inner cutout?
# Actually, the polygon+fillet method is standard for this kind of "laser cut" bracketry.
# Let's adjusting points to make it look exactly like the image.

# Revised Points
p_bottom_left_outer = (-8, -6)
p_bottom_right_outer = (18, -6)
p_top_right_outer = (32, 28)
p_top_left_outer = (12, 42)
p_top_left_inner = (-2, 30)
p_inner_corner = (12, 16)
p_bottom_left_inner = (-8, 6)

result = (
    cq.Workplane("XY")
    .moveTo(p_bottom_left_outer[0], p_bottom_left_outer[1])
    .lineTo(p_bottom_right_outer[0], p_bottom_right_outer[1])
    .lineTo(p_top_right_outer[0], p_top_right_outer[1])
    .lineTo(p_top_left_outer[0], p_top_left_outer[1])
    .lineTo(p_top_left_inner[0], p_top_left_inner[1])
    # Create the arc for the inner cutout
    .threePointArc(p_inner_corner, p_bottom_left_inner)
    .close()
    .extrude(thickness)
)

# Apply fillets to outside corners
result = result.edges("|Z").fillet(3.0)

# Define hole positions relative to this new geometry
holes = [
    (0, 0),      # Bottom-left
    (16, 2),     # Middle-bottom
    (22, 24),    # Middle-top
    (8, 32)      # Top-left
]

# Cut the holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(holes)
    .hole(hole_diameter)
)

# Final code structure
import cadquery as cq

# Dimensions
thickness = 6.0
hole_dia = 5.0
fillet_r = 4.0

# Define the outer shape using a polyline approach
# The shape is effectively a polygon that gets rounded
pts = [
    (0, 0),       # Bottom-left reference
    (25, 5),      # Bottom-right
    (38, 40),     # Top-right
    (20, 50),     # Top-left peak
    (5, 38),      # Top-left ear end
    (18, 25),     # Inner curve approximation point (to be filleted or arced)
    (0, 15)       # Bottom-left ear start
]

# Let's try a pure sketch approach with tangents for a smoother result closer to the image
model = cq.Workplane("XY")

# Constructing the "L" or "C" shape
# We'll use a hull of two main rectangular-ish zones or just draw the outline
# Let's look at the image: 
# It looks like a standard link bracket.
# Let's use coordinates that create the slanted look.

p1 = (-5, 0)   # Bottom Left
p2 = (20, 5)   # Bottom Right
p3 = (35, 45)  # Top Right
p4 = (15, 50)  # Top Left
p5 = (5, 35)   # Inner Top
p6 = (15, 25)  # Inner Crook
p7 = (0, 15)   # Inner Bottom

result = (
    cq.Workplane("XY")
    .moveTo(p1[0], p1[1])
    .lineTo(p2[0], p2[1])
    .lineTo(p3[0], p3[1])
    .lineTo(p4[0], p4[1])
    .lineTo(p5[0], p5[1])
    # The inner cutout is concave
    .threePointArc(p6, p7)
    .close()
    .extrude(thickness)
)

# Round vertical edges
# We select all vertical edges. The fillet radius will naturally round the sharp corners.
# The inner arc transition might need a smaller radius or handled automatically if tangent.
result = result.edges("|Z").fillet(fillet_r)

# Add holes
# Visual estimation of hole centers based on the fillet-rounded body
hole_centers = [
    (2, 6),     # Bottom hole
    (17, 12),   # Lower middle hole
    (27, 38),   # Upper middle hole
    (13, 42)    # Top hole
]

# Re-adjusting coordinates to ensure holes are centered in the lobes
# Let's parameterize the shape relative to the hole centers to ensure good topology.
h1 = (0, 0)
h2 = (25, 10)
h3 = (10, 40)
h4 = (35, 30) # This one is weird.

# Let's go back to visual estimation, the polygon approach + fillet is usually the most robust for this "blob" shape.

final_pts = [
    (0, 0),    # Bottom left corner
    (30, 8),   # Bottom right corner
    (45, 50),  # Top right corner
    (20, 55),  # Top left corner
    (5, 40),   # Inner top
    (20, 28),  # Inner corner
    (5, 15)    # Inner bottom
]

result = (
    cq.Workplane("XY")
    .moveTo(final_pts[0][0], final_pts[0][1])
    .lineTo(final_pts[1][0], final_pts[1][1])
    .lineTo(final_pts[2][0], final_pts[2][1])
    .lineTo(final_pts[3][0], final_pts[3][1])
    .lineTo(final_pts[4][0], final_pts[4][1])
    .threePointArc(final_pts[5], final_pts[6])
    .close()
    .extrude(8)
    .edges("|Z").fillet(5)
)

# Hole locations adjusted to fit the final filleted shape
hole_locs = [
    (8, 8),     # Bottom left
    (26, 16),   # Bottom right
    (36, 43),   # Top right
    (18, 46)    # Top left
]

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_locs)
    .hole(5)
)