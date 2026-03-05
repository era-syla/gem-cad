import cadquery as cq

# Define parametric dimensions
disk_radius = 6.0
disk_thickness = 1.5

# Define the positions for the two disks to match the diagonal layout
# Point 1: Top-left relative to origin
# Point 2: Bottom-right relative to origin
positions = [
    (-30, 20), 
    (30, -20)
]

# Create the model by pushing points to the workplane and extruding circles
result = (
    cq.Workplane("XY")
    .pushPoints(positions)
    .circle(disk_radius)
    .extrude(disk_thickness)
)