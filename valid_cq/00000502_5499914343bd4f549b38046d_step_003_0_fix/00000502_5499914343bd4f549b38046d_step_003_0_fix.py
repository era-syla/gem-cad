import cadquery as cq
import math

# Create a curved tube/rod shape - appears to be a curved cylindrical rod
# that follows an arc path

# Define the arc path for sweeping
# The shape looks like a curved rod/handle with circular cross-section

# Create the sweep path as an arc
path = (
    cq.Workplane("XY")
    .moveTo(-60, 0)
    .threePointArc((0, 30), (60, 0))
)

# Create the circular cross-section profile
profile = cq.Workplane("YZ").circle(6)

# Sweep the circle along the arc path
result = profile.sweep(path)