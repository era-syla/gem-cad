import cadquery as cq

# --- Parameter Definitions ---
# Overall plate dimensions
plate_length = 100.0
plate_width = 50.0
plate_thickness = 2.0

# Mounting hole parameters
hole_diameter = 4.0
hole_margin = 5.0  # Distance from the short edge to the hole center

# Flexure slot parameters
num_slots = 6         # Number of main slots per side (interleaved)
slot_width = 2.0      # Width of the cut
slot_gap = 4.0        # Material thickness between slots (beam width)
# Determine effective length for slots based on visual appearance
# The slots start from one side and go almost to the other.
slot_length_ratio = 0.75 # Percentage of width the slot cuts through

# --- Calculations ---
# Calculate the total length available for the flexure pattern
# Leaving some solid margin on the ends near the holes
margin_length = 10.0 
flexure_region_length = plate_length - (2 * margin_length)

# Calculate pitch (center-to-center distance along length)
# We have slots coming from left and slots coming from right.
# Pattern: [Slot L] - gap - [Slot R] - gap - [Slot L] ...
# Total items in sequence for N slots per side is roughly 2*N
# Let's space them evenly in the flexure region.
total_cuts = (num_slots * 2) - 1 # Total cuts visible in the middle
pitch = flexure_region_length / (total_cuts + 1)

# --- Geometry Construction ---

# 1. Base Plate
result = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# 2. Mounting Holes
# Four holes, one in each corner area
hole_x_dist = (plate_length / 2) - hole_margin
hole_y_dist = (plate_width / 2) - hole_margin

result = (result
          .faces(">Z")
          .workplane()
          .pushPoints([
              (hole_x_dist, hole_y_dist),
              (hole_x_dist, -hole_y_dist),
              (-hole_x_dist, hole_y_dist),
              (-hole_x_dist, -hole_y_dist)
          ])
          .hole(hole_diameter)
          )

# 3. Flexure Slots
# We need to cut slots alternating from the +Y and -Y sides
# The slots run along the X direction (width of the plate is Y in this setup)?
# Wait, let's re-orient.
# In the image, the long dimension has the slots arranged perpendicular to it.
# Let's assume Length is X, Width is Y.
# The slots are cuts running in the Y direction (along the width).
# One set starts from Y+, goes down. The next starts from Y-, goes up.

slot_cut_length = plate_width * slot_length_ratio

# Create points for slots starting from the "Top" (+Y side)
top_slot_centers = []
# Create points for slots starting from the "Bottom" (-Y side)
bottom_slot_centers = []

start_x = - (flexure_region_length / 2) + pitch

for i in range(num_slots * 2):
    x_pos = start_x + (i * pitch)
    
    # Check bounds to ensure we don't go past the flexure region
    if x_pos > (flexure_region_length / 2):
        break
        
    if i % 2 == 0:
        # Even index: Cut from Top (+Y) going down
        # Center of the slot needs to be offset so the cut starts at the edge
        # Center Y = (Width/2) - (CutLength/2)
        center_y = (plate_width / 2) - (slot_cut_length / 2)
        top_slot_centers.append((x_pos, center_y))
    else:
        # Odd index: Cut from Bottom (-Y) going up
        # Center Y = -(Width/2) + (CutLength/2)
        center_y = -(plate_width / 2) + (slot_cut_length / 2)
        bottom_slot_centers.append((x_pos, center_y))

# Perform the cuts
# Use slot2d to make stadium shaped cuts (rounded ends)

# Top Cuts
if top_slot_centers:
    result = (result
              .faces(">Z")
              .workplane()
              .pushPoints(top_slot_centers)
              .slot2D(slot_cut_length, slot_width, angle=90)
              .cutThruAll()
              )

# Bottom Cuts
if bottom_slot_centers:
    result = (result
              .faces(">Z")
              .workplane()
              .pushPoints(bottom_slot_centers)
              .slot2D(slot_cut_length, slot_width, angle=90)
              .cutThruAll()
              )

# 4. Center Relief Cut (Optional but common in these designs)
# The image shows a single wide flexure with cuts alternating. 
# Sometimes there is a central spine, but this image looks like a standard "serpentine" spring.
# The previous logic generates a serpentine pattern.

# Let's ensure the ends of the slots are open to the sides.
# slot2D creates a closed shape inside the material.
# We need the slots to break the edge.
# To do this, we extend the cut length slightly and shift the center further out.

# Let's re-do the cut logic to ensure edge breaking.

# Reset result to base plate and holes
result = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)
result = (result
          .faces(">Z")
          .workplane()
          .pushPoints([
              (hole_x_dist, hole_y_dist),
              (hole_x_dist, -hole_y_dist),
              (-hole_x_dist, hole_y_dist),
              (-hole_x_dist, -hole_y_dist)
          ])
          .hole(hole_diameter)
          )

# New cut logic for edge-breaking slots
cut_length_extended = slot_cut_length + slot_width # Ensure we cut through the edge
offset_from_center = (plate_width - cut_length_extended) / 2

# Top Edge Cuts (Starting from +Y)
top_cut_points = []
# Bottom Edge Cuts (Starting from -Y)
bottom_cut_points = []

# Recalculate distribution
num_total_slots = 13 # Adjust to match image count approx
step = flexure_region_length / (num_total_slots - 1)
start_x_pos = -flexure_region_length / 2

for i in range(num_total_slots):
    x_pos = start_x_pos + (i * step)
    
    if i % 2 == 0:
        # Cut from Top (+Y)
        # Center Y is shifted up so the slot breaks the top edge
        y_pos = (plate_width / 2) - (cut_length_extended / 2) + (slot_width/2) # nudge out
        top_cut_points.append((x_pos, y_pos))
    else:
        # Cut from Bottom (-Y)
        y_pos = -((plate_width / 2) - (cut_length_extended / 2) + (slot_width/2))
        bottom_cut_points.append((x_pos, y_pos))

# Execute Top Cuts
if top_cut_points:
    result = (result
              .faces(">Z")
              .workplane()
              .pushPoints(top_cut_points)
              .slot2D(cut_length_extended, slot_width, angle=90)
              .cutThruAll()
              )

# Execute Bottom Cuts
if bottom_cut_points:
    result = (result
              .faces(">Z")
              .workplane()
              .pushPoints(bottom_cut_points)
              .slot2D(cut_length_extended, slot_width, angle=90)
              .cutThruAll()
              )