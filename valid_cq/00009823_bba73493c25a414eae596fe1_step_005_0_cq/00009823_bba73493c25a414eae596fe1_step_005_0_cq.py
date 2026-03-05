import cadquery as cq

# Define dimensions
thickness = 2.0
overall_width = 100.0
overall_height = 80.0

# Define the outer polygon points
# The shape looks like a hexagon that has been flattened or stretched.
# Let's approximate the vertices based on visual inspection relative to a center.
# The shape is roughly symmetric around a vertical axis, but the cutouts are asymmetric.
# Let's assume the outer boundary is a distorted hexagon.

p1 = (0, 40)        # Top point
p2 = (50, 20)       # Top right
p3 = (60, -20)      # Bottom right side
p4 = (25, -45)      # Bottom right corner (approx)
p5 = (-25, -40)     # Bottom left corner
p6 = (-60, 10)      # Top left side

# Create the main base plate
base_pts = [p1, p2, p3, p4, p5, p6]
base_plate = cq.Workplane("XY").polyline(base_pts).close().extrude(thickness)

# Now define the cutouts.
# Looking at the image, there are three distinct cutout shapes radiating from the bottom center area.
# They look like stylized "claw marks" or angled slots.

# Cutout 1: The leftmost angled slot
c1_p1 = (-10, -10) # Inner top
c1_p2 = (-25, -35) # Outer bottom left
c1_p3 = (-15, -38) # Outer bottom right
c1_p4 = (0, -15)   # Inner bottom
# This will be a polygon to cut

# Cutout 2: The middle angled slot
c2_p1 = (10, -10)  # Inner top
c2_p2 = (5, -18)   # Inner bottom
c2_p3 = (25, -40)  # Outer bottom left
c2_p4 = (35, -32)  # Outer bottom right

# Cutout 3: The rightmost shape (triangular/trapezoidal)
c3_p1 = (15, -25)
c3_p2 = (25, -45)
c3_p3 = (45, -35)
c3_p4 = (35, -20)

# The image shows "lands" (solid parts) separated by "gaps" (cutouts).
# It's actually easier to model this by drawing the solid regions if the geometry is complex,
# or by subtracting slots if the base is simple.
# Let's re-evaluate the image structure. It looks like a single solid piece with narrow slots cut into it.
# The slots separate the bottom right quadrant into 3 fingers/islands.

# Let's define the slots (the negative space) instead.
# Slot A: Leftmost gap
slot_a_pts = [
    (-5, -5),    # Top pivot area
    (-20, -35),  # Bottom left
    (-10, -38),  # Bottom right (making the slot width)
    (5, -10)     # Back to pivot
]
# Wait, looking closer at the image, the gaps are constant width.
# It's easier to sketch the outline of the "fingers".

# Alternative approach: Sketch the entire profile as a single face with wires.
# The shape consists of a large main body and two smaller "island" pieces, OR
# it is a single piece where the slots don't go all the way through to the edge?
# Looking at the bottom edge, the slots go all the way through, breaking the perimeter.
# This means the object is actually composed of disjoint parts?
# No, looking at the center, the slots stop before the center. They are like fingers.
# So it is one single solid object.

# Let's define the points for the "slots" to be subtracted.
# Slot 1 (Left): Separates the main left body from the middle finger.
slot1_pts = [
    (-8, -5),    # Inner tip
    (-22, -42),  # Bottom left 
    (-15, -44),  # Bottom right
    (0, -10)     # Inner bottom
]

# Slot 2 (Right): Separates the middle finger from the rightmost triangular island.
slot2_pts = [
    (12, -8),    # Inner tip
    (20, -48),   # Bottom left
    (40, -38),   # Bottom right
    (28, -12)    # Inner top
]

# This is getting tricky to guess coordinates. Let's try a constructive geometry approach.
# 1. Create the main hexagonal-ish shape.
# 2. Cut slots into it.

# Refined Base Shape Points (Counter-Clockwise)
base_points = [
    (0, 40),      # Top
    (-50, 15),    # Top Left
    (-30, -35),   # Bottom Left
    (0, -40),     # Bottom Center (approx)
    (30, -45),    # Bottom Right 1
    (55, -20),    # Bottom Right 2
    (50, 20)      # Top Right
]

# Let's build the specific "fingers" geometry shown in the bottom half.
# It looks like a logo.
# Let's define the cutting tools (the negative space).

# Slot 1: Angled slot on the left-bottom
s1_p1 = (-5, -5)
s1_p2 = (-20, -40)
s1_p3 = (-14, -42)
s1_p4 = (1, -7)

# Slot 2: Angled slot on the right-bottom
s2_p1 = (10, -5)
s2_p2 = (22, -50) # Goes past the edge to ensure cut
s2_p3 = (32, -45) # Goes past the edge
s2_p4 = (18, -7)

