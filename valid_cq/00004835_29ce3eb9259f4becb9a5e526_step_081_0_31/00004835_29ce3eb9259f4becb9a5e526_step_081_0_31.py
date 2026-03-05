import cadquery as cq

# Parameters for the modeled strip
length = 200.0
width = 5.0
thickness = 1.5

num_grooves = 20
spacing = length / num_grooves
groove_height = spacing * 0.25
groove_depth = thickness * 0.4

# Create the base flat strip
base = cq.Workplane("XY").box(width, thickness, length)

# Calculate center positions for each of the grooves along the strip
# The face ">Y" will have its local Y-axis aligned with the global Z-axis
pts = [(0, -length/2 + spacing/2 + i * spacing) for i in range(num_grooves)]

# Cut the grooves into the front face
result = (
    base.faces(">Y").workplane()
    .pushPoints(pts)
    .rect(width + 2.0, groove_height) # Slightly wider than the strip to ensure a clean cut across
    .cutBlind(-groove_depth)
)