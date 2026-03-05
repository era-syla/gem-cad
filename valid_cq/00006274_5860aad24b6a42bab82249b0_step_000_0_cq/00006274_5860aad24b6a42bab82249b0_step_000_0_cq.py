import cadquery as cq
import math

# --- Parameters ---
# Stem (bottom part)
stem_diameter = 10.0
stem_length = 50.0

# Collar (middle part)
collar_diameter = 20.0
collar_height = 15.0

# Funnel/Cup (top part)
cup_outer_radius_top = 40.0
cup_wall_thickness = 4.0
cup_height = 40.0
cup_base_radius = collar_diameter / 2.0

# The cup is cut at an angle. To achieve the "scoop" shape, 
# we can revolve a profile and then cut it, or loft profiles.
# Looking at the image, it looks like a revolved profile that has been 
# sliced by a plane or simply constructed as a partial revolution with a unique shape.
# Let's try a revolution of a spline profile to get the nice curve, 
# and then cut away the front section to create the "spout" look.

# --- Modeling Process ---

# 1. Create the Stem
stem = cq.Workplane("XY").circle(stem_diameter / 2).extrude(stem_length)

# 2. Create the Collar on top of the stem
collar = (
    cq.Workplane("XY")
    .workplane(offset=stem_length)
    .circle(collar_diameter / 2)
    .extrude(collar_height)
)

# 3. Create the Cup Shape
# We will create a solid revolution first, then hollow it out or shell it.
# The profile needs to go from the collar radius to the top radius with a curve.

# Define the workplane for the profile on top of the collar
base_plane_z = stem_length + collar_height

# Let's define points for a curved profile
p0 = (cup_base_radius, 0)
p1 = (cup_base_radius + (cup_outer_radius_top - cup_base_radius) * 0.3, cup_height * 0.4)
p2 = (cup_outer_radius_top, cup_height)

# Create the solid outer shape of the cup
cup_solid = (
    cq.Workplane("XZ")
    .workplane(offset=base_plane_z) # Move origin to top of collar
    .moveTo(0, 0)
    .lineTo(p0[0], p0[1])           # Start at collar edge
    .threePointArc(p1, p2)          # Curve up to top rim
    .lineTo(0, p2[1])               # Close to center axis
    .close()
    .revolve()
)

# Create the inner cutting shape (for the hollow)
# We offset the points inwards by the wall thickness
p0_in = (cup_base_radius - cup_wall_thickness/2, 0) # Taper bottom slightly or match hole
# Ensure hole at bottom matches roughly the stem or slightly smaller/larger based on flow
# Let's just make it hollow with consistent thickness approx
inner_r_top = cup_outer_radius_top - cup_wall_thickness
inner_r_base = cup_base_radius # Let it taper to the collar hole

p1_in = (inner_r_base + (inner_r_top - inner_r_base) * 0.3, cup_height * 0.4)
p2_in = (inner_r_top, cup_height)

cup_hollow_tool = (
    cq.Workplane("XZ")
    .workplane(offset=base_plane_z)
    .moveTo(0, 0)
    .lineTo(p0[0], 0) # Start from same outer edge to ensure bottom connectivity?
    # Actually, for a funnel, we want a hole through. 
    # Let's define the inner curve starting from a hole radius.
    # Let's assume the hole diameter matches the stem diameter roughly for flow.
    .moveTo(0,0)
    .lineTo(stem_diameter/2, 0)
    .threePointArc(p1_in, p2_in)
    .lineTo(0, p2_in[1])
    .close()
    .revolve()
)

# Combine stem, collar and solid cup
full_solid = stem.union(collar).union(cup_solid)

# Hollow out the cup
hollowed_shape = full_solid.cut(cup_hollow_tool)

# 4. Create the "Scoop" Cut
# The image shows the front cut away. It looks like a slanted plane cut 
# or a large cylindrical cut. Looking at the "lip", it curves down.
# A slanted plane cut is the most robust way to get this scoop look.

# Define a cutting plane.
# The plane should pass through the top rim at the back, 
# and cut lower at the front.
# Let's use a large block or a defined face to cut.

