import cadquery as cq

# Parametric dimensions for the droplet
height = 24.0        # Total height of the droplet (tip to bottom)
max_radius = 10.0    # Maximum radius of the droplet body
bulge_height = 8.0   # Height (from bottom) where the radius is maximum

# Create the droplet geometry
# Strategy: Draw half the profile on the XZ plane and revolve around the Z-axis
result = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(0, height)  # Draw the central vertical axis
    .spline(
        # Define spline points: from top tip, through max width, to bottom center
        [(max_radius, bulge_height), (0, 0)],
        # Define tangents to control shape:
        # Start (Top): Downwards and slightly outwards for a sharp tip (vector: dx, dy)
        # End (Bottom): Horizontal towards the axis for a smooth rounded bottom
        tangents=[(0.4, -1.0), (-1.0, 0.0)],
        includeCurrent=True
    )
    .close()  # Ensure the wire is closed
    .revolve(360, (0, 0, 0), (0, 0, 1))  # Revolve around the Global Z axis
)