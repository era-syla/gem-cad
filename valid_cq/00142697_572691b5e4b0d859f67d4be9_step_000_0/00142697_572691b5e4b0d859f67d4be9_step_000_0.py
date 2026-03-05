import cadquery as cq

# Parametric dimensions
center_distance = 80.0   # Distance between the centers of the circular ends
end_radius = 12.5        # Radius of the rounded ends
bar_width = 16.0         # Width of the central connecting bar
thickness = 5.0          # Thickness of the part

# Create the central rectangular section
# We extrude a centered rectangle. Z-extrusion starts from XY plane.
bar = cq.Workplane("XY").rect(center_distance, bar_width).extrude(thickness)

# Create the left circular end
# We move the workplane center to the left, draw a circle, and extrude.
left_end = (
    cq.Workplane("XY")
    .center(-center_distance / 2.0, 0)
    .circle(end_radius)
    .extrude(thickness)
)

# Create the right circular end
# We move the workplane center to the right, draw a circle, and extrude.
right_end = (
    cq.Workplane("XY")
    .center(center_distance / 2.0, 0)
    .circle(end_radius)
    .extrude(thickness)
)

# Combine the three solids into one single geometry
result = bar.union(left_end).union(right_end)