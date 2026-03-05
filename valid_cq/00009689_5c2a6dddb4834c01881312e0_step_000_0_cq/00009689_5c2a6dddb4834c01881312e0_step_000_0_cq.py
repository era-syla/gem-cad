import cadquery as cq

# --- Parameters ---
outer_radius = 50.0       # Radius of the main outer ring
ring_width = 3.0          # Thickness of the ring wall
ring_height = 4.0         # Height (Z) of the ring
spoke_width = 3.0         # Width of the cross spokes
boss_radius = 5.0         # Outer radius of the cylindrical bosses
boss_hole_radius = 2.5    # Inner hole radius of the bosses
boss_height = 6.0         # Height of the bosses (slightly taller than the ring)

# Central feature parameters
center_sq_size = 15.0     # Approximate size of the central cutout area
cutout_feature_w = 2.0    # Width of the cutout line

# --- Modeling ---

# 1. Create the Outer Ring
# We create a tube by subtracting a smaller cylinder from a larger one
ring = (cq.Workplane("XY")
        .circle(outer_radius)
        .circle(outer_radius - ring_width)
        .extrude(ring_height)
        )

# 2. Create the Cross Spokes
# A simple rectangle extruded, then rotated to form the cross
spoke_length = outer_radius * 2.0
spoke1 = (cq.Workplane("XY")
          .rect(spoke_length, spoke_width)
          .extrude(ring_height)
          )
spoke2 = spoke1.rotate((0, 0, 0), (0, 0, 1), 90)

# 3. Create the Mounting Bosses
# There are 4 bosses spaced evenly around the ring. 
# We'll make one and rotate/union it.
# The bosses seem to be centered on the ring's circumference.
boss_positions = [
    (outer_radius - ring_width/2, 0),
    (-(outer_radius - ring_width/2), 0),
    (0, outer_radius - ring_width/2),
    (0, -(outer_radius - ring_width/2))
]

# Note: In the image, the bosses are aligned with the spokes.
# Let's verify the alignment. Yes, they are at 0, 90, 180, 270 degrees.
# However, the spokes in the image are rotated 45 degrees relative to the cardinal axes 
# OR the bosses are rotated 45 degrees relative to the spokes.
# Let's look closely. The spokes form an X shape. The bosses are at the ends of the spokes.
# So if spokes are X (diagonal), bosses are diagonal. 
# Let's stick to cardinal axes for simplicity and rotate the whole model if needed, 
# or just align everything to diagonals. 
# Actually, looking at the image, the spokes go vertically and horizontally? 
# No, the perspective makes it look like an 'X'. 
# Let's assume standard orientation: Bosses at North, South, East, West. Spokes connect them.

bosses = cq.Workplane("XY")
for pos in boss_positions:
    boss = (cq.Workplane("XY")
            .center(*pos)
            .circle(boss_radius)
            .circle(boss_hole_radius)
            .extrude(boss_height)
            )
    bosses = bosses.union(boss)

# 4. Create the Central Detail
# There is a distinct shape in the center. It looks like a square frame 
# rotated 45 degrees (diamond) or just a square aligned with axes, 
# but with "ears" or lobes.
# Looking closely at the crop: It's a square frame located at the intersection.
# It seems to be a void or a thin wall structure.
# It looks like a thin-walled square with rounded corners or looped corners.
# Let's model a square frame in the center.
# The spokes pass through it.
# It looks like a square contour extruded.

