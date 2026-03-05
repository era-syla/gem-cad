import cadquery as cq

# Define parametric dimensions
length = 150.0   # Total length of the plate
width = 50.0     # Total width of the plate
thickness = 3.0  # Thickness of the plate
hole_diameter = 4.0 # Diameter of the mounting holes
hole_inset_x = 10.0 # Distance from the short edge to the hole center
hole_inset_y = 8.0  # Distance from the long edge to the hole center

# Calculate hole center positions relative to the plate center
# The plate will be centered at (0,0), so we use half dimensions
x_pos = length / 2.0 - hole_inset_x
y_pos = width / 2.0 - hole_inset_y

# Create the base plate
plate = cq.Workplane("XY").box(length, width, thickness)

# Create the hole pattern
# We use rect to define a rectangular pattern for the hole centers
result = (
    plate
    .faces(">Z")
    .workplane()
    .rect(2 * x_pos, 2 * y_pos, forConstruction=True)
    .vertices()
    .hole(hole_diameter)
)

# Export or visualization would typically happen here, 
# but per instructions, we just ensure 'result' is defined.