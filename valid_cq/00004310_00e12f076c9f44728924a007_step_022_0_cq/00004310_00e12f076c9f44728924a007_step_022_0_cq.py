import cadquery as cq

# --- Parametric Dimensions ---
# Main body dimensions
outer_diameter = 50.0
cylinder_height = 40.0
dome_radius = outer_diameter / 2.0
total_height = cylinder_height + dome_radius

# Top opening dimensions
opening_outer_diameter = 25.0  # The main cutout
opening_depth = 5.0
inner_shelf_diameter = 20.0    # The hole going further down
inner_shelf_depth = 10.0

# Notch dimensions
notch_width = 2.0
notch_depth = 1.5
notch_height = 3.0 # How deep down from the top edge the notch goes

# --- Modeling Process ---

# 1. Create the base Cylinder
# We start with the cylindrical section
base = cq.Workplane("XY").circle(outer_diameter / 2.0).extrude(cylinder_height)

# 2. Create the Dome
# We create a sphere and cut it to be a hemisphere, then place it on top
dome = (
    cq.Workplane("XY")
    .workplane(offset=cylinder_height)
    .sphere(dome_radius)
)

# We need to trim the bottom half of the sphere if it protrudes, 
# but simply unioning a sphere centered at the top face works well for a dome.
# To make it cleaner, we can create a hemisphere specifically or intersect.
# A simple way in CQ for a dome cap is to revolve an arc.
# Let's try the sphere union approach, ensuring the center is correct.
# Sphere center needs to be at Z = cylinder_height to form a perfect dome on top.
dome = cq.Workplane("XY", origin=(0, 0, cylinder_height)).sphere(dome_radius)

# Since sphere generates a full sphere, we cut off the bottom half 
# (everything below Z=cylinder_height)
# Actually, a cleaner way is to just Union them. The bottom part of the sphere 
# is inside the cylinder.
body = base.union(dome)

# However, looking closely at the image, the transition is seamless.
# The sphere center is likely at z = cylinder_height.
# Let's cut the bottom of the object flat again just in case the sphere 
# protruded below Z=0 (which it doesn't if cylinder_height > radius, 
# but good practice).
body = body.cut(
    cq.Workplane("XY").workplane(offset=-10).box(100, 100, 10).translate((0,0,-5))
)


# 3. Create the Top Opening (Counterbored Hole)
# First, the wider opening
body = body.faces(">Z").workplane().hole(opening_outer_diameter, opening_depth)

# Second, the thru-hole or deeper pocket (inner shelf)
# The image shows a bottom, so it's a blind hole, not a through hole.
# We drill from the bottom of the previous hole.
body = (
    body.faces(">Z[-2]") # Select the face at the bottom of the first hole
    .workplane()
    .hole(inner_shelf_diameter, inner_shelf_depth) 
)


# 4. Create the Notches
# There are 4 notches around the rim of the opening.
# We can create a cutter profile and pattern it.

# Define a cutter for the notch
notch_cutter = (
    cq.Workplane("XY")
    .workplane(offset=total_height) # Start at the very top of the dome
    .rect(notch_width, opening_outer_diameter + 5) # Rectangle spanning the hole
    .extrude(-notch_depth) # Cut downwards
)

# Refine the cutter: we only want to cut the rim, not the whole center.
# A better approach is to place rectangles on the rim.

def create_notch_cutter(angle):
    return (
        cq.Workplane("XY")
        .workplane(offset=total_height)
        .transformed(rotate=(0, 0, angle))
        .center(opening_outer_diameter/2.0, 0) # Move to the rim edge
        .box(5, notch_width, notch_depth * 2, combined=False) # Box large enough to cut
        .translate((-2.5, 0, -notch_depth)) # Adjust position to cut into the rim
    )

# Create 4 notches
cutters = cq.Workplane("XY")
for i in range(4):
    angle = i * 90
    # Create a box at the specific location on the rim
    # We position a box such that it intersects the inner rim of the larger hole
    # Radius to center of cut: approx opening_outer_diameter/2
    r_cut = opening_outer_diameter / 2.0
    
    cutter = (
        cq.Workplane("XY")
        .workplane(offset=total_height)
        .transformed(rotate=(0, 0, angle))
        .center(r_cut, 0)
        # Create a box: Length (radial), Width (tangential), Height (Z)
        .box(3.0, notch_width, notch_height * 2, centered=(True, True, True))
        .translate((0, 0, -notch_height + 0.1)) # Shift down to cut into the material
    )
    body = body.cut(cutter)

# 5. Finalize
result = body

# Optional: Fillet the transition if needed, but the image looks sharp or tangent.
# The sphere-cylinder transition is tangent by definition if radius matches.

if __name__ == "__main__":
    # If running in an environment that supports show_object (like CQ-editor)
    try:
        show_object(result)
    except NameError:
        pass