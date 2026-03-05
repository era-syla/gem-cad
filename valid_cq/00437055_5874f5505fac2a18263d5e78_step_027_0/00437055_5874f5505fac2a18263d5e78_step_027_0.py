import cadquery as cq

# --- Parametric Dimensions ---
# Main housing dimensions
housing_length = 24.0
housing_width = 11.0
housing_height = 5.5
housing_fillet = 0.5

# Connector plug dimensions (approx. USB-C geometry)
plug_length = 7.0
plug_width = 8.3
plug_height = 2.5
plug_corner_radius = (plug_height / 2.0) - 0.01  # Near-semicircle sides

# Cable dimensions
cable_length = 60.0
cable_diameter = 3.2

# --- Modeling ---

# 1. Housing Body
# Create a rectangular box centered at the origin
housing = cq.Workplane("XY").box(housing_length, housing_width, housing_height)
# Round the longitudinal edges to give it a finished look
housing = housing.edges("|X").fillet(housing_fillet)

# 2. Connector Plug
# Created on the YZ plane and extruded along +X
# We create a rectangle, extrude it, then fillet the side edges to create the "racetrack" profile
plug = (
    cq.Workplane("YZ")
    .rect(plug_width, plug_height)
    .extrude(plug_length)
    .edges("|X")
    .fillet(plug_corner_radius)
    .translate((housing_length / 2.0, 0, 0))  # Move to the front face of the housing
)

# 3. Cable
# Created on the YZ plane and extruded along -X (backwards)
cable = (
    cq.Workplane("YZ")
    .circle(cable_diameter / 2.0)
    .extrude(-cable_length)
    .translate((-housing_length / 2.0, 0, 0))  # Move to the back face of the housing
)

# 4. Assembly
# Union the parts together to form the final solid
result = housing.union(plug).union(cable)