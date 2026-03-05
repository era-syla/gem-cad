import cadquery as cq

# Geometric parameters to define the shape proportions
base_diameter = 12.0
tip_diameter = 4.5
total_height = 35.0
cylinder_height = 10.0  # Height of the straight cylindrical base section

# Derived radii
base_radius = base_diameter / 2.0
tip_radius = tip_diameter / 2.0

# Construct the model using a revolution profile
# Drawing on the XZ plane allows revolving around the Z axis
result = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(base_radius, 0)                  # Bottom radius
    .lineTo(base_radius, cylinder_height)    # Vertical cylindrical side
    # Create the curved ogive section. 
    # tangentArcPoint ensures the curve is tangent to the previous vertical line,
    # creating a smooth transition typical of this geometry.
    .tangentArcPoint((tip_radius, total_height), relative=False)
    .lineTo(0, total_height)                 # Flat top (meplat)
    .close()
    .revolve()                               # Generate the solid
)