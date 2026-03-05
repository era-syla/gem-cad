import cadquery as cq

# Model Parameters
rod_length = 150.0      # Length of each rod
rod_diameter = 2.5      # Diameter of the rods
pair_spacing = 5.0      # Spacing between rods within a pair (center-to-center)
group_spacing = 60.0    # Spacing between the top and bottom pairs
stagger_offset = 25.0   # Longitudinal shift for the staggered pair

# Calculate radius
radius = rod_diameter / 2.0

# Bottom Pair: Aligned rods
# First rod of the bottom pair
bottom_rod_1 = (
    cq.Workplane("YZ")
    .center(-group_spacing / 2, 0)
    .circle(radius)
    .extrude(rod_length)
)

# Second rod of the bottom pair
bottom_rod_2 = (
    cq.Workplane("YZ")
    .center(-group_spacing / 2 - pair_spacing, 0)
    .circle(radius)
    .extrude(rod_length)
)

# Top Pair: Staggered rods
# Inner rod of the top pair (aligned with X=0)
top_rod_inner = (
    cq.Workplane("YZ")
    .center(group_spacing / 2, 0)
    .circle(radius)
    .extrude(rod_length)
)

# Outer rod of the top pair (shifted along X axis)
top_rod_outer = (
    cq.Workplane("YZ")
    .workplane(offset=stagger_offset)
    .center(group_spacing / 2 + pair_spacing, 0)
    .circle(radius)
    .extrude(rod_length)
)

# Combine all solids into the final result
result = bottom_rod_1.union(bottom_rod_2).union(top_rod_inner).union(top_rod_outer)