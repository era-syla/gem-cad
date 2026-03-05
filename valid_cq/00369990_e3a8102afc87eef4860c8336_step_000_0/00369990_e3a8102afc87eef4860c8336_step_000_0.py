import cadquery as cq

# Parametric dimensions based on the visual estimation
height = 60.0          # Length of the part
base_radius = 20.0     # Radius at the wider end
top_radius = 12.0      # Radius at the narrower end
hole_radius = 8.0      # Radius of the internal cylindrical bore

# Method: Create a 2D profile of the wall cross-section and revolve it
# We sketch on the XZ plane. In this plane, the local Y axis aligns with the global Z axis.
# Default behavior of revolve() on a 2D sketch is to revolve around the local Y axis.
result = (
    cq.Workplane("XZ")
    .polyline([
        (hole_radius, 0),         # Bottom inner corner
        (base_radius, 0),         # Bottom outer corner
        (top_radius, height),     # Top outer corner
        (hole_radius, height),    # Top inner corner
        (hole_radius, 0)          # Close the loop back to start
    ])
    .close()
    .revolve()  # Revolve 360 degrees to create the solid
)