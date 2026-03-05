import cadquery as cq

# --- Parameters ---
arm_length = 50.0       # Distance from center to post
arm_thickness = 4.0     # Thickness of the web connecting the parts
hub_od = 12.0           # Outer diameter of the central hub
hub_id = 6.0            # Inner diameter of the central hub (the hole)
post_od = 6.0           # Diameter of the corner posts
post_height = 50.0      # Total height of the corner posts
hub_height = 20.0       # Height of the central hub
curve_radius = 40.0     # Radius of the arc connecting posts to hub
fillet_radius = 2.0     # Fillet at the base

# --- Construction ---

# 1. Create one arm (a quadrant)
# We will create a profile that represents one "web" connecting the center to a post
# Imagine looking at the object from the side.

# Define points for the web profile
# Origin is at (0,0) which corresponds to the center bottom of the part
pts = [
    (hub_od / 2.0, 0),                 # Bottom inside (near hub)
    (arm_length, 0),                   # Bottom outside (near post)
    (arm_length, post_height),         # Top outside (post top)
    (arm_length - post_od/2.0, post_height), # Move in slightly for post thickness
    (arm_length - post_od/2.0, 10),    # Go down, but not all the way
    # We need a curved cut here. Let's simplify: straight lines first or a spline
    # Looking at the image, it's a deep curve like a parabola or large radius arc.
    # Let's define the top of the web as a point significantly lower than the post.
    (hub_od / 2.0, hub_height)         # Top inside (hub top)
]

# Let's try a different approach: Build the main components and loft or union them.
# The shape is complex to sketch in one go because of the curvature.
# Let's build the "X" base shape first, then the sweeping curves.

# Strategy B:
# 1. Create the central cylinder.
# 2. Create the 4 corner cylinders.
# 3. Create the "webs" connecting them with the specific curved profile.

# 1. Central Hub
hub = cq.Workplane("XY").circle(hub_od/2.0).extrude(hub_height)
hub_hole = cq.Workplane("XY").circle(hub_id/2.0).extrude(hub_height).cut(hub) # Cut hole later

# 2. Corner Posts
# We'll make one and rotate/copy it
post = (cq.Workplane("XY")
        .center(arm_length, 0)
        .circle(post_od/2.0)
        .extrude(post_height))

# 3. The Web (Connecting Arm)
# The web connects the hub to the post. It has a curved top profile.
# We will draw this profile in the XZ plane and extrude it symmetrically.

# Calculate points for the web sketch
x_start = hub_od / 2.0 - 1.0 # overlap slightly
x_end = arm_length + 1.0     # overlap slightly
y_hub_top = hub_height
y_post_top = post_height
y_post_bottom = 0 # Assume flat bottom for now

# Create the profile of the web
# It looks like a sweep or a loft, but an extrusion of a side profile is closest.
web_profile = (
    cq.Workplane("XZ")
    .moveTo(x_start, 0)
    .lineTo(x_end, 0) # Bottom line
    .lineTo(x_end, post_height * 0.8) # Go up the post side partially
    # Create the swooping curve down to the hub
    .threePointArc((x_start + (x_end-x_start)*0.5, hub_height * 0.5), (x_start, y_hub_top)) 
    .close()
)

# Extrude the web
web = web_profile.extrude(arm_thickness/2.0, both=True)

# 4. Combine one arm assembly
one_arm = post.union(web)

# 5. Pattern the arms
# We need 4 arms rotated 90 degrees
arms = one_arm
for i in range(1, 4):
    arms = arms.union(one_arm.rotate((0,0,0), (0,0,1), 90 * i))

# 6. Combine with Hub
result_solid = hub.union(arms)

# 7. Add the central hole
result_solid = result_solid.faces("<Z").workplane().circle(hub_id/2.0).cutThruAll()

# 8. Refinements based on the image
# The image shows "lips" or reduced diameters at the top of the posts and hub.
# Let's add the small indents at the top of the posts.
# Post top detail:
for i in range(4):
    angle = 90 * i
    # Position for the cut
    cut_loc = cq.Workplane("XY").rotate((0,0,0), (0,0,1), angle).center(arm_length, 0).workplane(offset=post_height)
    # Create a small cylindrical cut to make it look like a tube or stepped pin
    # Actually, looking closer, it looks like a stepped down diameter.
    # We'll cut a ring.
    result_solid = result_solid.cut(
        cq.Workplane("XY").rotate((0,0,0), (0,0,1), angle)
        .center(arm_length, 0)
        .workplane(offset=post_height - 2.0) # Start slightly down
        .circle(post_od/2.0 + 1.0) # Outer boundary (large enough)
        .circle(post_od/2.0 - 0.5) # Inner boundary (the resulting pin size)
        .extrude(3.0) # Cut upwards
    )

# Hub top detail (similar stepped look)
result_solid = result_solid.cut(
    cq.Workplane("XY")
    .workplane(offset=hub_height - 2.0)
    .circle(hub_od/2.0 + 1.0)
    .circle(hub_od/2.0 - 0.5)
    .extrude(3.0)
)

# 9. Fillets
# The base where the arms meet the posts and the hub are filleted.
# This is often computationally expensive or tricky, so we apply carefully.
# We select edges perpendicular to Z that are at the bottom.
try:
    result = result_solid.edges("|Z").fillet(fillet_radius/2.0)
except:
    # Fallback if fillets fail on complex geometry
    result = result_solid

# Final variable assignment
result = result