import cadquery as cq
import math

# Parameters for the Bolt (based on approx M12 proportions)
shaft_diameter = 12.0
shaft_length = 50.0
head_height = 8.0
head_waf = 19.0  # Width Across Flats
chamfer_tip = 1.0
fillet_neck = 0.8

# Calculate derived dimension: Width Across Corners (WAC)
# For a hexagon, WAC = WAF * 2 / sqrt(3)
head_wac = head_waf * 2 / math.sqrt(3)

# Calculate chamfer size for the head
# We want to chamfer the corners such that the top face becomes a circle tangent to the flats
# Radial distance to remove = (Radius Corners - Radius Flats)
head_chamfer_dist = (head_wac - head_waf) / 2.0

# 1. Create the Hex Head Geometry
# Step A: Create a cylinder representing the outer bounds (across corners)
# and apply a chamfer to the top edge to simulate the standard conical bolt head cut.
head_cylinder = (
    cq.Workplane("XY")
    .circle(head_wac / 2.0)
    .extrude(head_height)
    .faces(">Z")
    .edges()
    .chamfer(head_chamfer_dist)
)

# Step B: Create a Hexagonal Prism
hex_prism = (
    cq.Workplane("XY")
    .polygon(6, head_wac)
    .extrude(head_height)
)

# Step C: Intersect the Chamfered Cylinder with the Hex Prism
# This leaves the hexagonal shape with the corners 'turned' off
head = head_cylinder.intersect(hex_prism)

# 2. Create the Shaft
# Extrude from the bottom of the head (Z=0 plane) downwards
shaft = (
    cq.Workplane("XY")
    .circle(shaft_diameter / 2.0)
    .extrude(-shaft_length)
)

# 3. Combine Head and Shaft
bolt = head.union(shaft)

# 4. Apply Final Details
# Chamfer the tip of the shaft
bolt = bolt.faces("<Z").edges().chamfer(chamfer_tip)

# Fillet the neck (intersection of head and shaft)
# We select the edge closest to the origin (0,0,0) which is the neck circle
bolt = bolt.edges(cq.selectors.NearestToPointSelector((0, 0, 0))).fillet(fillet_neck)

# Final result
result = bolt