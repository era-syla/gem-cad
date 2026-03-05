import cadquery as cq

# Parametric dimensions based on visual estimation from the image
# All units in mm

# Dimensions for the small pins at both ends
pin_diameter = 6.0
pin_length = 8.0

# Dimensions for the large collar/shoulder on the left side
collar_diameter = 14.0
collar_length = 12.0

# Dimensions for the main central shaft
main_shaft_diameter = 10.0
main_shaft_length = 100.0

# Create the model by stacking cylinders along the X-axis
# 1. Start with the Left Pin
result = (
    cq.Workplane("YZ")
    .circle(pin_diameter / 2.0)
    .extrude(pin_length)
)

# 2. Add the Collar (Step up in diameter)
result = (
    result.faces(">X")
    .workplane()
    .circle(collar_diameter / 2.0)
    .extrude(collar_length)
)

# 3. Add the Main Shaft (Step down in diameter)
result = (
    result.faces(">X")
    .workplane()
    .circle(main_shaft_diameter / 2.0)
    .extrude(main_shaft_length)
)

# 4. Add the Right Pin (Step down in diameter)
result = (
    result.faces(">X")
    .workplane()
    .circle(pin_diameter / 2.0)
    .extrude(pin_length)
)