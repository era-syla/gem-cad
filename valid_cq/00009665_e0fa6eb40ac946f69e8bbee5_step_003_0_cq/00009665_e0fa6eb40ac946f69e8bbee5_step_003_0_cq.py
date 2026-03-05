import cadquery as cq

# --- Parameters ---
# Dimensions are estimated based on visual proportions.
# Large Ring
large_ring_od = 60.0    # Outer diameter
large_ring_id = 50.0    # Inner diameter
large_ring_height = 10.0
large_chamfer = 1.0     # Top edge chamfer

# Small Rings
small_ring_od = 30.0
small_ring_id = 22.0
small_ring_height = 8.0
small_chamfer = 1.0

# Positioning
dist_center_large = 0.0
dist_center_small = 45.0 # Distance from center for small rings
angle_offset = 30.0      # To arrange them in a semi-circle pattern

# --- Helper Function for Creating a Single Ring ---
def create_ring(od, id, height, chamfer_size):
    # Calculate radius
    orad = od / 2.0
    irad = id / 2.0
    
    # Create the base cylinder
    ring = cq.Workplane("XY").circle(orad).circle(irad).extrude(height)
    
    # Apply chamfer to the top outer edge
    # Selecting the top face, then the outer edge
    ring = ring.faces(">Z").edges().fillet(chamfer_size)
    
    return ring

# --- Building the Assembly ---

# 1. Create the Large Ring
large_ring = create_ring(large_ring_od, large_ring_id, large_ring_height, large_chamfer)

# 2. Create the Small Rings
# Small Ring 1 (Left)
small_ring_1 = create_ring(small_ring_od, small_ring_id, small_ring_height, small_chamfer)
small_ring_1 = small_ring_1.translate((-dist_center_small, -15, 0))

# Small Ring 2 (Center-ish/Bottom)
small_ring_2 = create_ring(small_ring_od, small_ring_id, small_ring_height, small_chamfer)
small_ring_2 = small_ring_2.translate((0, -dist_center_small, 0))

# Small Ring 3 (Right)
small_ring_3 = create_ring(small_ring_od, small_ring_id, small_ring_height, small_chamfer)
small_ring_3 = small_ring_3.translate((dist_center_small, -15, 0))


# Combine all parts into a single compound object
result = large_ring.union(small_ring_1).union(small_ring_2).union(small_ring_3)

# If running in an environment that supports show_object, this would visualize it
# show_object(result)