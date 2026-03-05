import cadquery as cq

# A spool/pulley shape: two flanges connected by a hub with a groove in the middle
# and a central hole through the axis

outer_radius = 30
flange_thickness = 5
hub_radius = 18
hub_length = 20
groove_depth = 5
groove_width = 10
hole_radius = 8

# Create the spool by revolving a profile
# Profile points (2D, in the XZ plane, revolving around Z axis)
# We'll build this as a revolved profile

profile = (
    cq.Workplane("XZ")
    .moveTo(hole_radius, 0)
    # Bottom flange bottom face
    .lineTo(outer_radius, 0)
    # Bottom flange outer edge
    .lineTo(outer_radius, flange_thickness)
    # Transition to hub
    .lineTo(hub_radius, flange_thickness)
    # Hub side
    .lineTo(hub_radius, flange_thickness + (hub_length - groove_width) / 2)
    # Groove bottom
    .lineTo(hub_radius - groove_depth, flange_thickness + (hub_length - groove_width) / 2)
    .lineTo(hub_radius - groove_depth, flange_thickness + (hub_length - groove_width) / 2 + groove_width)
    .lineTo(hub_radius, flange_thickness + (hub_length - groove_width) / 2 + groove_width)
    # Hub top side
    .lineTo(hub_radius, flange_thickness + hub_length)
    # Top flange inner
    .lineTo(outer_radius, flange_thickness + hub_length)
    # Top flange outer edge
    .lineTo(outer_radius, 2 * flange_thickness + hub_length)
    # Top face
    .lineTo(hole_radius, 2 * flange_thickness + hub_length)
    # Inner hole
    .lineTo(hole_radius, 0)
    .close()
)

result = profile.revolve(360, (0, 0, 0), (0, 1, 0))