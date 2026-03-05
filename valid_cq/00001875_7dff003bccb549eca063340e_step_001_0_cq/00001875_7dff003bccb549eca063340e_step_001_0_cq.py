import cadquery as cq

# Parametric dimensions
diameter = 100.0   # Diameter of the main semi-circle
thickness = 5.0    # Thickness of the plate
cutout_radius = 10.0 # Radius of the central cutout

# Derived dimensions
radius = diameter / 2.0

# Create the main semi-circle shape
# We start with a circle, cut it in half, and then extrude.
# Alternatively, we can sketch the profile directly.

# Method: Create a sketch of the profile and extrude
result = (
    cq.Workplane("XY")
    # Draw the outer arc (180 degrees)
    .moveTo(radius, 0)
    .threePointArc((0, radius), (-radius, 0))
    # Draw the straight line back to the center, but stop for the cutout
    .lineTo(-cutout_radius, 0)
    # Draw the inner cutout arc (negative direction to dig into the shape)
    .threePointArc((0, cutout_radius), (cutout_radius, 0))
    # Close the shape
    .close()
    # Extrude to thickness
    .extrude(thickness)
)

# Alternative simpler approach using boolean operations which might be more robust
# Create a full disc
base_disc = cq.Workplane("XY").circle(radius).extrude(thickness)

# Create a rectangle to cut the disc in half
cut_rect = (
    cq.Workplane("XY")
    .rect(diameter * 1.5, diameter) # Make it large enough to cover half
    .extrude(thickness)
    .translate((0, -diameter/2.0, 0)) # Shift it to cover the bottom half
)

# Create the central cutout cylinder
cutout_cyl = (
    cq.Workplane("XY")
    .circle(cutout_radius)
    .extrude(thickness)
)

# Combine operations: Base disc MINUS bottom half MINUS central hole
# Note: The visual shows the straight edge is aligned with the X-axis.
# Let's rebuild simply using a sketch for cleaner geometry.

result = (
    cq.Workplane("XY")
    .moveTo(radius, 0)
    .threePointArc((0, radius), (-radius, 0))
    .lineTo(-cutout_radius, 0)
    # The cutout is a semi-circle indentation into the flat face.
    # Looking at the image, the cutout goes inwards.
    .threePointArc((0, cutout_radius), (cutout_radius, 0))
    .close()
    .extrude(thickness)
)