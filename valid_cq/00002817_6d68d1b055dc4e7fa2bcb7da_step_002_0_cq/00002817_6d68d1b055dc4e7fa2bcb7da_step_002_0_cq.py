import cadquery as cq

# --- Parameter Definitions ---

# General settings
plate_thickness = 5.0
fillet_radius = 2.0

# Smaller Plate (Left) Parameters
small_plate_length = 60.0
small_plate_width = 35.0

# Larger Plate (Right) Parameters
large_plate_length = 80.0
large_plate_width = 80.0
separation_distance = 60.0  # Distance to move the large plate

# Hole Parameters
# Countersunk hole style
counterbore_dia = 8.0
counterbore_depth = 2.0
through_hole_dia = 4.0

# Small through holes (plain)
small_hole_dia = 3.0

# --- Helper Function for Counterbored Holes ---
def create_cbore_hole(workplane, x, y):
    return (workplane
            .pushPoints([(x, y)])
            .cboreHole(through_hole_dia, counterbore_dia, counterbore_depth))

def create_simple_hole(workplane, x, y):
    return (workplane
            .pushPoints([(x, y)])
            .hole(small_hole_dia))

# --- Build Small Plate (Left) ---

# Base shape
small_plate = (cq.Workplane("XY")
               .box(small_plate_length, small_plate_width, plate_thickness)
               .edges("|Z").fillet(fillet_radius))

# Pattern for small plate holes
# It has a distinctive grid pattern. 
# Looks like 3 rows roughly.
# Outer large holes: 4 corners + 2 middle of long edges? No, looks like 2 rows of 3 large holes + 2 small central holes.
# Actually, looking closer at the left plate:
# It has 6 counterbored holes arranged in 2 rows of 3.
# Between the counterbored holes, there are smaller simple holes.

# Coordinates estimation for small plate (centered at 0,0)
sp_cx = 20.0 # X spacing from center for outer columns
sp_cy = 10.0 # Y spacing from center

# Add Counterbored holes (6 total)
pts_large_holes_sp = [
    (-sp_cx, sp_cy), (0, sp_cy), (sp_cx, sp_cy),
    (-sp_cx, -sp_cy), (0, -sp_cy), (sp_cx, -sp_cy)
]

for pt in pts_large_holes_sp:
    small_plate = create_cbore_hole(small_plate, pt[0], pt[1])

# Add small holes (4 total)
# They seem to be interleaved or centered relative to others.
# Two on the centerline X, two on centerline Y?
# Based on image: 2 small holes on Y=0 axis, between the columns of large holes.
# And 2 small holes on X=0 axis? No, maybe just 4 small holes in a diamond or cross pattern.
# Let's assume two small holes on Y=0 between the columns.
pts_small_holes_sp = [
    (-10.0, 0), (10.0, 0), (0, 0) # Looking very closely, there is a center hole and two side holes
]
# Wait, let's look at the specific pattern on the left plate again.
# Top row: Large, small, Large
# Bottom row: Large, small, Large
# Middle row: Large (left), small (center), Large (right) - Wait, no.
# Let's go with a standard mounting plate pattern.
# 2 rows of 3 large holes.
# In between the 4 outer large holes, there are 2 small holes.
small_plate = (small_plate
               .pushPoints([(-10, 0), (10, 0), (0,0)]) # Centerline holes
               .hole(small_hole_dia))


# --- Build Large Plate (Right) ---

# Base shape
large_plate = (cq.Workplane("XY")
               .box(large_plate_width, large_plate_length, plate_thickness)
               .edges("|Z").fillet(fillet_radius))

# The large plate has slotted holes in the corners and a grid of small holes.
slot_length = 12.0 # Total length including radius
slot_w = 6.0
corner_offset = 28.0

# Create Slotted Corner Holes
# We will cut these.
def cut_slot(wp, x, y, angle):
    # Create a slot profile
    slot = (cq.Workplane("XY")
            .center(x, y)
            .transformed(rotate=(0,0,angle))
            .slot2D(slot_length, slot_w)
            .extrude(plate_thickness, both=True)) # Cut through
    
    # Simple cut
    return wp.cut(slot)

# Add slots (angled towards center or parallel? Image shows parallel to edges usually, but these look like corner slots)
# Looking at the image, the slots are at the 4 corners.
# Top Right: Horizontal slot? No, looks like an oval counterbore.
# Let's approximate them as double-hole slots or just slots. They look like counterbored slots.
# To make a counterbored slot is complex. Let's make them simple slots with a larger recess on top.

# Slot positions
lp_slot_dx = 25.0
lp_slot_dy = 25.0

# Let's approximate the corner features as pairs of counterbored holes merged, 
# or just slots. Given the resolution, they look like oval pockets.
# Let's just create slots for simplicity.
large_plate = (large_plate
               .pushPoints([(lp_slot_dx, lp_slot_dy), (lp_slot_dx, -lp_slot_dy), 
                            (-lp_slot_dx, lp_slot_dy), (-lp_slot_dx, -lp_slot_dy)])
               .slot2D(15, through_hole_dia*2) # Outer recess
               .cutBlind(counterbore_depth)
               .pushPoints([(lp_slot_dx, lp_slot_dy), (lp_slot_dx, -lp_slot_dy), 
                            (-lp_slot_dx, lp_slot_dy), (-lp_slot_dx, -lp_slot_dy)])
               .slot2D(15, through_hole_dia)   # Through hole
               .cutThruAll())

# Inner grid of holes
# Looks like a 5x5 grid or similar, missing corners, or specific mounting pattern.
# It looks like a standard V-slot gantry plate or similar.
# Central cluster: 4 holes in square, 1 in center.
inner_square = 20.0
large_plate = (large_plate
               .pushPoints([(inner_square/2, inner_square/2), (inner_square/2, -inner_square/2),
                            (-inner_square/2, inner_square/2), (-inner_square/2, -inner_square/2),
                            (0,0)])
               .hole(small_hole_dia))

# Outer ring of small holes
outer_ring = 40.0
large_plate = (large_plate
               .pushPoints([(outer_ring/2, 0), (-outer_ring/2, 0),
                            (0, outer_ring/2), (0, -outer_ring/2)])
               .hole(small_hole_dia))


# --- Assembly ---

# Move the large plate to the right
large_plate_moved = large_plate.translate((separation_distance + large_plate_width/2 + small_plate_length/2, 0, 0))

# Combine
result = small_plate.union(large_plate_moved)