cut_angle = 45.0 # degrees
cut_z_offset = base_plane_z + (cup_height * 0.3) # Start cut partway up the cup

# Create a cutting volume using a workplane rotated at the desired angle
# We want to keep the "back" (positive Y) and cut the "front" (negative Y).
scoop_cut = (
    cq.Workplane("YZ")
    .workplane(offset=0)
    .transformed(rotate=(cut_angle, 0, 0)) # Tilt the plane
    .workplane(offset=cut_z_offset)       # Move it up/down relative to tilt center
    .rect(200, 200)                       # Big rectangle
    .extrude(200)                         # Cut upwards/outwards
)

# However, Extruding a rotated plane can be tricky to place exactly. 
# Alternative: Create a cutting solid based on global coordinates.
# Let's define 3 points for a splitting plane or use a large subtractive shape.

# Let's try a cleaner approach: Make a large box, rotate it, and subtract.
# The box needs to cover the front half and slope upwards.
cutter = (
    cq.Workplane("XY")
    .rect(200, 200)
    .extrude(100)
    .rotate((0,0,0), (1,0,0), -cut_angle) # Tilt the box
    .translate((0, -65, base_plane_z + cup_height + 10)) # Position it
)
# Fine tuning position:
# We want the cut to be high at Y+, low at Y-.
# The image shows the scoop is open at the front (Viewer perspective).
# Let's assume Y- is the front.
# The cut plane passes from somewhere near the top of the back rim
# down to the front.

# Let's construct a simpler cutter: A wedge.
wedge_height = cup_height * 1.5
wedge_width = cup_outer_radius_top * 3
wedge_angle = 30

# Position a cutting plane
# Point 1: Top of the back rim (0, radius, top_z)
# Point 2: Somewhere lower on the front (0, -radius, low_z)
pt_back = (0, cup_outer_radius_top, base_plane_z + cup_height)
pt_front = (0, -cup_outer_radius_top, base_plane_z + cup_height * 0.4)
pt_side = (100, 0, base_plane_z + cup_height * 0.7) # Just to define plane

# Since CadQuery splitting with 3 points can be verbose, 
# let's use the solid subtraction method with a rotated box, it's reliable.

cutter_box = (
    cq.Workplane("XY")
    .workplane(offset=base_plane_z + cup_height) # Start at top
    .box(200, 200, 200, centered=(True, True, False)) # Box sitting on top
    .rotate((0,0,0), (1,0,0), -35) # Tilt backward to expose the back, cut the front?
    # If we tilt -35 around X, the part +Y goes up, -Y goes down. 
    # The box is initially at Z=top. 
    # So +Y part of box lifts off the model (keeping the back of the cup).
    # -Y part of box sinks into the model (cutting the front of the cup).
    .translate((0, 0, -10)) # Shift down slightly to catch the rim properly
)

result = hollowed_shape.cut(cutter_box)

# 5. Drill the central bore
# Ensure the hole goes all the way through the stem and collar
# The cup creation already handled the upper funnel part, but let's clean the shaft.
bore = (
    cq.Workplane("XY")
    .circle(stem_diameter / 2 - 1.5) # Wall thickness of stem approx 1.5
    .extrude(stem_length + collar_height + 5) # Cut through stem and collar
)

# Looking at the image, the inside is smooth. The previous hollow_tool
# started at the stem_diameter/2, so the transition should be okay.
# Let's just ensure the stem itself is hollow.
result = result.cut(bore)

# Add a fillet to the transition between collar and cup for smoothness (optional but good)
# Finding the edge at the neck
try:
    result = result.edges(cq.selectors.NearestToPointSelector((0, cup_base_radius, base_plane_z))).fillet(2.0)
except:
    pass # In case selection is tricky

# Final clean up (optional fillets on the cut edge if feasible, often fails on complex intersections)
# result = result.edges("%CIRCLE").fillet(0.5) 

# Export/Return
if __name__ == "__main__":
    # If running in CQ-Editor
    # show_object(result)
    pass