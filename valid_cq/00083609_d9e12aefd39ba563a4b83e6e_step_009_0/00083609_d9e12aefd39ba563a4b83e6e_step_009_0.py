import cadquery as cq

# Parametric dimensions
length = 200.0       # Total length of the plate
height = 100.0       # Total height/width of the plate
thickness = 10.0     # Thickness of the plate
hole_diameter = 10.0 # Diameter of the mounting holes
margin = 20.0        # Distance from edge to hole center

# Calculate distance between hole centers based on margins
rect_width = length - (2 * margin)
rect_height = height - (2 * margin)

# Generate the CAD model
result = (
    cq.Workplane("XY")
    .box(length, height, thickness)  # Create the base rectangular plate
    .faces(">Z")                     # Select the top face
    .workplane()                     # Create a new workplane on the top face
    .rect(rect_width, rect_height, forConstruction=True) # Create construction geometry for hole placement
    .vertices()                      # Select the vertices of the construction rectangle
    .hole(hole_diameter)             # Cut holes at selected vertices
)