# Let's refine the central shape based on the zoomed crop.
# It looks like a square with loop-like corners.
# Let's try to sketch a custom profile for this.
def central_shape(size):
    # A square with small circular lobes at corners
    s = cq.Sketch()
    rect = cq.Workplane("XY").rect(size, size)
    # Add lobes at corners
    offset = size / 2.0
    corner_r = size / 5.0
    
    # Let's just make a rounded rectangle frame that is slightly complex
    # It looks like a "clover" or a square with bulging corners.
    # Let's keep it simple but recognizable: A square rotated 45 deg?
    # No, looking at the crop, the square sides are parallel to the spokes.
    # The spokes connect the midpoints of the square sides? Or corners?
    # The spokes go through the center. The square is "woven" or placed on top/in-plane.
    
    # Let's model a square frame.
    center_frame = (cq.Workplane("XY")
                    .rect(size, size)
                    .rect(size - cutout_feature_w*2, size - cutout_feature_w*2)
                    .extrude(ring_height)
                   )
    
    # Looking very closely at the crop, there are little "ears" on the square.
    # Let's add cylinders at the corners of the square to mimic the "lobes".
    corner_cyls = (cq.Workplane("XY")
                   .rect(size, size, forConstruction=True)
                   .vertices()
                   .circle(cutout_feature_w * 1.5)
                   .extrude(ring_height)
                   )
    
    # Create the hollow effect for corners
    corner_cyls_hollow = (cq.Workplane("XY")
                   .rect(size, size, forConstruction=True)
                   .vertices()
                   .circle(cutout_feature_w * 0.5)
                   .extrude(ring_height)
                   )
    
    return center_frame.union(corner_cyls).cut(corner_cyls_hollow)

# Let's build the assembly.
# We have a ring, spokes, bosses, and a central detail.
# First, unite ring and spokes.
structure = ring.union(spoke1).union(spoke2)

# Now rotated the whole structure 45 degrees so spokes form an X relative to view?
# The image shows spokes at roughly 45 degrees relative to the view plane "horizon".
# But usually modeling is done axis-aligned.
# Let's assume the spokes are on X and Y axes.
# The bosses are at the ends of the spokes.

# Add the central detail.
# The central detail in the image is a bit ambiguous. 
# It looks like a square rotated 45 degrees relative to the spokes.
# If spokes are X/Y, the square is diamond shaped.
# Let's create a diamond shape frame.
center_size = 12.0
center_detail = (cq.Workplane("XY")
                 .rect(center_size, center_size)
                 .rect(center_size - 2.0, center_size - 2.0)
                 .extrude(ring_height)
                 .rotate((0,0,0), (0,0,1), 45) # Rotate 45 degrees to make it a diamond relative to spokes
                 )
# Add small circular loops at the corners of the diamond
diamond_corners = (cq.Workplane("XY")
                   .rect(center_size, center_size, forConstruction=True)
                   .vertices()
                   .circle(2.0)
                   .circle(1.0)
                   .extrude(ring_height)
                   .rotate((0,0,0), (0,0,1), 45)
                   )

center_assembly = center_detail.union(diamond_corners)

# Combine everything
result = structure.union(bosses).union(center_assembly)

# Rotate to match isometric view better (optional, but standard result is usually axis aligned)
# The image shows bosses at diagonals.
result = result.rotate((0,0,0), (0,0,1), 45)

# Final check of intersections.
# The central detail overlaps the spokes. Union handles this.
# The holes in the bosses need to be clear.
# Since we unioned solids (some with holes), the holes might be filled if the spoke extends into them.
# The spokes length is `outer_radius * 2.0`, which goes to the edge of the ring.
# The bosses are centered on the ring.
# The boss hole is radius 2.5. The spoke is width 3.0 (radius 1.5).
# The spoke will block the hole.
# We need to cut the boss holes again at the very end to ensure they are clear.

hole_cutter = cq.Workplane("XY")
for pos in boss_positions:
    h = (cq.Workplane("XY")
         .center(*pos)
         .circle(boss_hole_radius)
         .extrude(boss_height * 2, both=True) # Ensure it cuts through everything
         )
    hole_cutter = hole_cutter.union(h)

# Rotate cutters to match the rotation of the main body
hole_cutter = hole_cutter.rotate((0,0,0), (0,0,1), 45)

result = result.cut(hole_cutter)

# Export or Render command is implicit for the user variable 'result'