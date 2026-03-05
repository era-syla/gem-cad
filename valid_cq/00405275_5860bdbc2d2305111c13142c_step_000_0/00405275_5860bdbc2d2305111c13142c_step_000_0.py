import cadquery as cq

# Parametric dimensions based on visual estimation
inner_radius = 15.0
root_radius = 19.0
outer_radius = 24.0
thickness = 5.0
num_teeth = 22
tooth_width_root = 3.8  # Width of the tooth at the root radius
tooth_width_tip = 2.2   # Width of the tooth at the outer radius

# 1. Create the base ring
# This creates a hollow cylinder from the inner radius to the root radius
base_ring = cq.Workplane("XY").circle(root_radius).circle(inner_radius).extrude(thickness)

# 2. Define the geometry for a single tooth
# The tooth is a trapezoid in the 2D plane, extruded to the thickness.
# We calculate the points to create a tapered "wedge" shape.
# To ensure a solid union with the base ring, we extend the tooth profile 
# slightly inwards past the root radius (overlap).

overlap = 1.0
start_radius = root_radius - overlap

# Calculate half-widths for the trapezoid profile
# We calculate the width at the start_radius by linearly projecting the taper
slope = ((tooth_width_tip - tooth_width_root) / 2.0) / (outer_radius - root_radius)
start_half_width = (tooth_width_root / 2.0) + slope * (start_radius - root_radius)
tip_half_width = tooth_width_tip / 2.0

# Define the points of the tooth polygon centered on the X-axis
tooth_profile = [
    (start_radius, -start_half_width),
    (outer_radius, -tip_half_width),
    (outer_radius, tip_half_width),
    (start_radius, start_half_width)
]

# Create the solid for a single tooth
tooth = (cq.Workplane("XY")
         .polyline(tooth_profile)
         .close()
         .extrude(thickness))

# 3. Create the pattern of teeth
# We use polarArray with a radius of 0. This applies pure rotation to our
# already-positioned tooth object relative to the center (0,0).
teeth_pattern = (cq.Workplane("XY")
                 .polarArray(0, 0, 360, num_teeth)
                 .eachpoint(lambda loc: tooth.val().located(loc)))

# 4. Combine the base ring and the teeth into the final result
result = base_ring.union(teeth_pattern)