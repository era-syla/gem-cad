import cadquery as cq

# --- Parameters ---
# Base dimensions
base_diameter = 14.0
base_thickness = 2.0
base_fillet_radius = 0.8

# Female (Socket) dimensions
socket_od = 4.5
socket_id = 2.5
socket_height = 3.5

# Male (Stud) dimensions
stud_od = 2.4
stud_height = 4.5

# Spacing between parts
spacing = 20.0

# --- Helper Function for Base ---
def create_base():
    """Creates the rounded button-like base."""
    return (
        cq.Workplane("XY")
        .circle(base_diameter / 2.0)
        .extrude(base_thickness)
        .edges()
        .fillet(base_fillet_radius)
    )

# --- Create Female Part (Left) ---
# 1. Base Geometry
female_base = create_base()

# 2. Hollow Cylinder Feature
female_post = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .circle(socket_od / 2.0)
    .extrude(socket_height)
)

# 3. Combine and Refine
female_part = female_base.union(female_post)

# Add fillet at the intersection of base and post
female_part = female_part.edges(
    cq.selectors.NearestToPointSelector((0, 0, base_thickness))
).fillet(0.4)

# Cut the inner hole
female_part = (
    female_part.faces(">Z")
    .workplane()
    .circle(socket_id / 2.0)
    .cutBlind(-(socket_height + base_thickness * 0.5))
)

# Chamfer the top edges (inner and outer)
female_part = female_part.faces(">Z").edges().chamfer(0.15)


# --- Create Male Part (Right) ---
# 1. Base Geometry
male_base = create_base()

# 2. Solid Pin Feature
male_pin = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .circle(stud_od / 2.0)
    .extrude(stud_height)
)

# 3. Combine and Refine
male_part = male_base.union(male_pin)

# Add fillet at the intersection
male_part = male_part.edges(
    cq.selectors.NearestToPointSelector((0, 0, base_thickness))
).fillet(0.4)

# Chamfer the top edge of the pin
male_part = male_part.faces(">Z").edges().chamfer(0.2)

# 4. Position the Male Part
male_part = male_part.translate((spacing, 0, 0))


# --- Final Result ---
result = female_part.union(male_part)