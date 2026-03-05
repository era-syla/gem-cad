import cadquery as cq

# Parametric dimensions based on visual estimation of the image
thickness = 3.0           # Thickness of the plate
outer_radius = 50.0       # Radius of the outer ring
rim_width = 5.0           # Width of the outer ring material
spoke_width = 5.0         # Width of the connecting cross arms
center_hub_radius = 12.0  # Radius of the central circular hub
center_hole_radius = 6.0  # Radius of the central hole
sat_hub_radius = 9.0      # Radius of the 4 satellite hubs on the arms
sat_hole_radius = 4.0     # Radius of the holes in the satellite hubs
sat_distance = 29.0       # Distance from center to satellite hub center

# 1. Create the outer ring (rim)
# We define an outer circle and an inner circle to form a ring profile, then extrude
rim = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(outer_radius - rim_width)
    .extrude(thickness)
)

# 2. Create the cross spokes
# To ensure the spokes merge cleanly into the rim without protruding outside the curvature,
# we set the length to end midway into the rim width.
# Length = Diameter - Rim Width
spoke_length = (outer_radius * 2) - rim_width

spokes = (
    cq.Workplane("XY")
    .rect(spoke_length, spoke_width)  # Horizontal arm
    .rect(spoke_width, spoke_length)  # Vertical arm
    .extrude(thickness)
)

# 3. Create the center hub
center_hub = (
    cq.Workplane("XY")
    .circle(center_hub_radius)
    .extrude(thickness)
)

# 4. Create the satellite hubs
# Use polar array to position 4 cylinders
satellite_hubs = (
    cq.Workplane("XY")
    .polarArray(sat_distance, 0, 360, 4)
    .circle(sat_hub_radius)
    .extrude(thickness)
)

# 5. Combine all additive geometry
# Union the rim, spokes, center hub, and satellite hubs into one solid
base_geo = rim.union(spokes).union(center_hub).union(satellite_hubs)

# 6. Create the cuts (holes)
# Cut the center hole
result = (
    base_geo.faces(">Z").workplane()
    .circle(center_hole_radius)
    .cutThruAll()
)

# Cut the satellite holes using the same polar array logic
result = (
    result.faces(">Z").workplane()
    .polarArray(sat_distance, 0, 360, 4)
    .circle(sat_hole_radius)
    .cutThruAll()
)