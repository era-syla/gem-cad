import cadquery as cq

# Parametric dimensions
length = 120.0     # Total length along the X-axis
width = 15.0       # Depth/Width along the Y-axis
height = 20.0      # Height of the vertical flanges along the Z-axis
thickness = 3.0    # Thickness of the material

# Define points for the U-shaped cross-section profile on the XZ plane
# Starting from top-left vertical flange
pts = [
    (0, height),                       # Top-left outer
    (0, 0),                            # Bottom-left outer
    (length, 0),                       # Bottom-right outer
    (length, height),                  # Top-right outer
    (length - thickness, height),      # Top-right inner
    (length - thickness, thickness),   # Bottom-right inner
    (thickness, thickness),            # Bottom-left inner
    (thickness, height)                # Top-left inner
]

# Generate the 3D model
result = (
    cq.Workplane("XZ")                 # Create workplane on Front plane
    .polyline(pts)                     # Draw the profile
    .close()                           # Close the sketch
    .extrude(width)                    # Extrude to give it depth
)