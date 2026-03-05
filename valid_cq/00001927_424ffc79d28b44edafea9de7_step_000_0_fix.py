import cadquery as cq
import math

# Rocket body - tapered cylinder (cone-like body)
# Main body: starts wide at bottom, tapers to narrow at top

# Body parameters
body_bottom_r = 3.0
body_top_r = 0.8
body_height = 18.0

# Create the main rocket body as a loft between two circles
body = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .circle(body_bottom_r)
    .workplane(offset=body_height)
    .circle(body_top_r)
    .loft()
)

# Nose cone - hemisphere/bullet shape on top
nose_r = body_top_r
nose_height = 2.5
nose = (
    cq.Workplane("XY")
    .workplane(offset=body_height)
    .circle(nose_r)
    .workplane(offset=nose_height * 0.7)
    .circle(nose_r * 0.6)
    .workplane(offset=nose_height)
    .circle(0.05)
    .loft()
)

# Combine body and nose
rocket_body = body.union(nose)

# Fins - 4 fins at the base
# Each fin is a swept triangle shape
fin_thickness = 0.5
fin_height = 6.0
fin_width = 4.0
fin_base_offset = body_bottom_r - 0.2

def make_fin(angle_deg):
    # Create a fin as an extruded polygon
    # Fin profile: triangle pointing outward
    pts = [
        (0, 0),
        (fin_width, 0),
        (0, fin_height),
    ]
    fin = (
        cq.Workplane("XZ")
        .workplane(offset=0)
        .polyline(pts)
        .close()
        .extrude(fin_thickness)
        .translate((-fin_thickness/2, fin_base_offset, 0))
    )
    # Rotate around Z axis
    fin = fin.rotate((0, 0, 0), (0, 0, 1), angle_deg)
    return fin

# Create 4 fins at 90 degree intervals
angles = [0, 90, 180, 270]
fins = []
for angle in angles:
    fin = make_fin(angle)
    fins.append(fin)

# Union all fins
result = rocket_body
for fin in fins:
    result = result.union(fin)

# Add a small base ring / skirt at the bottom
skirt_height = 1.2
skirt_outer_r = body_bottom_r + 0.5
skirt_inner_r = body_bottom_r - 0.3
skirt = (
    cq.Workplane("XY")
    .circle(skirt_outer_r)
    .circle(skirt_inner_r)
    .extrude(skirt_height)
    .translate((0, 0, -skirt_height + 0.5))
)

result = result.union(skirt)

# Fillet the top edges slightly
try:
    result = result.edges("|Z").fillet(0.15)
except:
    pass