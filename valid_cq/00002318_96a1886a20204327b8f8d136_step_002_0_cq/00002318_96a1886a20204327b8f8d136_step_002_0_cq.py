import cadquery as cq

# Parametric dimensions
outer_diameter = 50.0
thickness = 5.0  # Wall thickness of the ring
height = 5.0     # Height of the main ring structure
pin_diameter = 2.0
pin_height = 5.0 # Height of the pin above the surface
pin_offset = 15.0 # Distance of pin from center (approximate)

# Derived dimensions
inner_diameter = outer_diameter - (2 * thickness)
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0

# 1. Create the main ring
ring = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(height)
)

# 2. Create the triangular wedge (inward pointing)
# The wedge seems to start from the inner wall and point towards the center.
# Let's define it as a polygon.
# We need to calculate vertices that connect to the inner ring.
# It looks like a segment of a pie, or simply a triangle attached to the inner wall.
# Based on the image, the back of the triangle is flush with the inner radius curvature,
# but for a simple CAD model, a trapezoid or triangle booleaned with the ring might work best.
# However, looking closely, the "triangle" is actually part of the solid mass.
# It seems to connect two points on the inner circle and a point closer to the center.

# Let's create a wedge shape.
# We'll make a sketch that encompasses the area.
# The tip of the triangle is near the center, but not at the center.
# The base is on the ring.
wedge_tip_x = 5.0  # Offset from center
wedge_width_at_ring = 20.0 # How wide the base is

# A cleaner way: Draw the entire 2D profile and extrude.
# Profile: Outer circle, Inner circle, but with a "V" shape cutting into the void (adding material).

result = (
    cq.Workplane("XY")
    .circle(outer_radius) # Outer boundary
    .extrude(height)
)

# Create the inner cutout shape.
# It's a circle, minus a triangular wedge shape.
# We can create a solid cylinder for the "hole" and subtract a wedge from that cylinder before cutting.
# Or, just cut the ring and add the wedge.

# Let's try adding the wedge to the ring.
# The wedge points towards the center.
# Vertices for a triangle:
# Point 1: (tip_x, 0)
# Point 2: On inner circle, +Y
# Point 3: On inner circle, -Y

# Let's approximate the intersection points on the inner circle.
# Let's say the wedge opens up at an angle or has a fixed width.
# Judging by the image, it looks like an isosceles triangle with the tip somewhere along the X-axis.

tip_x = 8.0 # Tip position relative to center
base_x = inner_radius # Base is at the inner wall
# Let's define the width of the triangle at the inner wall.
half_width = 12.0 

# Define the triangular prism
wedge = (
    cq.Workplane("XY")
    .moveTo(tip_x, 0)
    .lineTo(outer_radius + 2, half_width) # Extend past outer radius to ensure clean union
    .lineTo(outer_radius + 2, -half_width)
    .close()
    .extrude(height)
)

# Intersect the wedge with a cylinder of the inner radius to get the curved back face?
# No, the image shows the wedge *merging* with the ring.
# So we simply union the wedge with the ring.
# But wait, the wedge shouldn't stick out the *outer* side of the ring.
# It should be contained within the inner diameter circle? No, it connects to the ring.
# So we need a shape that fits inside the Outer Circle.

# Let's refine the construction strategy:
# 1. Base Ring (Solid cylinder OD)
# 2. Subtract Inner Shape (Solid cylinder ID)
# 3. Add Wedge Shape.
# The wedge connects the inner wall to a point near the center.

wedge_shape = (
    cq.Workplane("XY")
    .moveTo(tip_x, 0)
    .lineTo(inner_radius, half_width) # Point on inner radius
    .lineTo(inner_radius, -half_width) # Point on inner radius
    .close()
    .extrude(height)
)
# Note: The straight lines above from (tip_x,0) to (inner_radius, half_width) 
# leave a gap between the flat line and the curved inner wall.
# To fill this perfectly, we should overshoot into the ring wall.

wedge_overshoot = (
    cq.Workplane("XY")
    .moveTo(tip_x, 0)
    .lineTo(outer_radius - 1.0, half_width + 5) # Go deep into the ring wall
    .lineTo(outer_radius - 1.0, -(half_width + 5))
    .close()
    .extrude(height)
)

# Now combine:
# 1. Ring
# 2. Wedge (intersected with Inner Cylinder so it doesn't poke out, or carefully constructed)

# Let's build the final result by boolean operations.
main_body = ring.union(wedge_overshoot)

# Now we need to clean up the outside. The wedge might have poked through the outer wall if I made it too big.
# But since I defined the ring with OD/ID, and unioned a wedge, 
# I just need to make sure the wedge stays *inside* the OD.
# Actually, the simplest way is:
# Create a solid cylinder (OD)
# Create a cutting tool: A cylinder (ID) MINUS the wedge shape.
# Cut the solid cylinder with the cutting tool.

cutting_tool_wedge = (
    cq.Workplane("XY")
    .moveTo(tip_x, 0)
    .lineTo(outer_radius + 10, 30) # Arbitrary large numbers to clear the circle
    .lineTo(outer_radius + 10, -30)
    .close()
    .extrude(height)
)

# The "hole" is the inner circle area, EXCEPT for the wedge area.
inner_void = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(height)
)

# The shape to REMOVE is the inner_void MINUS the wedge.
# This leaves the wedge part solid when we subtract the result from the main block.
cutout_shape = inner_void.cut(cutting_tool_wedge)

# Create the base disc
base_disc = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(height)
)

# Apply the cut
result = base_disc.cut(cutout_shape)

# 3. Add the pin
# The pin is located on the wedge surface.
# We need to find a suitable location on the wedge.
pin_x = (tip_x + inner_radius) / 2.0  # Roughly middle of the wedge
# Looking at image, pin is closer to tip
pin_x = tip_x + 4.0 

pin = (
    cq.Workplane("XY")
    .workplane(offset=height) # Start on top of the existing geometry
    .center(pin_x, 0)
    .circle(pin_diameter / 2.0)
    .extrude(pin_height)
)

result = result.union(pin)

# Export (optional, for verification during dev)
# cq.exporters.export(result, "result.step")