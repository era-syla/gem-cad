import cadquery as cq

# -- Parametric Dimensions --
# Heating Element Dimensions
tube_diameter = 10.0
tube_radius = tube_diameter / 2.0
tube_straight_length = 450.0  # Height of the vertical straight sections
tube_center_dist = 24.0       # Distance between the two tube centers

# Base/Plug Dimensions
flange_diameter = 42.0
flange_height = 8.0
seal_diameter = 38.0          # Slightly narrower section (gasket area)
seal_height = 4.0
body_diameter = 35.0          # Main plug body
body_length = 50.0

# -- Geometry Generation --

# 1. Define the Sweep Path for the heating U-tube
# We sketch on the XZ plane, with Z being the vertical axis.
# The path starts at the base (Z=0), goes up, arcs 180 degrees, and comes back down.
path = (
    cq.Workplane("XZ")
    .moveTo(-tube_center_dist / 2, 0)
    .lineTo(-tube_center_dist / 2, tube_straight_length)
    .threePointArc(
        (0, tube_straight_length + tube_center_dist / 2),  # Midpoint of the arc (apex)
        (tube_center_dist / 2, tube_straight_length)       # Endpoint of the arc
    )
    .lineTo(tube_center_dist / 2, 0)
)

# 2. Create the Tube Solid
# Create the circular profile on the XY plane at the start of the path and sweep it.
heating_element = (
    cq.Workplane("XY")
    .center(-tube_center_dist / 2, 0)
    .circle(tube_radius)
    .sweep(path)
)

# 3. Create the Base/Plug
# Constructed downwards from Z=0 so the tubes sit on top.
# We create a stack of cylinders: Flange -> Seal -> Main Body
base = (
    cq.Workplane("XY")
    .circle(flange_diameter / 2)
    .extrude(-flange_height)
    # Continue from the bottom face of the flange
    .faces("<Z").workplane()
    .circle(seal_diameter / 2)
    .extrude(-seal_height)
    # Continue from the bottom face of the seal section
    .faces("<Z").workplane()
    .circle(body_diameter / 2)
    .extrude(-body_length)
)

# 4. Final Result
# Combine the base and the heating element into a single solid
result = base.union(heating_element)