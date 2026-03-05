import cadquery as cq

# Parametric dimensions
base_diameter = 50.0   # Diameter of the main circular plate
base_thickness = 2.0   # Thickness of the main circular plate
pin_diameter = 8.0     # Diameter of the upright pin
pin_height = 15.0      # Height of the upright pin from the top surface
pin_offset = 18.0      # Distance from center to the pin location
center_boss_dia = 6.0  # Diameter of the small protrusion underneath
center_boss_h = 3.0    # Height of the small protrusion underneath

# Create the base plate
# We start with a workplane on the XY plane
result = (
    cq.Workplane("XY")
    .circle(base_diameter / 2.0)
    .extrude(base_thickness)
)

# Add the upright pin
# We select the top face of the base plate to sketch on
result = (
    result.faces(">Z")
    .workplane()
    .center(pin_offset, 0)  # Move sketching position to the offset location
    .circle(pin_diameter / 2.0)
    .extrude(pin_height)
)

# Add the center boss underneath
# We select the bottom face of the base plate
result = (
    result.faces("<Z")
    .workplane()
    .center(0, 0)  # Ensure we are at the center (relative to the face center)
    .circle(center_boss_dia / 2.0)
    .extrude(center_boss_h)
)

# If this were run in a CQ editor, 'show_object(result)' would be used.
# The variable 'result' holds the final geometry.