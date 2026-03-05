import cadquery as cq
import math

# --- Parametric Dimensions ---
# Main body dimensions
outer_diameter = 40.0
inner_diameter = 36.0  # Defines wall thickness
total_length = 50.0

# "Visor" or hood feature dimensions
hood_length = 20.0     # The length of the section with the visor
hood_thickness_adder = 4.0 # How much thicker the hood is than the base tube
hood_angle = 240.0     # The coverage angle of the hood in degrees (looks like roughly 2/3rds)

# The flat spot on top of the hood
flat_width = 18.0

# The small hole on the side
hole_diameter = 2.0
hole_offset_from_front = 10.0 # Distance from the front face
hole_angle_offset = 45.0      # Angle from the side/horizontal

# --- Derived Dimensions ---
radius = outer_diameter / 2.0
hood_radius = radius + hood_thickness_adder
wall_thickness = (outer_diameter - inner_diameter) / 2.0

# --- Modeling Strategy ---
# 1. Create the base cylindrical tube.
# 2. Create the "hood" feature as a thicker cylindrical segment.
# 3. Cut the flat top on the hood.
# 4. Cut the bottom section away from the hood to create the open visor shape.
# 5. Drill the small hole.
# 6. Hollow out the entire center.

# Step 1: Base Tube
# We'll create the main cylindrical body first.
base_tube = cq.Workplane("XY").circle(radius).extrude(total_length)

# Step 2: Create the Hood/Visor Outer Shape
# We create a cylinder at the front end that is larger.
# The hood is located at the 'top' (positive Z in local extrude coordinates, usually)
# Let's align the tube along Z-axis.
hood_solid = (
    cq.Workplane("XY")
    .workplane(offset=total_length - hood_length)
    .circle(hood_radius)
    .extrude(hood_length)
)

# Join the hood to the base
main_body = base_tube.union(hood_solid)

# Step 3: Create the flat top on the hood
# We need to cut a flat surface.
# Calculate height of the flat cut based on width and radius
# We want the flat to be tangent or chordal. Looking at image, it's a chordal cut.
# We cut away anything above a certain Y height.
# Using the Pythagorean theorem to find the Y distance for the cut plane:
# y_cut = sqrt(r^2 - (w/2)^2)
y_cut_height = math.sqrt(hood_radius**2 - (flat_width/2.0)**2)

# Create a cutting box for the flat top
# Position it high up so it cuts off the top arc
flat_cut = (
    cq.Workplane("XY")
    .workplane(offset=total_length - hood_length)
    .transformed(offset=(0, y_cut_height, 0))
    .box(hood_radius*2 + 5, hood_radius, hood_length + 5, centered=(True, False, False))
)

main_body = main_body.cut(flat_cut)

# Step 4: Cut the bottom section to define the "visor" shape
# The image shows the hood only covers the top and sides, the bottom matches the inner diameter or base diameter.
# Actually, looking closely, the bottom part of the hood section is cut away entirely, exposing the base tube? 
# Or rather, the hood wraps around like a C-clip.
# Let's cut away the bottom sector of the hood.
# We will cut a rectangular block from the bottom half, but restrict it to the hood length.

# Calculate the cutout height. The image shows the cut goes up to about the midline or slightly below.
# Let's assume the hood covers roughly -30 to +210 degrees (if 0 is right).
# A simple way is to cut a box from the bottom up to a certain Y coordinate.
cutout_y_start = -hood_radius 
cutout_y_end = -radius * 0.2 # Cut slightly above the bottom tangent of the inner tube

# We create a cutting shape for the bottom opening of the hood
bottom_cut = (
    cq.Workplane("XY")
    .workplane(offset=total_length - hood_length)
    .transformed(offset=(0, -hood_radius * 2, 0)) # Start low
    .box(hood_radius * 3, hood_radius * 2 - (hood_radius - abs(cutout_y_end)), hood_length + 1, centered=(True, False, False))
)

# Apply the cut only to the hood region essentially.
# However, the image shows the *inner* bore is continuous. The outer "hood" layer is what is missing at the bottom.
# To achieve this cleanly:
# 1. We have the merged body (Base + Hood).
# 2. We cut the bottom part of the *hood radius* back down to the *base radius*? 
# No, looking at the transition, the hood is an added layer. The bottom of that section is just the base tube.
# So, instead of Unioning a full cylinder then cutting, let's intersect or just create the hood shape correctly first.

