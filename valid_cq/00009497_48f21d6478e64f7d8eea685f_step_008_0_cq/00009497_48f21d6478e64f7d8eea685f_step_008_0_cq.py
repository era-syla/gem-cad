import cadquery as cq
import math

# --- Parameters ---
ring_inner_diameter = 40.0
ring_outer_diameter = 56.0
ring_thickness = 8.0

# Lugs parameters
num_lugs = 4
lug_width = 12.0  # Tangential width
lug_protrusion = 6.0  # How far it sticks out from the outer ring
lug_chamfer = 2.0  # Chamfer size on the outer corners of the lugs
lug_hole_diameter = 2.5
lug_hole_depth = 5.0 # Depth of the side hole

# Derived parameters
ring_inner_radius = ring_inner_diameter / 2.0
ring_outer_radius = ring_outer_diameter / 2.0
lug_total_radius = ring_outer_radius + lug_protrusion

# --- Geometry Construction ---

# 1. Base Ring
base_ring = (
    cq.Workplane("XY")
    .circle(ring_outer_radius)
    .circle(ring_inner_radius)
    .extrude(ring_thickness)
)

# 2. Lugs
# We will create one lug and pattern it.

# Calculate the angle subtended by the lug width for positioning logic if needed,
# but constructing a box and positioning it is easier.
lug_box_length = lug_protrusion + (ring_outer_radius - ring_inner_radius) # Ensure it merges well
lug_center_radius = ring_outer_radius + lug_protrusion/2.0

def create_lug(loc):
    # Create the basic block for the lug
    # We position a box such that it protrudes correctly
    
    # Box dimensions: 
    # Length (radial direction) needs to overlap with the ring to fuse properly
    # Width (tangential direction) = lug_width
    # Height = ring_thickness
    
    lug = (
        cq.Workplane("XY")
        .box(lug_protrusion * 2 + 5, lug_width, ring_thickness) # Extra length for overlap
        .translate((ring_outer_radius + lug_protrusion/2.0 - 2.5, 0, ring_thickness/2.0))
    )
    
    # Apply chamfers to the outer vertical edges and outer top/bottom edges
    # The outer face is at x = ring_outer_radius + lug_protrusion
    
    # We need to select edges carefully.
    # Let's filter edges on the outermost face (+X relative to the lug center local coords)
    
    # The box is centered. Let's find the max X face.
    lug = lug.faces(">X").edges().chamfer(lug_chamfer)
    
    # Create the hole
    # The hole is on the outer face pointing inwards (radially)
    lug = (
        lug.faces(">X")
        .workplane()
        .hole(lug_hole_diameter, lug_hole_depth)
    )
    
    return lug.val().located(loc)

# Create locations for the 4 lugs
lug_locations = (
    cq.Workplane("XY")
    .polarArray(ring_outer_radius, 0, 360, num_lugs)
    .vals()
)

# Generate lugs at locations (handling rotation manually is often safer for custom orientation)
# polarArray gives locations, but we need to rotate the lug geometry itself.
lugs = cq.Assembly()
for i in range(num_lugs):
    angle = i * (360.0 / num_lugs)
    
    # Create a single lug
    # Note: The create_lug function builds it along X axis.
    # We need to rotate it around Z.
    lug_solid = (
        cq.Workplane("XY")
        .box(lug_protrusion + 5, lug_width, ring_thickness) # Overlap 5mm
        .translate(((lug_protrusion + 5)/2.0 + ring_outer_radius - 5, 0, ring_thickness/2.0))
    )
    
    # Chamfer outer edges
    # Select edges on the face furthest from center (>X)
    lug_solid = lug_solid.faces(">X").edges().chamfer(lug_chamfer)
    
    # Add hole
    lug_solid = lug_solid.faces(">X").workplane().hole(lug_hole_diameter, lug_hole_depth)
    
    # Rotate into position
    lug_solid = lug_solid.rotate((0,0,0), (0,0,1), angle)
    
    base_ring = base_ring.union(lug_solid)

# 3. Final Result
result = base_ring