import cadquery as cq
import math

# Model Parameters
wire_diameter = 2.0         # Diameter of the wire cross-section
spring_outer_diameter = 12.0 # Total outer diameter of the spring
pitch = 3.2                 # Vertical rise per revolution (approx wire_dia + gap)
number_of_turns = 13        # Total number of coils

# Derived Dimensions
mean_radius = (spring_outer_diameter - wire_diameter) / 2.0
height = pitch * number_of_turns
wire_radius = wire_diameter / 2.0

# 1. Generate the Helical Path
# makeHelix creates a wire spiral along the Z-axis
path_wire = cq.Wire.makeHelix(pitch=pitch, height=height, radius=mean_radius)

# 2. Define the Profile Plane
# We need to construct a plane perpendicular to the start of the helix.
# The standard makeHelix starts at (radius, 0, 0).
# The tangent vector at the start (t=0) is (0, r, pitch/2pi).
c_val = pitch / (2 * math.pi)
start_point = cq.Vector(mean_radius, 0, 0)
tangent_vector = cq.Vector(0, mean_radius, c_val)

# Create a plane defined by the start point and the tangent normal
profile_plane = cq.Plane(origin=start_point, normal=tangent_vector)

# 3. Create the Solid Spring
# Draw the circular wire profile and sweep it along the helical path
result = (
    cq.Workplane(profile_plane)
    .circle(wire_radius)
    .sweep(cq.Workplane(obj=path_wire), isFrenet=True)
)