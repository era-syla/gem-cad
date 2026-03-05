import cadquery as cq

# --- Parameters ---
thickness = 5.0          # Thickness of the plate
outer_diameter = 100.0   # Diameter of the outer rim
inner_diameter = 50.0    # Diameter of the central hole
rim_width = 6.0          # Width of the material for the inner and outer rings
bolt_hole_diameter = 8.0 # Diameter of the 4 small mounting holes
num_holes = 4            # Number of spokes/holes

# --- Derived Dimensions ---
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0

# Define the boundaries of the rings
outer_ring_inner_rad = outer_radius - rim_width
inner_ring_outer_rad = inner_radius + rim_width

# Calculate boss size and position to bridge the gap between rings perfectly
# The gap is the space between the inner ring and outer ring
gap_width = outer_ring_inner_rad - inner_ring_outer_rad
boss_radius = gap_width / 2.0
bolt_circle_radius = inner_ring_outer_rad + boss_radius

# --- Modeling ---

# 1. Create the Outer Ring
# Draw two concentric circles and extrude the area between them
outer_ring = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(outer_ring_inner_rad)
    .extrude(thickness)
)

# 2. Create the Inner Ring
inner_ring = (
    cq.Workplane("XY")
    .circle(inner_ring_outer_rad)
    .circle(inner_radius)
    .extrude(thickness)
)

# 3. Create the Bosses (Spokes)
# Create cylinders arranged in a polar pattern to connect the rings
bosses = (
    cq.Workplane("XY")
    .polarArray(bolt_circle_radius, 0, 360, num_holes)
    .circle(boss_radius)
    .extrude(thickness)
)

# 4. Combine the solid bodies
base_plate = outer_ring.union(inner_ring).union(bosses)

# 5. Cut the bolt holes
# Select the top face, create a new workplane, and cut the holes
result = (
    base_plate.faces(">Z")
    .workplane()
    .polarArray(bolt_circle_radius, 0, 360, num_holes)
    .circle(bolt_hole_diameter / 2.0)
    .cutThruAll()
)