# Alternative Step 2 Revised:
# Create the specific cross-section of the hood and extrude it.
# The hood is a partial circle with a flat top.
s = cq.Workplane("XY").workplane(offset=total_length - hood_length)

# Define points for the custom profile
# We want an arc that goes from some angle to another, and a flat top.
# Easier method: Create the full shape with flat top, then cut the bottom.
# Let's stick to the subtractive method on the Union, it's robust.

# Let's refine the bottom cut. The image shows the hood ends abruptly on the sides.
# The cut should be a box removing the material from Y_min up to some Y_level, 
# but we must preserve the inner tube geometry if the hood was just added on top.
# Actually, looking at the front face, the wall thickness looks constant *except* for the hood.
# The hood adds thickness.
# So, the bottom cut should remove the "Hood Material" but leave the "Base Tube" material.
# But `main_body` merged them.
# So we need a cutter that is: an annulus (hood_radius outer, radius inner) restricted to the bottom sector.

# Create the cutter for the bottom of the hood
cutter_mask = (
    cq.Workplane("XY")
    .workplane(offset=total_length - hood_length)
    .circle(hood_radius) # Outer limit
    .rect(hood_radius*4, hood_radius*2, centered=True) # Make it a box context
    .extrude(hood_length)
)
# Now we restrict this cutter. We want to keep the top part.
# Let's go back to simplest geometric construction:
# 1. Tube (0 to 50)
# 2. Hood Shell (30 to 50), shaped like a C-clip with a flat top.

# Re-doing the construction for clarity and robustness:
# Part A: The long underlying tube
part_a = cq.Workplane("XY").circle(radius).circle(inner_diameter/2.0).extrude(total_length)

# Part B: The Hood
# Start with a solid cylinder
part_b_solid = (
    cq.Workplane("XY")
    .workplane(offset=total_length - hood_length)
    .circle(hood_radius)
    .extrude(hood_length)
)

# Cut the flat top on Part B
part_b_flat = part_b_solid.cut(flat_cut)

# Cut the bottom opening on Part B to make it a "C" shape
# We remove material below a certain Y level to expose the inner tube (Part A)
# The image shows the side walls of the hood go down to about the horizontal centerline.
# Let's cut everything below Y=0 for the hood, maybe slightly lower.
part_b_c_shape = (
    part_b_flat.cut(
        cq.Workplane("XY")
        .workplane(offset=total_length - hood_length)
        .transformed(offset=(0, -hood_radius, 0))
        .box(hood_radius * 3, hood_radius, hood_length + 5, centered=(True, False, False))
    )
)

# Now we need to make sure Part B has a hole for Part A to fit through
part_b_final = part_b_c_shape.cut(
    cq.Workplane("XY")
    .workplane(offset=total_length - hood_length)
    .circle(radius)
    .extrude(hood_length)
)

# Combine them
result_solid = part_a.union(part_b_final)

# Step 5: The side hole
# The hole is on the side of the hood.
# Looking at the image, there is a small circular depression or hole.
# It seems to be on the left side (negative X if Y is up).
# We define a workplane on the surface or tangent.
# Let's define a plane tangent to the hood radius at a specific angle.

# Angle roughly 20-30 degrees below the horizontal equator? No, looks like it's on the cheek.
# Let's put it at X = -radius, Y = something small.
hole_pos_angle = 195.0 # degrees
hole_z_pos = total_length - hole_offset_from_front

# Create an axis for the hole
hole_axis = cq.Vector(math.cos(math.radians(hole_pos_angle)), math.sin(math.radians(hole_pos_angle)), 0)

# We can cut a hole by creating a cylinder oriented correctly and subtracting
hole_cutter = (
    cq.Workplane("XY")
    .workplane(offset=hole_z_pos)
    .transformed(rotate=(0, 0, hole_pos_angle)) # Rotate to face the radial direction
    .transformed(rotate=(90, 0, 0)) # Rotate to point inward/outward
    .circle(hole_diameter/2.0)
    .extrude(hood_radius * 2) # Length of cutter
)

result = result_solid.cut(hole_cutter)

# Ensure the final output is just the object
# Just in case `part_a` hollow operation didn't propagate through the union (it usually does for simple unions of disjoint shells, but here they overlap)
# To be 100% safe on the internal bore:
core_cutter = cq.Workplane("XY").circle(inner_diameter/2.0).extrude(total_length * 2).translate((0,0,-10))
result = result.cut(core_cutter)