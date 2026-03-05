import cadquery as cq

# --- Parameters ---
total_height = 90.0     # Total height of the rocket
body_radius = 11.0      # Radius of the fuselage at the base
fin_count = 4           # Number of fins
fin_span = 30.0         # Distance from center to fin tip
fin_tip_height = 8.0    # Height of the vertical edge at the fin tip
fin_root_height = 32.0  # Height where the fin meets the body
fin_thickness = 2.5     # Thickness of the fins

# --- 1. Fuselage Generation ---
# Create the main body profile on the XZ plane and revolve it.
# We use a spline to create the smooth ogive/aerodynamic shape.
fuselage = (
    cq.Workplane("XZ")
    .moveTo(0, 0)                       # Start at bottom center
    .lineTo(body_radius, 0)             # Line to bottom outer edge
    .spline(
        [(body_radius * 0.65, total_height * 0.4), (0, total_height)], 
        includeCurrent=True
    )                                   # Curve to the top tip
    .close()                            # Close back to (0,0)
    .revolve()                          # Revolve around Z axis
)

# --- 2. Fin Generation ---
# Create a single fin shape on the XZ plane.
# The shape is defined as a polygon that penetrates the center of the body 
# to ensure a solid connection.
fin_pts = [
    (0, 0),                       # Center bottom
    (fin_span, 0),                # Outer bottom tip
    (fin_span, fin_tip_height),   # Outer top tip
    (0, fin_root_height)          # Center top (inside fuselage)
]

base_fin = (
    cq.Workplane("XZ")
    .polyline(fin_pts)
    .close()
    .extrude(fin_thickness / 2.0, both=True) # Extrude symmetrically
)

# --- 3. Assembly ---
# Combine the fuselage with the fins in a circular pattern.
result = fuselage

for i in range(fin_count):
    angle = i * (360.0 / fin_count)
    # Rotate the base fin around the Z-axis (0,0,0 to 0,0,1)
    rotated_fin = base_fin.rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.union(rotated_fin)

# The 'result' variable now contains the final solid geometry.