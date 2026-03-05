import cadquery as cq
import math

# --- Parameters ---
outer_radius = 100.0       # Radius of the outer rim
inner_hub_radius = 15.0    # Radius of the central hub
rim_thickness = 5.0        # Thickness of the outer rim ring (radial width)
height = 8.0               # Height of the entire part
num_spokes = 10            # Number of spokes
spoke_width_hub = 3.0      # Width of the spoke near the hub
spoke_width_rim = 8.0      # Width of the spoke near the rim (tapered)

# Mounting hole lugs on the rim
lug_radius = 4.0           # Radius of the small circular lugs on the rim
lug_hole_radius = 2.0      # Radius of the holes inside the lugs

# --- Geometry Construction ---

# 1. Create the central hub
# Simple cylinder centered at origin
hub = cq.Workplane("XY").circle(inner_hub_radius).extrude(height)

# 2. Create the outer rim
# A pipe created by subtracting an inner circle from an outer circle
rim = (cq.Workplane("XY")
       .circle(outer_radius)
       .circle(outer_radius - rim_thickness)
       .extrude(height))

# 3. Create the spokes
# We will create one spoke and pattern it.
# The spoke is a tapered shape (trapezoid) extruded.
# To make it parametric and centered, we can loft or simply draw a polygon.
# Let's draw a polygon on the XY plane.

# Calculate coordinates for half the spoke to mirror or draw fully
# We draw it along the Y-axis for easy rotation later
spoke_half_w_hub = spoke_width_hub / 2.0
spoke_half_w_rim = spoke_width_rim / 2.0

# Points for a single spoke polygon (trapezoid)
# Starting near the center, ending at the outer radius
p1 = (-spoke_half_w_hub, inner_hub_radius - 1.0) # slightly inside hub to ensure overlap
p2 = (spoke_half_w_hub, inner_hub_radius - 1.0)
p3 = (spoke_half_w_rim, outer_radius - rim_thickness + 1.0) # slightly inside rim
p4 = (-spoke_half_w_rim, outer_radius - rim_thickness + 1.0)

single_spoke = (cq.Workplane("XY")
                .polyline([p1, p2, p3, p4])
                .close()
                .extrude(height))

# Create the full set of spokes by rotating the single spoke
spokes = single_spoke
for i in range(1, num_spokes):
    angle = i * (360.0 / num_spokes)
    spokes = spokes.union(single_spoke.rotate((0, 0, 0), (0, 0, 1), angle))

# 4. Create the mounting lugs on the rim
# These are small cylinders located at the end of each spoke, embedded in the rim
lug_center_radius = outer_radius + lug_radius - 2.0 # Position slightly sticking out
# Actually, looking at the image, the lugs seem centered *on* the rim or slightly outside.
# Let's place them centered on the rim radius.
lug_dist = outer_radius

# Define one lug
one_lug = (cq.Workplane("XY")
           .center(0, lug_dist) # Move to the rim location
           .circle(lug_radius)
           .extrude(height))

# Define the hole inside the lug
one_lug_hole = (cq.Workplane("XY")
                .center(0, lug_dist)
                .circle(lug_hole_radius)
                .extrude(height))

# Subtract hole from lug
one_lug_solid = one_lug.cut(one_lug_hole)

# Pattern the lugs
lugs = one_lug_solid
for i in range(1, num_spokes):
    angle = i * (360.0 / num_spokes)
    lugs = lugs.union(one_lug_solid.rotate((0, 0, 0), (0, 0, 1), angle))

# --- Combine Everything ---

result = hub.union(rim).union(spokes).union(lugs)

# Optional: Fillet edges for a cleaner look (similar to the smooth render)
# Finding vertical edges can be tricky, so we apply a small fillet to everything feasible
# result = result.edges("|Z").fillet(0.5) 

# Export or display
# show_object(result)