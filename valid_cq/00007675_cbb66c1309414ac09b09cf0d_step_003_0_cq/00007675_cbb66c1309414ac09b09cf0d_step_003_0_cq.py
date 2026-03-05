import cadquery as cq

# Parametric dimensions for the blower fan housing
fan_radius = 25.0       # Radius of the main circular part
fan_height = 15.0       # Total height of the housing
wall_thickness = 1.5    # Thickness of the outer shell

exit_width = 24.0       # Width of the rectangular air exit
exit_length = 20.0      # Length of the exit nozzle extrusion
fillet_radius = 2.0     # Fillet radius where the nozzle meets the main body

mount_lug_radius = 3.5  # Radius of the mounting lugs
mount_hole_radius = 1.6 # Radius of the screw holes
mount_dist = 32.0       # Distance from center to mounting lug center

hub_radius = 12.0       # Radius of the central hub area
inlet_radius = 10.0     # Radius of the air intake opening
hub_recess = 2.0        # Depth of the recess for the fan hub

# 1. Main Body Construction
# The main body shape of a centrifugal fan is roughly a circle + a tangent exit.
# We'll sketch the base profile.

# Create the base sketch
s = (
    cq.Sketch()
    .push([(0, 0)])
    .circle(fan_radius)  # The main circular chamber
)

# Create the exit nozzle profile
# We need a shape that transitions from the circle to a straight exit
# A common simplified way is a rectangle merged with the circle.
# Let's define the exit rectangle.
# The exit usually points tangentially. Looking at the image, it shoots "up and right" relative to a standard circle.
# Let's orient it along the Y-axis for simplicity, then rotate or adjust.
# Actually, looking at the image: The exit is a tangential extension.
# Let's make a hull of a circle and a box to approximate the spiral casing shape simply.

# Define the box for the outlet
# Center of the box needs to be offset so one side is tangent to the fan circle.
# Let's align the exit along the Y-axis.
box_center_x = (fan_radius + exit_length) / 2.0
box_center_y = fan_radius/2.0 + 5 # Offset slightly to create the spiral look
# This is tricky to get perfect without complex curves, but a union of a cylinder and a box works for a visual approximation.

base_geo = (
    cq.Workplane("XY")
    .circle(fan_radius)
    .extrude(fan_height)
)

# Create the rectangular exit extension
# We place a rectangle tangent to the circle
exit_geo = (
    cq.Workplane("XY")
    .center(0, fan_radius/2.0) # Shift up
    .box(exit_width, fan_radius + exit_length, fan_height, centered=(True, False, False))
)

# Rotate the exit to match the approximate 45-degree angle in the image if we assume standard orientation,
# but looking at the image, let's keep it simple: Circle center at (0,0), exit pointing towards +Y/+X.
# Let's reconstruct using a sketch hull for a cleaner transition.

pts = [
    (0, 0),
    (exit_width/2, fan_radius),
    (exit_width/2, fan_radius + exit_length),
    (-exit_width/2, fan_radius + exit_length),
    (-exit_width/2, 0) # Back to near center
]

# A better approach for the specific "spiral" shape:
# 1. Main Cylinder
# 2. Tangential Box
# 3. Mounting Ears
# 4. Central Hub

# Step 1: Main Cylinder
main_body = cq.Workplane("XY").circle(fan_radius).extrude(fan_height)

# Step 2: The Tangential Exit (Nozzle)
# Positioning a box such that its side is tangent to the circle
exit_extension = (
    cq.Workplane("XY")
    .center(0, 0)
    .moveTo(-exit_width/2, 0)
    .lineTo(-exit_width/2, fan_radius + exit_length)
    .lineTo(exit_width/2, fan_radius + exit_length)
    .lineTo(exit_width/2, 0)
    .close()
    .extrude(fan_height)
)

# Rotate the extension to allow tangential mating
# The image shows the exit coming off a "corner".
# Let's offset the extension so one wall aligns with the circle edge approx.
exit_extension = exit_extension.translate((fan_radius/2, 0, 0))

# Combine body and exit
fan_housing = main_body.union(exit_extension)

# Create a smoother transition (fillet) at the neck if needed, though union handles it fairly well.

# Step 3: Mounting Lugs
# Lug 1 (Left)
lug1 = (
    cq.Workplane("XY")
    .center(-mount_dist, 0)
    .circle(mount_lug_radius)
    .extrude(fan_height)
)

