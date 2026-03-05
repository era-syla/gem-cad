import cadquery as cq

# Dimensions
length = 100.0    # Total length of the bar
width = 20.0      # Total width of the cross-section
height = 10.0     # Height (thickness) of the cross-section

# Derived dimensions for the profile
# The profile consists of a rectangle and a semi-circle end.
radius = height / 2.0
straight_section = width - radius

# Generate the CAD model
# Drawing the profile on the YZ plane and extruding along the X axis
result = (
    cq.Workplane("YZ")
    .moveTo(0, 0)
    .lineTo(0, height)                      # Vertical back edge
    .lineTo(straight_section, height)       # Top flat edge
    .threePointArc(
        (width, height / 2.0),              # Midpoint of the arc (the nose)
        (straight_section, 0)               # End point of the arc
    )
    .close()
    .extrude(length)
)