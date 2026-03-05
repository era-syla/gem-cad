import cadquery as cq

# Parameters
center_distance = 100.0  # Distance between the centers of the two holes
width = 12.0             # Width of the bar
thickness = 4.0          # Thickness of the bar
hole_diameter = 5.0      # Diameter of the holes at each end

# Create the model
result = (
    cq.Workplane("XY")
    # Create the base capsule/slot shape
    .slot2D(center_distance, width)
    .extrude(thickness)
    # Select the top face to sketch the holes
    .faces(">Z")
    .workplane()
    # Place points at the arc centers for the holes
    .pushPoints([(-center_distance / 2, 0), (center_distance / 2, 0)])
    # Cut the holes through the part
    .hole(hole_diameter)
)