import cadquery as cq

# -- Parametric Dimensions --
length = 60.0       # Total length of the part
width = 20.0        # Width of the part
thickness = 5.0     # Thickness of the plate
hole_diameter = 10.0 # Diameter of the hole

# -- Derived Parameters --
# Calculate the offset from the center of the part to the center of the bottom radius
# Total length = 2 * radius + straight_section
# The offset is half the straight section length
radius = width / 2.0
center_offset = (length / 2.0) - radius

# -- Geometry Generation --
result = (
    cq.Workplane("XY")
    # Create the base stadium (slot) shape profile oriented vertically
    .slot2D(length, width, angle=90)
    # Extrude to create the solid geometry
    .extrude(thickness)
    # Select the top face to place the hole
    .faces(">Z")
    .workplane()
    # Move to the position of the bottom arc center
    .moveTo(0, -center_offset)
    # Cut the through hole
    .hole(hole_diameter)
)