# Slot 3: Maybe a third smaller slot or just the shape of the perimeter?
# The image shows 3 distinct "prongs" or sections at the bottom.
# Left section (main body), Middle finger, Right island.

# Let's try to trace the "gap" directly.
# Gap 1 (Left): 
gap1_sketch = cq.Workplane("XY").polyline([
    (-4, -5), (-18, -45), (-12, -45), (2, -5)
]).close()

# Gap 2 (Right):
gap2_sketch = cq.Workplane("XY").polyline([
    (8, -5), (20, -55), (35, -45), (15, -5)
]).close()


# Let's try a different strategy: Construct the shape by defining the final perimeter directly.
# This avoids boolean operations which might be tricky with estimated coordinates.
# The shape is a single polygon if we trace the perimeter, assuming the slots don't meet.
# Looking at the image, the slots end blindly in the center. So it is a single closed wire.

# Coordinates estimation for a single continuous wire:
pts = []
# Start Top
pts.append((0, 35))
# Top Left side
pts.append((-45, 10))
# Bottom Left corner
pts.append((-25, -30))
# -- Start of Left Slot --
# Go up into the slot
pts.append((-10, 0)) 
# Go down the other side of the left finger
pts.append((-15, -32)) 
# Bottom of middle finger
pts.append((-5, -35)) 
# -- Start of Right Slot --
# Go up into the slot
pts.append((5, 0)) 
# Go down the other side of the right finger
pts.append((25, -25))
# Bottom of right finger/island
pts.append((35, -20))
# Right side
pts.append((45, 15))
# Close back to top
pts.append((0, 35))

# The generated shape above is a bit too simple, let's refine the specific stylized "claw" look.
# The image has a very specific geometric feel.

# Let's use boolean subtraction which is more robust for "carving" out the slots.

# 1. The Base Hull
hull_pts = [
    (0, 40),       # Top
    (55, 15),      # Top Right
    (60, -10),     # Mid Right
    (30, -35),     # Bottom Right
    (-10, -35),    # Bottom Center-ish
    (-30, -30),    # Bottom Left
    (-50, 15)      # Top Left
]
base = cq.Workplane("XY").polyline(hull_pts).close().extrude(thickness)

# 2. The Cuts
# Cut 1: The left angled gap
cut1_pts = [
    (-5, -2),     # Top Inner
    (-15, -40),   # Bottom Left
    (-8, -42),    # Bottom Right
    (2, -4)       # Top Outer
]
cut1 = cq.Workplane("XY").polyline(cut1_pts).close().extrude(thickness * 2).translate((0,0,-thickness/2))

# Cut 2: The right angled gap
cut2_pts = [
    (10, -2),     # Top Inner
    (15, -40),    # Bottom Left
    (40, -25),    # Bottom Right
    (20, -4)      # Top Outer
]
cut2 = cq.Workplane("XY").polyline(cut2_pts).close().extrude(thickness * 2).translate((0,0,-thickness/2))

# Let's combine this into a single fluent script with carefully tuned coordinates to match the image.
# The image shows a specific logo, likely from a game or faction symbol.
# It resembles a simplified skull or a claw mark.

final_pts = [
    # Start at top center
    (0.0, 35.0),
    # Top Left
    (-40.0, 15.0),
    # Bottom Left Corner
    (-25.0, -30.0),
    # Slot 1 (Left) - Inner
    (-12.0, -28.0), # Bottom of the "thumb"
    (-5.0, -5.0),   # Junction
    
    # Middle Finger
    (-2.0, -28.0),  # Left side of middle finger
    (8.0, -28.0),   # Right side of middle finger
    
    # Slot 2 (Right) - Inner
    (5.0, -5.0),    # Junction
    (18.0, -20.0),  # Top side of the gap
    
    # Right Island/Wing
    (30.0, -25.0),  # Bottom tip of right wing
    (45.0, 5.0),    # Top Right corner
]
# The single wire approach is hard because of the disjointed look at the bottom.
# Reverting to Base Shape - Cuts approach as it guarantees validity.

# Final Geometry Strategy:
# 1. Create a large pentagon/hexagon base.
# 2. Create two polygonal cutters.
# 3. Cut.

result = (
    cq.Workplane("XY")
    .polyline([
        (0, 40),      # Top Peak
        (45, 20),     # Top Right
        (55, -15),    # Bottom Right Side
        (35, -35),    # Bottom Right Corner
        (-15, -35),   # Bottom Left Corner
        (-45, -15),   # Bottom Left Side
        (-45, 15)     # Top Left
    ])
    .close()
    .extrude(thickness)
)

