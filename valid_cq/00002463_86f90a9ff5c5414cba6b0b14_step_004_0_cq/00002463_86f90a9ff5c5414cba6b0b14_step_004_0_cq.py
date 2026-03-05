import cadquery as cq
import math

# --- Parameters ---
# Main triangle body
tri_base = 50.0  # Length of the base side (where the hinge is)
tri_height = 40.0 # Height of the triangle
thickness = 4.0   # Thickness of the plate
corner_radius = 2.0
inner_cutout_offset = 6.0 # How wide the frame of the triangle is

# Circular Hinge/Connector part
hinge_outer_radius = 12.0
hinge_inner_radius = 7.0
hinge_wall_thickness = 1.5
hinge_height_offset = 2.0  # How much higher the ring sits
hinge_slit_width = 1.5     # Width of the cutout slit

# The ring has a stepped profile
ring_rim_width = 1.5
ring_rim_height = 1.5

# Side hole for pin/screw
pin_hole_dia = 1.5

# --- Geometry Construction ---

# 1. Create the base triangular shape
# We define points for a right-angled-ish triangle, positioned relative to origin
pts = [
    (0, 0),
    (tri_base, 0),
    (0, tri_height)
]

# Create the solid triangle plate
# Using polyline and extrude, then fillet
tri_plate = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# 2. Create the inner cutout
# We can do this by offsetting a wire from the top face
tri_face = tri_plate.faces(">Z")
cutout_wire = tri_face.wires().toPending().offset2D(-inner_cutout_offset)
tri_plate = tri_plate.cut(
    tri_face.workplane()
    .add(cutout_wire)
    .extrude(-thickness, combine=False) # Extrude downwards to cut
)


# 3. Create the Circular Hinge/Connector Assembly
# The circular part is attached to one of the corners (let's assume (tri_base, 0))
# Based on the image, the ring center seems aligned with one leg of the triangle.
# Let's position the ring center slightly offset from the corner.

ring_center_x = tri_base
ring_center_y = 0

# Create the main cylindrical body of the connector
# It looks like a cup or a flanged bearing housing.
# Let's model the profile and revolve it or stack cylinders.

# Base cylinder (connection to triangle)
connector_base = (
    cq.Workplane("XY")
    .center(ring_center_x, ring_center_y)
    .circle(hinge_outer_radius)
    .extrude(thickness)
)

# Upper Ring (the flanged part)
upper_ring = (
    cq.Workplane("XY")
    .workplane(offset=thickness) # Start on top of the plate
    .center(ring_center_x, ring_center_y)
    .circle(hinge_outer_radius + 1.0) # Slightly wider rim
    .circle(hinge_inner_radius)
    .extrude(ring_rim_height)
)

# Lower internal cylinder (if visible, let's just make it a through hole first)
# Combining the base ring with the main body
body_with_ring = tri_plate.union(connector_base).union(upper_ring)

# Cut the through hole in the center of the ring
body_with_hole = body_with_ring.cut(
    cq.Workplane("XY")
    .center(ring_center_x, ring_center_y)
    .circle(hinge_inner_radius)
    .extrude(100, both=True)
)

# 4. Add the specific "stepped" look inside the ring
# The image shows an inner ledge.
inner_ledge = (
    cq.Workplane("XY")
    .workplane(offset=thickness - 1.0) # Slightly below top surface
    .center(ring_center_x, ring_center_y)
    .circle(hinge_inner_radius + 2.0)
    .extrude(ring_rim_height + 1.0)
)
# We subtract a smaller cylinder to leave a ledge? 
# Actually, easiest is to cut a larger hole partially, then a smaller hole through.
# Let's refine the hole cutting strategy.

# Reset to solid body before holes
base_solid = tri_plate.union(connector_base).union(upper_ring)

# Cut the main inner clear bore (smaller diameter)
final_body = base_solid.cut(
    cq.Workplane("XY")
    .center(ring_center_x, ring_center_y)
    .circle(hinge_inner_radius - 2.0) # The smallest hole at bottom
    .extrude(100, both=True)
)

# Cut the upper recess (larger diameter)
final_body = final_body.cut(
    cq.Workplane("XY")
    .workplane(offset=thickness - 1.5) # Start of the recess depth
    .center(ring_center_x, ring_center_y)
    .circle(hinge_inner_radius + 1.5) # Wider opening
    .extrude(10) # Cut upwards
)

# 5. Create the slit in the ring
# The slit is oriented towards the outside, perpendicular to the triangle leg.
# Based on image, it looks like it's at angle 0 relative to the corner.
slit_cutter = (
    cq.Workplane("XY")
    .center(ring_center_x + hinge_outer_radius, ring_center_y)
    .box(hinge_outer_radius * 2, hinge_slit_width, 20) # Box centered on edge
)

final_body = final_body.cut(slit_cutter)

# 6. Add the side pin hole on the triangle leg
# Looking at the image, there is a small hole on the vertical face of the long leg
# near the circular hinge.
pin_hole = (
    cq.Workplane("XZ") # Side plane
    .center(ring_center_x - 10, thickness / 2.0) # Position along the leg
    .circle(pin_hole_dia / 2.0)
    .extrude(10) # Cut through the leg width
)

# The leg width varies, we need to make sure we cut through the material.
# The triangle edge is at Y=0.
final_body = final_body.cut(
    cq.Workplane("XZ")
    .workplane(offset=-5) # Start from outside
    .center(tri_base - 12.0, thickness / 2.0) # Approx position based on image
    .circle(pin_hole_dia / 2.0)
    .extrude(20) # Cut through Y
)


# 7. Refine the connection between triangle and ring
# The image shows the ring is somewhat merged but distinct.
# The current union handles this, but let's fillet the junction if possible.
# Due to complex topology, robust filleting might fail, but let's try specific edges.
# We will skip complex filleting to ensure valid geometry generation without kernel errors.

# Final cleanup/orientation
result = final_body