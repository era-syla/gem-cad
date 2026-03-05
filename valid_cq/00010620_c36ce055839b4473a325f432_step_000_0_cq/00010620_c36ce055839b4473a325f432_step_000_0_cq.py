import cadquery as cq

# Parametric dimensions
main_diameter = 50.0  # Diameter of the main central cylinder
main_height = 20.0    # Height of the main cylinder
lug_radius = 5.0      # Radius of the mounting ears (lugs)
lug_offset = 28.0     # Distance from center to center of lug
hole_diameter = 4.0   # Diameter of the screw holes in the lugs

# Create the main cylindrical body
main_body = cq.Workplane("XY").circle(main_diameter / 2).extrude(main_height)

# Create the lugs
# We'll create one lug shape and then union it with the main body
# Lugs are typically positioned on opposite sides
lug_sketch = (
    cq.Workplane("XY")
    .moveTo(lug_offset, 0)
    .circle(lug_radius)
    .moveTo(-lug_offset, 0)
    .circle(lug_radius)
)
lugs = lug_sketch.extrude(main_height)

# Combine the main body and the lugs
combined_shape = main_body.union(lugs)

# Create the mounting holes
# We'll select the top face and drill holes at the lug centers
result = (
    combined_shape
    .faces(">Z")
    .workplane()
    .pushPoints([(lug_offset, 0), (-lug_offset, 0)])
    .hole(hole_diameter)
)

# Optional: Add fillets for a smoother transition if needed (not strictly visible in image but good practice)
# result = result.edges("|Z").fillet(1.0) # Not applying to keep strictly to image geometry which looks sharp-edged at junctions

# Export the result for visualization (optional in script, but 'result' variable is required)