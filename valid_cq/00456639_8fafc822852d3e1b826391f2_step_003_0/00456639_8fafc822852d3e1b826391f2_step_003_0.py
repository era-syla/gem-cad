import cadquery as cq

# Parametric dimensions
radius_mean = 35.0      # Radius to the center of the curved path
arc_width = 10.0        # Width of the curved base
arc_height = 4.0        # Thickness of the curved base
pillar_side = 5.0       # Side length of the square pillars
gap = 6.0               # Gap between the arc and first pillar, and between pillars
pillar_heights = [40.0, 60.0, 80.0] # Heights of the pillars from shortest to tallest

# 1. Create the Curved Base
# Sketch a rectangle on the XZ plane offset by the radius
# Revolve 180 degrees around the Z-axis to create a semi-circle
# The resulting solid spans from angle 0 (X-axis) to 180 degrees
result = (
    cq.Workplane("XZ")
    .moveTo(radius_mean, arc_height / 2.0)
    .rect(arc_width, arc_height)
    .revolve(180, (0, 0, 0), (0, 0, 1))
)

# 2. Create and Add the Pillars
# The pillars are positioned linearly starting near the end of the arc (y=0)
# and extending in the negative Y direction
current_y_center = -(gap + pillar_side / 2.0)

for h in pillar_heights:
    pillar = (
        cq.Workplane("XY")
        .moveTo(radius_mean, current_y_center)
        .rect(pillar_side, pillar_side)
        .extrude(h)
    )
    
    # Combine the pillar with the base geometry
    result = result.union(pillar)
    
    # Calculate Y position for the next pillar
    current_y_center -= (pillar_side + gap)