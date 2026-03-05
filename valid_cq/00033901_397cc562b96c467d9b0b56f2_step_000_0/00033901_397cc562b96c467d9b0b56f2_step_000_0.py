import cadquery as cq

# -- Parametric Dimensions --
# Main body dimensions
main_dia = 20.0
main_length = 60.0
main_bottom_fillet_radius = 1.0

# Bottom protrusion dimensions
base_dia = 12.0
base_length = 4.0

# Tapered section (shoulder) dimensions
taper_height = 10.0
neck_dia = 10.0

# Neck dimensions
neck_length = 8.0

# Tip dimensions
tip_dia = 5.0
tip_cyl_length = 2.5

# -- Geometry Construction --

# 1. Base Protrusion
# Creates the small cylinder at the bottom
base = cq.Workplane("XY").circle(base_dia / 2.0).extrude(base_length)

# 2. Main Cylindrical Body
# Constructed on top of the base level.
# Created as a separate object initially to allow robust edge selection for the fillet.
main_body_wp = cq.Workplane("XY").workplane(offset=base_length)
main_body = (
    main_body_wp
    .circle(main_dia / 2.0)
    .extrude(main_length)
)

# Apply fillet to the bottom edge of the main body where it overhangs the base
# We select the edges at the lowest Z coordinate of this specific solid
main_body = main_body.edges("<Z").fillet(main_bottom_fillet_radius)

# 3. Tapered Transition (Shoulder)
# Loft from Main Diameter to Neck Diameter
z_taper_start = base_length + main_length
taper = (
    cq.Workplane("XY")
    .workplane(offset=z_taper_start)
    .circle(main_dia / 2.0)
    .workplane(offset=taper_height)
    .circle(neck_dia / 2.0)
    .loft()
)

# 4. Neck Section
z_neck_start = z_taper_start + taper_height
neck = (
    cq.Workplane("XY")
    .workplane(offset=z_neck_start)
    .circle(neck_dia / 2.0)
    .extrude(neck_length)
)

# 5. Tip Section
# Cylinder with a hemispherical dome on top
z_tip_start = z_neck_start + neck_length
tip = (
    cq.Workplane("XY")
    .workplane(offset=z_tip_start)
    .circle(tip_dia / 2.0)
    .extrude(tip_cyl_length)
)

# Create the dome by filleting the top edge
# Radius is set to approx half the diameter to create a hemisphere
tip = tip.edges(">Z").fillet((tip_dia / 2.0) - 0.01)

# -- Final Assembly --
# Union all components into the final result
result = base.union(main_body).union(taper).union(neck).union(tip)