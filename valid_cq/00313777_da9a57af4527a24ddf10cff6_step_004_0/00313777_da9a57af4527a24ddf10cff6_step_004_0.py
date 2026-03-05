import cadquery as cq
import math

# --- Parametric Dimensions ---
height = 60.0               # Total height of the object
max_diameter = 34.0         # Diameter at the widest point (equator)
hole_diameter = 8.0         # Diameter of the central through-hole
chamfer_size = 3.0          # Size of the top countersink/chamfer
truncation_factor = 1.25    # Controls the curvature (1.0 = perfect sphere/ellipse ends, >1.0 = truncated)

# --- Derived Values ---
max_radius = max_diameter / 2.0
hole_radius = hole_diameter / 2.0
# Calculate the radii of the theoretical full ellipsoid
# r_z is half the height of the full ellipse
r_z = (height * truncation_factor) / 2.0
r_x = max_radius

# Define vertical bounds (centered at Z=0)
z_top = height / 2.0
z_bottom = -height / 2.0

# --- Geometry Generation ---

# Function to calculate X coordinate (radius) of ellipsoid at a given Z
def get_ellipsoid_x(z):
    # Ellipse equation: (x/rx)^2 + (z/rz)^2 = 1  =>  x = rx * sqrt(1 - (z/rz)^2)
    # Clamp term to 0 to prevent domain errors if z exceeds r_z slightly
    term = max(0, 1 - (z / r_z)**2)
    return r_x * math.sqrt(term)

# Generate points for the outer curved profile (Spline)
# We generate points from the bottom edge to the top edge
num_points = 30
outer_profile_points = []
for i in range(num_points + 1):
    z = z_bottom + (z_top - z_bottom) * (i / num_points)
    x = get_ellipsoid_x(z)
    outer_profile_points.append((x, z))

# Determine key points for the profile sketch
# Point 1: Bottom Inner (Start of hole)
p_hole_bottom = (hole_radius, z_bottom)
# Point 2: Bottom Outer (End of bottom flat face)
p_outer_bottom = outer_profile_points[0]
# Point 3: Top Outer (End of outer curve is the last point in our list)
# Point 4: Top Inner Chamfer Start (Outer edge of chamfer)
p_chamfer_top = (hole_radius + chamfer_size, z_top)
# Point 5: Top Inner Chamfer End (Inner edge of chamfer inside hole)
p_chamfer_bottom = (hole_radius, z_top - chamfer_size)

# Create the solid using a Revolve operation
# We draw the profile on the XZ plane and revolve around the Z axis
result = (
    cq.Workplane("XZ")
    .moveTo(*p_hole_bottom)                     # Start at bottom of hole
    .lineTo(*p_outer_bottom)                    # Draw bottom flat face
    .spline(outer_profile_points[1:], includeCurrent=True) # Draw curved outer surface
    .lineTo(*p_chamfer_top)                     # Draw top flat face
    .lineTo(*p_chamfer_bottom)                  # Draw chamfer slope
    .close()                                    # Close geometry back to start (creates the inner hole wall)
    .revolve()                                  # Revolve 360 degrees
)