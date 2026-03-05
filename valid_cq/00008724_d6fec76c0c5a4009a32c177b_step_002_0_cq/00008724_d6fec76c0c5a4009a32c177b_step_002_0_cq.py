import cadquery as cq
import math

# --- Parameters ---
disk_diameter = 100.0
disk_thickness = 8.0

# Central star shape parameters
star_points = 6
star_outer_radius = 35.0
star_inner_radius = 15.0  # Controls the sharpness of the star points
star_height = 12.0
fillet_radius = 5.0 # Large fillet between the star and the base

# Peripheral slot parameters
slot_count = 6
slot_width = 12.0
slot_height = 8.0 # Radial length
slot_position_radius = 42.0 # Distance from center to center of slot

# --- Geometry Construction ---

# 1. Base Disk
base = cq.Workplane("XY").circle(disk_diameter / 2.0).extrude(disk_thickness)

# 2. Central Star-like Boss
# We will create a sketch for the star shape.
# A star shape can be approximated by lofting or extruding a custom profile.
# Looking at the image, the sides are concave arcs.
# Let's build a custom wire for the star profile.

def star_profile(points, outer_r, inner_r):
    pts = []
    angle_step = 2 * math.pi / points
    
    # We will construct this using a series of 3-point arcs
    # For each "point" of the star, we need an outer vertex.
    # Between vertices, the curve dips inward.
    
    # Actually, the image looks like circles were subtracted from a larger circle 
    # to form the star shape, or arcs connecting the tips.
    # Let's try constructing a path of arcs.
    
    # Start at the first outer point
    path = cq.Workplane("XY").workplane(offset=disk_thickness)
    
    # To make a smooth continuous star with concave sides:
    # We iterate through the points.
    
    # Calculate vertices
    vertices = []
    for i in range(points):
        theta = i * angle_step
        # Tip of the star
        x_tip = outer_r * math.cos(theta)
        y_tip = outer_r * math.sin(theta)
        vertices.append((x_tip, y_tip))
        
    # Create the shape. 
    # The "sides" of the star look like arcs curving inwards.
    # We can use radiusArc to connect the tips.
    # We need a negative radius or a "through" point closer to the center.
    
    # Let's find a midpoint for the arc
    arcs = []
    start_point = vertices[0]
    
    # Initialize the wire at the first point
    wire = path.moveTo(start_point[0], start_point[1])
    
    for i in range(points):
        # Current tip is vertices[i]
        # Next tip is vertices[(i+1)%points]
        next_idx = (i + 1) % points
        end_point = vertices[next_idx]
        
        # Calculate angle for the "valley" between tips
        mid_theta = (i + 0.5) * angle_step
        
        # Calculate a point for the arc to pass through (the inner radius)
        mid_x = inner_r * math.cos(mid_theta)
        mid_y = inner_r * math.sin(mid_theta)
        
        # Draw the arc
        wire = wire.threePointArc((mid_x, mid_y), end_point)
        
    star_solid = wire.close().extrude(star_height)
    return star_solid

# Generate the star geometry
star_boss = star_profile(star_points, star_outer_radius, star_inner_radius)

# 3. Combine Base and Star
# The star sits on top of the base.
# The base was extruded up to `disk_thickness`. The star sketch started at `disk_thickness`.
combined = base.union(star_boss)

# 4. Apply Fillet
# The image shows a very smooth transition (fillet) between the star boss and the flat disk.
# We select the edges at the bottom of the star boss.
# These edges are at Z = disk_thickness.
combined = combined.edges(cq.selectors.NearestToPointSelector((0,0,disk_thickness))).fillet(fillet_radius)

# 5. Peripheral Slots
# The slots are rectangular/trapezoidal cuts around the rim.
# Based on the image, they look like simple rectangular through-cuts or pockets.
# Let's make them rectangular pockets going all the way through for simplicity, or blind pockets.
# Looking closely, the shadow suggests they go through or are deep. Let's make them through holes.

# Create a single slot shape to cut
slot_sketch = (
    cq.Workplane("XY")
    .workplane(offset=disk_thickness) # Start cutting from top surface
    .rect(slot_width, slot_height) # Create rectangle
)

# Cut the slots in a polar array
final_model = combined
for i in range(slot_count):
    angle = i * (360.0 / slot_count)
    # The slots are rotated so their width is tangential. 
    # .rect() creates an axis-aligned rectangle.
    # We need to move it out to radius, then rotate it around the center Z axis.
    
    # More robust way: Create the cut directly on the object using polar coordinates mechanism isn't standard in CQ fluid API for sketches like this easily without context rotation.
    # We will rotate the workplane.
    
    cut_op = (
        cq.Workplane("XY")
        .workplane(offset=disk_thickness + 1) # Start slightly above to ensure clean cut
        .transformed(rotate=cq.Vector(0, 0, angle)) # Rotate the coordinate system
        .center(slot_position_radius, 0) # Move to the radial position
        .rect(slot_height, slot_width) # Define rect (swapped w/h because radial direction is X in transformed plane)
        .extrude(-disk_thickness - star_height - 2) # Cut downwards through everything
    )
    final_model = final_model.cut(cut_op)


# Assign to result
result = final_model