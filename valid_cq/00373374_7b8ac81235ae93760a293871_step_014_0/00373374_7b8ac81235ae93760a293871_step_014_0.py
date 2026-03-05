import cadquery as cq

# Parametric dimensions for the model
n_sides = 5           # Number of sides (Pentagon)
base_diameter = 30.0  # Diameter of the circumscribed circle for the base
top_diameter = 22.0   # Diameter of the circumscribed circle for the top
height = 6.0          # Height of the prism

# Generate the geometry using a loft operation
# This creates a tapered extrusion (frustum) by lofting between 
# a pentagon at the base and a smaller pentagon at the top height.
result = (
    cq.Workplane("XY")
    .polygon(n_sides, base_diameter)      # Create base pentagon wire
    .workplane(offset=height)             # Create a new workplane offset by the height
    .polygon(n_sides, top_diameter)       # Create top pentagon wire
    .loft()                               # Loft between the two wires to create the solid
)