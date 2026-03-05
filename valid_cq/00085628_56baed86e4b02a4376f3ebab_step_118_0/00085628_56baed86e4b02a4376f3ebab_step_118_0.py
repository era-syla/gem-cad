import cadquery as cq

# Geometric parameters based on visual proportions
height = 50.0           # Total height of the cylinder
outer_diameter = 24.0   # Outer diameter of the body
inner_diameter = 10.0   # Diameter of the through-hole
csk_diameter = 16.0     # Diameter of the countersink at the top edge
csk_angle = 90.0        # Angle of the countersink (standard 90 degrees)

# Generate the model
# 1. Start with the base cylinder extruding along the Z-axis
# 2. Select the top face (>Z)
# 3. Create a countersunk hole (cskHole) which cuts through the part
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(height)
    .faces(">Z")
    .workplane()
    .cskHole(
        diameter=inner_diameter,
        cskDiameter=csk_diameter,
        cskAngle=csk_angle,
        depth=None  # None implies a through-hole
    )
)