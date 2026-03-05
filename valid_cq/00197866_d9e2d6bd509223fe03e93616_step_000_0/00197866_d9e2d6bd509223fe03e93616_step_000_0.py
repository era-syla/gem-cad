import cadquery as cq

# --- Parameters ---
# Central body dimensions
length = 40.0       
width = 25.0        
thickness = 3.0     

# Wall dimensions
wall_height = 10.0  # Total height from bottom of base

# Leg dimensions
leg_dx = 5.0        # Horizontal extension of the diagonal section
leg_dy = 5.0        # Vertical extension of the diagonal section
leg_straight = 8.0  # Length of the straight section
leg_width = 3.0     # Width of the leg (approximated as material thickness)

# Slot dimensions
slot_w = 8.0
slot_h = 3.5

# --- Modeling ---

# 1. Base Plate
# Create the central flat plate
base = cq.Workplane("XY").box(length, width, thickness)

# 2. Legs
# We define one leg in the +X, +Y quadrant and mirror it.
# The leg extends from the corner of the wall/base.
pts = [
    (length/2, width/2),                                     # Outer start point (corner)
    (length/2 + leg_dx, width/2 + leg_dy),                   # Outer diagonal end
    (length/2 + leg_dx + leg_straight, width/2 + leg_dy),    # Outer straight end
    (length/2 + leg_dx + leg_straight, width/2 + leg_dy - leg_width), # Inner straight end
    (length/2 + leg_dx, width/2 + leg_dy - leg_width),       # Inner diagonal end
    (length/2, width/2 - leg_width)                          # Inner start point
]

# Create the leg solid
leg = cq.Workplane("XY").polyline(pts).close().extrude(thickness)

# Mirror legs to all 4 corners
right_legs = leg.union(leg.mirror("XZ"))
all_legs = right_legs.union(right_legs.mirror("YZ"))

# Union base and legs
body = base.union(all_legs)

# 3. Side Walls
# Sketch rectangles on top of the base for the walls
wall_offset = width/2 - thickness/2
wall_extrude_height = wall_height - thickness

walls = (cq.Workplane("XY")
         .workplane(offset=thickness)
         .center(0, wall_offset)
         .rect(length, thickness)
         .center(0, -2 * wall_offset)
         .rect(length, thickness)
         .extrude(wall_extrude_height))

body = body.union(walls)

# 4. Slots
# Cut slots through the side walls. 
# Selecting the >Y face automatically centers the workplane on that face.
result = (body.faces(">Y").workplane()
          .rect(slot_w, slot_h)
          .cutThruAll())