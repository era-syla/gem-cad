import cadquery as cq
import math

# --- Parametric Dimensions ---
# These dimensions can be adjusted to modify the shape
base_diameter = 100.0  # Diameter of the object's base
top_diameter = 35.0    # Diameter of the flat top face
height = 25.0          # Total height of the object

# --- Geometry Calculation ---
# The shape is modeled as a segment of a sphere (truncated spherical cap).
# We calculate the radius and center position of the underlying sphere
# based on the base radius, top radius, and height.

r_base = base_diameter / 2.0
r_top = top_diameter / 2.0

# Calculate the vertical position (z) of the sphere's center relative to the base (z=0).
# Using the Pythagorean theorem on the cross-section:
# R^2 = r_base^2 + center_z^2
# R^2 = r_top^2 + (height - center_z)^2
# Solving for center_z:
center_z = (r_top**2 + height**2 - r_base**2) / (2 * height)

# Calculate the sphere radius
sphere_radius = math.sqrt(r_base**2 + center_z**2)

# Size for cutting tools (must be larger than the sphere)
cut_box_size = sphere_radius * 4.0

# --- Model Generation ---
result = (
    cq.Workplane("XY")
    # 1. Create the base sphere
    .sphere(sphere_radius)
    # 2. Position the sphere so the correct slice aligns with Z=0 to Z=height
    .translate((0, 0, center_z))
    # 3. Cut off the bottom (everything below Z=0)
    .cut(
        cq.Workplane("XY")
        .rect(cut_box_size, cut_box_size)
        .extrude(-cut_box_size)
    )
    # 4. Cut off the top (everything above Z=height)
    .cut(
        cq.Workplane("XY")
        .workplane(offset=height)
        .rect(cut_box_size, cut_box_size)
        .extrude(cut_box_size)
    )
)