import cadquery as cq

# Parametric dimensions
plate_length = 200.0  # Length of the plate
plate_width = 100.0   # Width of the plate
plate_thickness = 10.0 # Thickness of the plate
hole_diameter = 8.0    # Diameter of the through holes
hole_inset_x = 15.0    # Distance from hole center to edge along X
hole_inset_y = 15.0    # Distance from hole center to edge along Y

# Calculate hole positions
# We will use the center of the plate as the origin (0,0,0)
# Holes are symmetric
x_pos = (plate_length / 2) - hole_inset_x
y_pos = (plate_width / 2) - hole_inset_y

# Create the base plate
result = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .faces(">Z")
    .workplane()
    .rect(2 * x_pos, 2 * y_pos, forConstruction=True) # Construction rectangle for hole placement
    .vertices()
    .cboreHole(hole_diameter, hole_diameter * 1.8, hole_diameter * 0.5) # Countersunk/Counterbored holes
)

# If standard holes are preferred over counterbore (image is ambiguous, could be just holes):
# Use .hole(hole_diameter) instead of .cboreHole(...) if simple holes are needed.
# Based on visual cue of "double circle" usually implying a chamfer or counterbore, 
# but often simple holes look like that in low-res. 
# Let's stick to simple holes as they are the most robust interpretation of "four holes".
# However, looking closely at the top right hole, it looks like a simple through hole.

result = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .faces(">Z")
    .workplane()
    .pushPoints([
        (-x_pos, -y_pos),
        (x_pos, -y_pos),
        (x_pos, y_pos),
        (-x_pos, y_pos)
    ])
    .hole(hole_diameter)
)