import cadquery as cq

# Parameters for the U-shaped tube/rod
total_length = 300.0   # Total length from the open end to the tip of the bend
rod_diameter = 6.0     # Diameter of the main tube/rod sections
bend_radius = 25.0     # Radius of the semi-circular bend (centerline)
gap_between_rods = bend_radius * 2

# The straight section length needs to account for the bend
straight_length = total_length - bend_radius

# Connection/step details (the slight bulges visible on the rod)
connector_diameter = 7.0
connector_length = 5.0
connector_pos_ratio = 0.5 # Position of the connector along the straight part (0 to 1)

# 1. Create the main U-shape path
# We will draw a path on the XY plane:
# Start at one end, go straight, arc 180 degrees, go straight back.
path = (
    cq.Workplane("XY")
    .moveTo(0, gap_between_rods / 2)
    .lineTo(straight_length, gap_between_rods / 2)
    .threePointArc((straight_length + bend_radius, 0), (straight_length, -gap_between_rods / 2))
    .lineTo(0, -gap_between_rods / 2)
)

# 2. Sweep a circular profile along the path to create the main body
main_body = (
    cq.Workplane("YZ")
    .circle(rod_diameter / 2)
    .sweep(path)
)

# 3. Create the connector "bulges"
# We place these at a specific distance along the straight sections
connector_x_pos = straight_length * connector_pos_ratio

# Upper leg connector
connector_top = (
    cq.Workplane("YZ")
    .workplane(offset=connector_x_pos)
    .center(0, gap_between_rods / 2) # Center on top rod axis
    .circle(connector_diameter / 2)
    .extrude(connector_length, both=True) # Extrude symmetrically
)

# Lower leg connector
connector_bottom = (
    cq.Workplane("YZ")
    .workplane(offset=connector_x_pos)
    .center(0, -gap_between_rods / 2) # Center on bottom rod axis
    .circle(connector_diameter / 2)
    .extrude(connector_length, both=True) # Extrude symmetrically
)

# 4. Create the connection bulges near the bend (visible in image)
# Often heating elements have a slightly thicker section right at the start of the bend
bend_connector_x_pos = straight_length

bend_connector_top = (
    cq.Workplane("YZ")
    .workplane(offset=bend_connector_x_pos)
    .center(0, gap_between_rods / 2)
    .circle(connector_diameter / 2)
    .extrude(connector_length/2, both=True)
)

bend_connector_bottom = (
    cq.Workplane("YZ")
    .workplane(offset=bend_connector_x_pos)
    .center(0, -gap_between_rods / 2)
    .circle(connector_diameter / 2)
    .extrude(connector_length/2, both=True)
)


# Combine all parts
result = (
    main_body
    .union(connector_top)
    .union(connector_bottom)
    .union(bend_connector_top)
    .union(bend_connector_bottom)
)