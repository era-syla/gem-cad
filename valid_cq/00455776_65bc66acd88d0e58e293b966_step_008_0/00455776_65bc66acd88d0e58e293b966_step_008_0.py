import cadquery as cq

# Parametric dimensions
outer_radius = 20.0
thickness = 10.0
lobe_radius = outer_radius / 2.0

# Generate the geometry
# The shape is constructed using three continuous arcs resembling a Yin-Yang section:
# 1. A large semi-circle on the left.
# 2. A smaller semi-circle forming the top lobe.
# 3. A smaller semi-circle forming the bottom cutout.
result = (
    cq.Workplane("XY")
    .moveTo(0, -outer_radius)  # Start at the bottom tail tip
    # Large outer arc (CCW from bottom to top)
    .threePointArc((-outer_radius, 0), (0, outer_radius))
    # Top lobe arc (CW from top to center)
    .threePointArc((lobe_radius, lobe_radius), (0, 0))
    # Bottom cutout arc (CW from center to bottom)
    .threePointArc((lobe_radius, -lobe_radius), (0, -outer_radius))
    .close()
    .extrude(thickness)
)