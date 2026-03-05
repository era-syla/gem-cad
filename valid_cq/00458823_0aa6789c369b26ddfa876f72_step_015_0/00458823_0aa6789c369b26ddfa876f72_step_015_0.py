import cadquery as cq

# Parametric dimensions
center_dist = 100.0  # Distance between hole centers
hub_diam = 40.0      # Outer diameter of the end hubs
hub_thick = 30.0     # Thickness (height) of the hubs
hole_diam = 20.0     # Diameter of the through holes
bar_width = 25.0     # Width of the connecting bar
bar_thick = 15.0     # Thickness of the connecting bar

# Create the two cylindrical hubs
# We center the extrusion on the Z-axis to make symmetry easier
hubs = (
    cq.Workplane("XY")
    .pushPoints([(-center_dist / 2, 0), (center_dist / 2, 0)])
    .circle(hub_diam / 2)
    .extrude(hub_thick)
    .translate((0, 0, -hub_thick / 2))
)

# Create the connecting rectangular bar
# The rectangle length matches center_dist, so it reaches the center of each hub
bar = (
    cq.Workplane("XY")
    .rect(center_dist, bar_width)
    .extrude(bar_thick)
    .translate((0, 0, -bar_thick / 2))
)

# Union the shapes and cut the holes
result = (
    hubs.union(bar)
    .faces(">Z").workplane()
    .pushPoints([(-center_dist / 2, 0), (center_dist / 2, 0)])
    .hole(hole_diam)
)