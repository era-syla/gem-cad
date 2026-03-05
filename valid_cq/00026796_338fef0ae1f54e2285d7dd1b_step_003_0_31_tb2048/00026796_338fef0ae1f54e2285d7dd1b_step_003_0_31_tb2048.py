import cadquery as cq

# Parametric dimensions
center_distance = 100.0  # Distance between the centers of the two holes
width = 15.0             # Overall width of the link (determines outer radius)
thickness = 4.0          # Thickness of the flat bar
hole_diameter = 6.0      # Diameter of the holes at each end

# Create the 3D model
result = (
    cq.Workplane("XY")
    # slot2D creates a capsule shape with specified distance between centers and width
    .slot2D(center_distance, width)
    .extrude(thickness)
    .faces(">Z")
    .workplane()
    # Position points at the center of the rounded ends for the holes
    .pushPoints([(-center_distance / 2.0, 0), (center_distance / 2.0, 0)])
    .hole(hole_diameter)
)