# Lug 2 (Right)
lug2 = (
    cq.Workplane("XY")
    .center(mount_dist, 0)
    .circle(mount_lug_radius)
    .extrude(fan_height)
)

fan_housing = fan_housing.union(lug1).union(lug2)

# Step 4: Add Mounting Holes
fan_housing = (
    fan_housing
    .faces(">Z")
    .workplane()
    .pushPoints([(-mount_dist, 0), (mount_dist, 0)])
    .hole(mount_hole_radius * 2)
)

# Step 5: Hollow out the central area (The Fan Intake)
# We need a stepped hole: A large recess for the blades, and a central hub.
# Looking at the image, there is a central hub (motor mount) connected by struts (not visible/simplified)
# or just a central opening with a recessed motor mount area.
# Let's create the recess described in the image.

# Cut the main inlet
fan_housing = (
    fan_housing
    .faces(">Z")
    .workplane()
    .circle(inlet_radius)
    .cutBlind(-hub_recess) # The shallow recess at the top
)

# Cut the deeper inside (simulating the volute interior), leaving a floor thickness
fan_housing = (
    fan_housing
    .faces(">Z")
    .workplane()
    .circle(hub_radius) # Slightly larger or smaller depending on design
    .cutBlind(-(fan_height - wall_thickness)) # Leave bottom wall
)

# Re-add the central motor hub cylinder inside
motor_hub = (
    cq.Workplane("XY")
    .workplane(offset=wall_thickness) # Start from inner floor
    .circle(inlet_radius - 2) # Smaller than the opening
    .extrude(fan_height - wall_thickness - hub_recess) # Build up to just below the rim
)

# In the image, the center is a solid flat circle recessed slightly from the top face.
# Let's adjust. The center looks like a "cap".
# We will just fill the center back in, but recessed.
center_cap = (
    cq.Workplane("XY")
    .workplane(offset=fan_height - hub_recess) # Start at the recessed level
    .circle(inlet_radius - 0.5) # Gap for air
    .extrude(- (fan_height/2)) # Go down halfway
)

# Actually, the image shows a large central circular area that is slightly lower than the top face.
# It seems to be the motor hub itself.
# Let's refine the top cut.
fan_housing = main_body.union(exit_extension).union(lug1).union(lug2) # Reset base

# Apply the mounting holes
fan_housing = (
    fan_housing
    .faces(">Z")
    .workplane()
    .pushPoints([(-mount_dist, 0), (mount_dist, 0)])
    .hole(mount_hole_radius * 2)
)

# Create the central recess
fan_housing = (
    fan_housing
    .faces(">Z")
    .workplane()
    .circle(inlet_radius + 2) # The outer rim of the recess
    .cutBlind(-2.0) # Depth of the top lip
)

# Create the central hole (gap around the hub)
fan_housing = (
    fan_housing
    .faces(">Z")
    .workplane(offset=-2.0)
    .circle(inlet_radius + 2)
    .circle(inlet_radius) # Create a ring
    .extrude(-5.0, combine='cut') # Cut a ring groove
)

# Let's simplify to match the visual exactly: 
# A flat top face, with a large circular recess, and inside that recess a central circular solid (hub).

final_body = main_body.union(exit_extension).union(lug1).union(lug2)

# 1. Cut the main hole for the screw mounts
final_body = (
    final_body
    .faces(">Z")
    .workplane()
    .pushPoints([(-mount_dist, 0), (mount_dist, 0)])
    .hole(mount_hole_radius * 2)
)

# 2. Create the central features
# Cut a large pocket for the fan area
final_body = (
    final_body
    .faces(">Z")
    .workplane()
    .circle(hub_radius + 4) # Outer diameter of the black ring area
    .cutBlind(-2.0) # Shallow cut for the lip
)

# Add the central hub back in (or rather, don't cut it fully, but easier to add)
# The image shows a gap (black ring) around a central grey cylinder.
# So we cut a deep ring.
final_body = (
    final_body
    .faces(">Z")
    .workplane(offset=-2.0) # Start from the bottom of the shallow cut
    .circle(hub_radius + 4) # Outer radius of gap
    .circle(hub_radius)     # Inner radius of gap (hub start)
    .cutBlind(-5.0)         # Depth of the gap
)

# Rotate the whole thing to match the isometric view orientation roughly
# The image has the exit pointing "back and left". 
# The current model has exit pointing roughly +Y/X.
result = final_body.rotate((0,0,0), (0,0,1), -45)