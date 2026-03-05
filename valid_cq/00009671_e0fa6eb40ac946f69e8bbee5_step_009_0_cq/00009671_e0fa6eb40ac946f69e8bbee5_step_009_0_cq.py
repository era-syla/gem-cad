import cadquery as cq

# Parametric dimensions
base_diameter = 10.0
base_height = 15.0

housing_diameter = 16.0
housing_height = 15.0
housing_wall_thickness = 2.0  # Estimated wall thickness for the cup shape

pin_diameter = 3.0
pin_height = 25.0  # Height extending above the housing base

# 1. Create the bottom cylindrical base
base = cq.Workplane("XY").circle(base_diameter / 2).extrude(base_height)

# 2. Create the main housing body on top of the base
# We start a new workplane on top of the base
housing = (
    base.faces(">Z")
    .workplane()
    .circle(housing_diameter / 2)
    .extrude(housing_height)
)

# 3. Hollow out the housing to create the cup shape
# We select the top face of the housing and cut a hole
# The depth will be the housing height minus the floor thickness (assumed similar to wall thickness)
floor_thickness = 3.0
cut_depth = housing_height - floor_thickness

housing_hollow = (
    housing.faces(">Z")
    .workplane()
    .circle((housing_diameter - 2 * housing_wall_thickness) / 2)
    .cutBlind(-cut_depth)
)

# 4. Create the central pin
# The pin starts from the floor of the cup (which is at base_height + floor_thickness)
# It extends upwards.
pin_total_length = pin_height + (housing_height - floor_thickness)

# We can add the pin relative to the bottom of the "cup" floor
# The Z-level of the cup floor is base_height + floor_thickness
# Alternatively, simply place it on the original base top plane and extrude through
pin = (
    base.faces(">Z")
    .workplane(offset=floor_thickness)
    .circle(pin_diameter / 2)
    .extrude(pin_height)
)

# Combine everything into the final result
result = housing_hollow.union(pin)