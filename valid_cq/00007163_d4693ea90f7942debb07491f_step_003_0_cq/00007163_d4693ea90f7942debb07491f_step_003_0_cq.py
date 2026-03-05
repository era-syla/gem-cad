import cadquery as cq

# Parametric dimensions
housing_outer_diameter = 40.0
housing_inner_diameter = 36.0  # Gives a 2mm wall thickness
housing_length = 15.0
housing_back_thickness = 2.0   # Thickness of the solid back wall

central_shaft_outer_diameter = 12.0
central_shaft_inner_diameter = 6.0
central_shaft_length = 30.0    # Length extending from the back face

arm_diameter = 3.0
arm_length = 40.0              # Length from the center of the housing

# 1. Create the main cylindrical housing (cup shape)
# Start with the solid cylinder
housing_outer = cq.Workplane("XY").circle(housing_outer_diameter / 2).extrude(housing_length)

# Create the hollow inside
# We cut from the front face inwards, leaving the back wall
housing_inner = (
    cq.Workplane("XY")
    .workplane(offset=housing_back_thickness)
    .circle(housing_inner_diameter / 2)
    .extrude(housing_length - housing_back_thickness, combine=False)
)

main_housing = housing_outer.cut(housing_inner)

# 2. Create the central hollow shaft
# It protrudes from the back wall center through the open side
central_shaft = (
    cq.Workplane("XY")
    .circle(central_shaft_outer_diameter / 2)
    .circle(central_shaft_inner_diameter / 2)
    .extrude(central_shaft_length)
)

# 3. Create the radial arm
# The arm sticks out of the side of the housing
# We position it halfway along the housing length or aligned with the back, 
# but visually it seems attached to the main cylindrical body.
arm = (
    cq.Workplane("XZ")
    .workplane(offset=housing_outer_diameter/2 - 2.0) # Embed slightly into the wall
    .center(0, housing_length / 2) # Center it along the housing length
    .circle(arm_diameter / 2)
    .extrude(arm_length)
)

# Combine all parts
result = main_housing.union(central_shaft).union(arm)

# Export or display (standard practice, but user asked for 'result' variable)
# show_object(result)