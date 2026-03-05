import cadquery as cq

# --- Parametric Dimensions ---
# Rod dimensions
rod_length = 200.0
rod_diameter = 6.0

# Collar/Flange dimensions
collar_diameter = 12.0
collar_thickness = 4.0

# Connecting neck dimensions (between rod and housing)
neck_length = 5.0
neck_diameter = 8.0

# Ball Joint Housing dimensions
housing_outer_diameter = 18.0
housing_height = 14.0
housing_thickness = 8.0 # Thickness of the main ring part

# Ball/Stud dimensions
ball_diameter = 14.0
stud_diameter = 10.0
stud_height = 15.0 # Height extending below the housing
stud_base_diameter = 12.0 # Slight reinforcement at base of stud

# Cap/Screw dimensions (top)
cap_diameter = 14.0
cap_height = 2.0
slot_width = 2.0
slot_depth = 1.0

# --- Modeling ---

# 1. The Main Rod
rod = cq.Workplane("YZ").circle(rod_diameter / 2).extrude(rod_length)

# 2. The Collar (Flange)
# We position it at the start of the rod (assumed origin side relative to the next parts)
collar = (
    cq.Workplane("YZ")
    .workplane(offset=-collar_thickness)
    .circle(collar_diameter / 2)
    .extrude(collar_thickness)
)

# 3. The Neck (connecting collar to housing)
neck = (
    cq.Workplane("YZ")
    .workplane(offset=-(collar_thickness + neck_length))
    .circle(neck_diameter / 2)
    .extrude(neck_length)
)

# 4. The Ball Joint Housing (Ring)
# This needs to be perpendicular to the rod. The rod runs along X.
# The housing axis should be vertical (Z).
housing_center_offset = -(collar_thickness + neck_length + housing_outer_diameter/2)

housing = (
    cq.Workplane("XY")
    .workplane(offset=housing_center_offset) # Move to the end of the neck
    # Create the main ring shape
    .transformed(rotate=(0, 90, 0)) # Rotate so the circle is on the XY plane (flat)
    .circle(housing_outer_diameter / 2)
    .extrude(housing_thickness)
)

# Let's refine the housing. It usually has a rounded transition to the neck.
# Instead of a simple cylinder, let's make the "eye" of the rod end.
# We will model the main eye cylinder vertically centered on the rod axis.
eye_center_x = -(collar_thickness + neck_length + housing_outer_diameter/2 * 0.8) # Adjust slightly for overlap

housing_eye = (
    cq.Workplane("XY")
    .workplane(offset=0) # Centered on Z=0
    .transformed(offset=(eye_center_x, 0, -housing_height/2))
    .circle(housing_outer_diameter / 2)
    .extrude(housing_height)
)

# Fillet/Blend the connection between the neck and the housing eye
# A simple way to approximate the "teardrop" shape is a loft or just overlapping geometry.
# Let's add a tapered section for the transition.
transition_start_x = -(collar_thickness + neck_length)
transition = (
    cq.Workplane("YZ")
    .workplane(offset=transition_start_x)
    .circle(neck_diameter/2)
    .workplane(offset=-housing_outer_diameter/2) # Move towards the eye center
    .circle(housing_height/2) # Transition to the height of the housing
    .loft()
)

# 5. The Stud/Ball assembly
# This goes through the housing eye vertically.

# The ball part (inside the housing, usually visible as a spherical bulge)
sphere_part = (
    cq.Workplane("XY")
    .transformed(offset=(eye_center_x, 0, 0))
    .sphere(ball_diameter / 2)
)

# The stud extending downwards
stud = (
    cq.Workplane("XY")
    .transformed(offset=(eye_center_x, 0, 0))
    .circle(stud_diameter / 2)
    .extrude(-stud_height)
)

# Reinforcement at the bottom of the stud (visual detail)
stud_base = (
    cq.Workplane("XY")
    .transformed(offset=(eye_center_x, 0, -housing_height/2))
    .circle(stud_base_diameter / 2)
    .extrude(-2.0)
)


# 6. The Top Cap/Screw
cap = (
    cq.Workplane("XY")
    .transformed(offset=(eye_center_x, 0, housing_height/2))
    .circle(cap_diameter / 2)
    .extrude(cap_height)
)

# Cut the slot in the cap
slot_cutter = (
    cq.Workplane("XY")
    .transformed(offset=(eye_center_x, 0, housing_height/2 + cap_height))
    .rect(cap_diameter + 2, slot_width) # Make it wider than the cap to ensure full cut
    .extrude(-slot_depth)
)

# Combine the housing parts
rod_assembly = rod.union(collar).union(neck).union(transition)
bearing_assembly = housing_eye.union(sphere_part).union(stud).union(stud_base).union(cap)

# Final Boolean operations
# Combine rod and bearing
result = rod_assembly.union(bearing_assembly)

# Cut the slot
result = result.cut(slot_cutter)

# Optional: Add hole through the stud if it's hollow (not visible in image, but common)
# result = result.faces("<Z").workplane().circle(stud_diameter/2 - 2).cutBlind(stud_height + housing_height)

# Apply fillets to smooth the look
try:
    # Fillet the junction between stud base and stud
    result = result.edges(cq.selectors.NearestToPointSelector((eye_center_x, 0, -housing_height/2 - 2))).fillet(0.5)
    
    # Fillet the rod to collar transition
    result = result.edges(cq.selectors.NearestToPointSelector((0, 0, rod_diameter/2))).fillet(0.5)
except:
    pass # Skip fillets if topology makes it difficult without specific edge selection

# Export or display
# cq.exporters.export(result, "rod_linkage.step")