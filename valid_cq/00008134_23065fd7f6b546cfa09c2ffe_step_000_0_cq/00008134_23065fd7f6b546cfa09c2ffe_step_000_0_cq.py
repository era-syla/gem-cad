import cadquery as cq

# --- Parameter Definitions ---
sphere_radius = 50.0  # Main body radius
split_plane_offset = 0.0 # Vertical offset for the horizontal split (0 = center)
pin_radius = 1.5      # Radius of the small cylindrical pin/stem
pin_height = 10.0     # Height of the pin protruding from the top
seam_gap = 0.5        # Visual indication of a seam (optional, but likely present in a real mold)

# --- Geometry Construction ---

# 1. Create the main sphere
sphere = cq.Workplane("XY").sphere(sphere_radius)

# 2. Create the horizontal split line feature
# The image shows a horizontal seam. Often this implies two hemispheres, 
# or a groove. Here we create a simple equatorial cut or just represent the sphere.
# Looking closely at the image, there is a horizontal line around the "equator"
# and a vertical line going up to the pin. This suggests a multi-part assembly 
# or a molded part with parting lines. 

# Let's create the geometry as a single solid sphere first, then add the pin.
# The lines in the image are likely edge lines from the CAD visualization, 
# representing the seam of the revolution or a parting line.
# To replicate the geometry itself:

# Base Sphere
main_body = cq.Workplane("XY").sphere(sphere_radius)

# 3. Create the pin/stem on top
# It's a small cylinder located at the top pole (Z axis)
pin = (
    cq.Workplane("XY")
    .workplane(offset=sphere_radius) # Move plane to top of sphere
    .circle(pin_radius)
    .extrude(pin_height)
)

# 4. Combine parts
# We union the pin to the sphere.
result = main_body.union(pin)

# Optional: If the request implies modeling the "seam" physically 
# (e.g. a small groove), we could cut it. However, standard CAD representation 
# usually just shows the edges of faces. The image looks like a standard sphere 
# primitive with a cylinder added, where the lines are just rendering artifacts 
# of the surface parameterization (u/v lines) or a parting line.
# The simplest robust interpretation is a Union.

# Final Result
result = result