# Left Slot Cutter
cutter1 = (
    cq.Workplane("XY")
    .polyline([
        (-2, 0),      # Top Pivot
        (-12, -40),   # Bottom Left
        (-4, -40),    # Bottom Right
        (4, 0)        # Top Right pivot area
    ])
    .close()
    .extrude(10)
    .translate((-12, -5, -5)) # Position it
)

# Right Slot Cutter
cutter2 = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),       # Top Pivot
        (10, -40),    # Bottom Left
        (35, -25),    # Bottom Right
        (10, 5)       # Top Right
    ])
    .close()
    .extrude(10)
    .translate((12, -8, -5)) # Position it
)

# Apply cuts
# result = result.cut(cutter1).cut(cutter2)

# The generated code below uses precise coordinates to replicate the visual proportions
# of the provided image (a stylized plate with 3 prongs/sections).

result = cq.Workplane("XY").polyline([
    (0, 50),          # Top point
    (-50, 20),        # Top-left
    (-35, -30),       # Bottom-left outer
    (-18, -25),       # Left slot bottom-left
    (-5, 0),          # Center convergence point (approx)
    (-2, -32),        # Middle prong left-bottom
    (12, -32),        # Middle prong right-bottom
    (10, 0),          # Center convergence right side
    (35, -22),        # Right slot bottom
    (55, -10),        # Bottom-right outer
    (50, 30),         # Top-right
    (0, 50)           # Close
]).close().extrude(2.0)

# That polyline was self-intersecting or messy.
# Let's do the subtraction method, it's safer for generated code.

base_shape = (
    cq.Workplane("XY")
    .polyline([
        (0, 40),       # Top
        (40, 30),      # Top Right
        (50, -10),     # Bottom Right Side
        (30, -35),     # Bottom Right Corner tip
        (-10, -35),    # Bottom Center
        (-30, -30),    # Bottom Left Corner tip
        (-40, 10)      # Top Left
    ])
    .close()
    .extrude(thickness)
)

# Cutter 1: The gap separating the left block from the middle strip
# Defined as a polygon
c1 = (
    cq.Workplane("XY")
    .polyline([
        (-5, -5),     # Apex
        (-20, -40),   # Bottom Left
        (-12, -40),   # Bottom Right
        (2, -5)       # Top Right
    ])
    .close()
    .extrude(10)
    .translate((-5, 0, -5))
)

# Cutter 2: The gap separating the middle strip from the right block
c2 = (
    cq.Workplane("XY")
    .polyline([
        (5, -5),      # Apex
        (10, -40),    # Bottom Left
        (35, -25),    # Bottom Right
        (15, -2)      # Top Right
    ])
    .close()
    .extrude(10)
    .translate((5, 0, -5))
)

result = base_shape.cut(c1).cut(c2)
# Refine Base shape to match image better
# The image is slightly asymmetric.

base_poly = [
    (0, 40),       # Top
    (45, 25),      # Top Right
    (55, -15),     # Bottom Right Side
    (35, -28),     # Bottom Right Tip
    (15, -15),     # Inner crook (will be cut)
    (-15, -35),    # Bottom Left Tip
    (-45, 10)      # Top Left
]
# Actually, let's just trace the positive geometry. 
# It is composed of 3 parts if we split it, or 1 part with holes.
# The "middle finger" is connected to the top body.
# The "left side" is connected to the top body.
# The "right side" is connected to the top body.
# They all meet at the main body mass.

# Final coordinate set attempt for a single subtraction operation
base_points = [
    (0, 35),       # Top
    (40, 20),      # Top Right
    (48, -15),     # Right Side
    (30, -30),     # Bottom Right
    (-5, -30),     # Bottom Middle
    (-30, -25),    # Bottom Left
    (-40, 5)       # Left Side
]

# Recalculating based on visual proportions
# Center is approx (0,0)
# Top tip: (0, 30)
# Top Right: (30, 20)
# Bottom Right: (35, -15)
# Bottom Left: (-30, -20)
# Top Left: (-30, 15)

base_geo = cq.Workplane("XY").polyline([
    (0, 40),      # Top
    (50, 25),     # Top Right
    (60, -15),    # Mid Right
    (30, -30),    # Bottom Right Tip
    (0, -10),     # Bottom Center (virtual)
    (-25, -30),   # Bottom Left Tip
    (-50, 10),    # Top Left
    (0, 40)
]).close().extrude(2)

# Slot 1 (Left vertical-ish)
slot1 = cq.Workplane("XY").polyline([
    (-5, 0), 
    (-15, -40), 
    (-8, -40), 
    (2, 0)
]).close().extrude(10).translate((-5,0,-5))

# Slot 2 (Right angled)
slot2 = cq.Workplane("XY").polyline([
    (5, 0),
    (15, -40), 
    (45, -25), 
    (15, 5)
]).close().extrude(10).translate((5,0,-5))

result = base_geo.cut(slot1).cut(slot2)