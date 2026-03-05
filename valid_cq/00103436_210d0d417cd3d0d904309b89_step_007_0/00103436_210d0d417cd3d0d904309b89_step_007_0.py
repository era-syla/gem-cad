import cadquery as cq
import math

# --- Parametric Dimensions ---
base_radius_bottom = 18.0
base_radius_top = 12.0
base_height = 14.0

collar_height = 5.0
collar_bulge_radius = 13.5  # The protrusion radius of the mid-section ring
upper_cone_base_radius = 11.0

upper_cone_height = 28.0
neck_radius = 5.0

head_radius = 8.0

# --- Geometry Calculation ---
z_base_top = base_height
z_collar_top = z_base_top + collar_height
z_neck = z_collar_top + upper_cone_height

# Calculate sphere center height so it sits perfectly on the neck rim
# h = sqrt(R^2 - r^2)
sphere_vertical_offset = math.sqrt(head_radius**2 - neck_radius**2)
z_sphere_center = z_neck + sphere_vertical_offset

# --- Modeling ---

# 1. Create the main body (Base + Collar + Upper Cone) via Revolution
# We define the profile on the XZ plane and revolve around the Z axis.
body = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(base_radius_bottom, 0)
    .lineTo(base_radius_top, z_base_top)
    # Create the bulging collar using a 3-point arc
    .threePointArc(
        (collar_bulge_radius, z_base_top + collar_height / 2.0), # Arc Midpoint
        (upper_cone_base_radius, z_collar_top)                   # Arc Endpoint
    )
    .lineTo(neck_radius, z_neck)
    .lineTo(0, z_neck)
    .close()
    .revolve()
)

# 2. Create the Spherical Head
head = (
    cq.Workplane("XY")
    .workplane(offset=z_sphere_center)
    .sphere(head_radius)
)

# 3. Combine parts into final object
result = body.union(head)