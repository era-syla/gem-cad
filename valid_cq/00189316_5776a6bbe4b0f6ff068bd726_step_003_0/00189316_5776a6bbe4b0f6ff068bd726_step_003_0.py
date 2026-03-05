import cadquery as cq

# --- Parametric Dimensions ---
length = 150.0          # Total length of the tube
outer_diameter = 20.0   # Outer diameter of the tube
wall_thickness = 2.0    # Thickness of the tube wall

# --- Calculations ---
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# --- Geometry Generation ---
# Create a workplane, draw two concentric circles, and extrude.
# Drawing a smaller circle inside a larger one creates a hollow profile upon extrusion.
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(length)
)