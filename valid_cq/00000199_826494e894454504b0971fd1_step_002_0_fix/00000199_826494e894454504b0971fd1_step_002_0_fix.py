import cadquery as cq
import math

# Create a curved plate/tag with text embossed on it
# The shape appears to be a curved rectangular plate (like a name tag)
# curved along the vertical axis

# Parameters
width = 40      # width of the plate
height = 70     # height of the plate
thickness = 4   # thickness of the plate
radius = 60     # radius of curvature

# Create the curved plate by revolving or using shell approach
# We'll create it as a swept shape along a curved path

# Create the base curved plate using loft or by creating a curved solid
# Approach: create a box and then use a cylindrical surface to curve it

# Simple approach: create a curved plate using sweep
# The plate is curved like a section of a cylinder

# Create the plate as a portion of a cylindrical shell
angle = math.degrees(width / radius)  # arc angle in degrees

# Create cylindrical shell section
outer_radius = radius + thickness/2
inner_radius = radius - thickness/2

# Create as a revolve of a rectangle
plate = (
    cq.Workplane("XZ")
    .rect(thickness, height)
    .revolve(angle, (radius, 0, 0), (radius, 0, 1))
)

# Try a different approach - create a solid curved plate
# Use a box and boolean with cylinders to create the curved shape

# Outer cylinder
outer_cyl = (
    cq.Workplane("XY")
    .cylinder(height, outer_radius)
)

# Inner cylinder  
inner_cyl = (
    cq.Workplane("XY")
    .cylinder(height, inner_radius)
)

# Cut inner from outer to get shell
shell = outer_cyl.cut(inner_cyl)

# Cut to get just a portion (the plate section)
# Use a box to cut away most of the cylinder
cut_box1 = (
    cq.Workplane("XY")
    .box(outer_radius * 3, outer_radius * 3, height * 2)
    .translate((-outer_radius * 1.5, 0, 0))
)

# Keep only a wedge section
half_angle_rad = math.radians(angle / 2)
# Box to cut the sides
cut_box2 = (
    cq.Workplane("XY")
    .box(outer_radius * 3, outer_radius * 3, height * 2)
    .translate((0, -outer_radius * 1.5, 0))
)

curved_plate = shell.cut(cut_box1)

# Cut the sides using rotated boxes
cut_side1 = (
    cq.Workplane("XY")
    .box(outer_radius * 3, outer_radius * 3, height * 2)
    .translate((0, outer_radius * 1.5, 0))
)

curved_plate = curved_plate.cut(cut_side1)

# Now we have the curved plate shape
# Add rounded corners at top and bottom
# The plate shape is now a curved strip

result = curved_plate

# Try simpler approach if the above doesn't work well
try:
    # Test that result has valid geometry
    bb = result.val().BoundingBox()
    if bb.xlen < 1:
        raise Exception("Invalid geometry")
except:
    # Fallback: simple curved plate
    pts_outer = []
    pts_inner = []
    n_pts = 20
    half_angle = math.radians(angle / 2)
    
    for i in range(n_pts + 1):
        a = -half_angle + i * (2 * half_angle) / n_pts
        x_o = outer_radius * math.sin(a)
        y_o = outer_radius * math.cos(a) - radius
        x_i = inner_radius * math.sin(a)
        y_i = inner_radius * math.cos(a) - radius
        pts_outer.append((x_o, y_o))
        pts_inner.append((x_i, y_i))
    
    all_pts = pts_outer + list(reversed(pts_inner))
    
    result = (
        cq.Workplane("XY")
        .polyline(all_pts)
        .close()
        .extrude(height)
    )