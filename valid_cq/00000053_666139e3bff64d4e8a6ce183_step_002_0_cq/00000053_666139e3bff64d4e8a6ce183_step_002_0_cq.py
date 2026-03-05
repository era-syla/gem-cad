import cadquery as cq

# --- Parameters ---
outer_diameter = 50.0
inner_diameter = 30.0
thickness = 15.0
slit_gap = 3.0

# Keyway dimensions
keyway_width = 5.0
keyway_depth = 2.5  # Depth from the inner radius

# Clamping Screw Hole dimensions
# The screw hole goes tangentially through the collar
screw_head_diameter = 9.0  # For the counterbore
screw_body_diameter = 5.0  # Clearance hole
screw_offset = 18.0        # Distance from center for the tangent screw
head_depth = 5.0           # Depth of the counterbore

# --- Model Construction ---

# 1. Create the main ring body
collar = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(thickness)
)

# 2. Add the Keyway
# We create a rectangular profile and cut it out
keyway = (
    cq.Workplane("XY")
    .rect(keyway_width, outer_diameter) # Tall rectangle to ensure it cuts through
    .extrude(thickness)
    .translate((0, (inner_diameter / 2.0) + (keyway_depth / 2.0) - (outer_diameter/2.0) + keyway_depth, 0))
)
# Note: Calculation above centers the keyway rectangle such that the 'depth' 
# cuts into the inner circle correctly.
# Simpler approach: place center of rect at inner radius + half depth.
key_y_pos = (inner_diameter / 2.0) + (keyway_depth / 2.0)
keyway_cutter = (
    cq.Workplane("XY")
    .center(0, (inner_diameter/2.0) + (keyway_depth/2.0) - (keyway_depth)) # Roughly position
    .rect(keyway_width, keyway_depth * 2) # Make it tall enough to cut clearly
    .extrude(thickness)
)
# Let's refine the keyway position to be exact.
# The bottom of the keyway should be at inner_radius + keyway_depth
keyway_cut = (
    cq.Workplane("XY")
    .center(0, (inner_diameter / 2.0))
    .rect(keyway_width, keyway_depth * 2, centered=True) # Start centered on ID edge
    .translate((0, keyway_depth / 2.0, 0)) # Shift up so the bottom aligns with ID
    .extrude(thickness)
)

collar = collar.cut(keyway_cut)


# 3. Create the clamping slit
# This is a simple rectangular cut through one side of the ring
slit = (
    cq.Workplane("XY")
    .rect(outer_diameter, slit_gap)
    .extrude(thickness)
    .translate((outer_diameter / 2.0, 0, 0)) # Shift to cut one side only
)

collar = collar.cut(slit)


# 4. Create the Clamping Screw Holes
# We need a counterbore on one side and a threaded/clearance hole through the other.
# The hole is tangential to the inner bore.

# Define the plane for the screw hole (Right plane, YZ, rotated or translated)
# The screw axis is along the Y axis in the image, perpendicular to the slit.
# Wait, looking at the image: 
# The slit is vertical (if we view from top). The screw goes horizontally through the "ears" created by the slit.
# In my current orientation (Z is up, ring in XY plane):
# - Slit is along X axis (cutting the positive X side).
# - Screw should be along Y axis, perpendicular to the slit.

# Let's reorient slightly to match the image better conceptually.
# Slit at X positive. Screw goes along Y axis at X positive location.

# Plane setup: Right side of the ring (Positive X), looking along Y axis.
# We create a workplane on the XZ plane, offset to where the screw enters.
# Actually, easiest is to drill from the "front" and "back" relative to the slit.

hole_loc_x = (inner_diameter + outer_diameter) / 4.0 # Midpoint of the ring wall
hole_loc_z = thickness / 2.0

# Create the through hole for the screw body
# Cut a cylinder through the whole slit area
screw_hole = (
    cq.Workplane("YZ")
    .center(0, hole_loc_z) # YZ plane: y=0 is center, z is up. Center is (0, thickness/2)
    .circle(screw_body_diameter / 2.0)
    .extrude(outer_diameter) # Long enough to go through
    .translate((-hole_loc_x, 0, 0)) # Move X to the wall position (negative X relative to YZ plane is standard X?)
    # Wait, YZ plane origin is at X=0.
    # We need to rotate or transform.
)

# Alternative approach for holes: Use simple geometrical primitives and boolean operations
# It's often more robust than complex plane transformations for simple side holes.

# Cylinder for the through hole
screw_shaft = (
    cq.Workplane("XZ")
    .workplane(offset=outer_diameter/2 + 5) # Start outside
    .center(hole_loc_x, hole_loc_z)
    .circle(screw_body_diameter/2.0)
    .extrude(-(outer_diameter + 10)) # Cut all the way through
)

# Counterbore
# In the image, the counterbore looks somewhat spherical or deeply recessed.
# A standard counterbore cylinder is sufficient representation.
# It needs to be on the side of the slit head.
screw_c_bore = (
    cq.Workplane("XZ")
    .workplane(offset=outer_diameter/2 + 1) # Start outside
    .center(hole_loc_x, hole_loc_z)
    .circle(screw_head_diameter/2.0)
    .extrude(-(outer_diameter - inner_diameter)/2.0 + slit_gap) # Depth estimation
    # Usually goes halfway into the material or until the screw head seats
    # Let's make it a specific depth from the surface
)

# Recalculating counterbore based on typical collar design
# The counterbore enters from one tangent side.
# Let's define the cut axis strictly.
# Axis: Line passing through (hole_loc_x, -outer_radius, hole_loc_z) and (hole_loc_x, outer_radius, hole_loc_z)

# Let's use Workplane with correct orientation for the tangent screw
# Position: X = hole_loc_x
# Direction: Y axis
screw_cut_solid = (
    cq.Workplane("XZ")
    .center(hole_loc_x, hole_loc_z) # Position on the wall
    .circle(screw_body_diameter / 2.0)
    .extrude(outer_diameter, both=True) # Cut through everything along Y (normal to XZ)
)

# Counterbore cut
# We only want the counterbore on one side of the slit.
# The slit is at Y=0 (along X axis). 
# Wait, previous slit was: .translate((outer_diameter / 2.0, 0, 0)). This puts the slit along the X-axis.
# So the gap is along Y, cutting the ring at X positive.
# Therefore the screw must go perpendicular to the slit, along the Y axis.

# Let's adjust the Slit orientation to match standard logic:
# Slit usually cuts the ring at one radial position.
# My slit code: rect(outer_diameter, slit_gap). This is a long rectangle along X, width Y.
# If translated to X+, it cuts the ring at 3 o'clock.
# The screw must cross this slit tangentially. i.e. along the Y axis.

counterbore_solid = (
    cq.Workplane("XZ")
    .center(hole_loc_x, hole_loc_z)
    .circle(screw_head_diameter / 2.0)
    .extrude(outer_diameter/2.0) # Extrude along positive Y
)
# We need to position this counterbore correctly.
# Currently extrude on XZ goes along normal (Y).
# We want the head to be recessed into the curvature.
# The image shows a "scoop" style relief cut for the screw head.

# Let's create a simpler flat counterbore first, then apply to the model.
# Move the counterbore so it starts slightly inside the outer diameter
cb_depth_from_tangent = (outer_diameter/2.0) - 4.0 # Seating depth
counterbore_solid = (
    cq.Workplane("XZ")
    .center(hole_loc_x, hole_loc_z)
    .workplane(offset=cb_depth_from_tangent) # Start plane at Y = ...
    .circle(screw_head_diameter / 2.0)
    .extrude(20) # Cut outwards
)

# Let's clean up the logic into one chain
result = (
    cq.Workplane("XY")
    
    # 1. Main Tube
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(thickness)
    
    # 2. Keyway
    .cut(
        cq.Workplane("XY")
        .center(0, (inner_diameter / 2.0))
        .rect(keyway_width, keyway_depth * 2, centered=True)
        .translate((0, keyway_depth / 2.0, 0))
        .extrude(thickness)
    )
    
    # 3. Slit
    .cut(
        cq.Workplane("XY")
        .rect(outer_diameter, slit_gap) # Long X, thin Y
        .translate((outer_diameter / 2.0, 0, 0)) # Move to +X side
        .extrude(thickness)
    )
    
    # 4. Screw Body Hole (Through hole along Y axis)
    .cut(
        cq.Workplane("XZ")
        .center(hole_loc_x, thickness / 2.0)
        .circle(screw_body_diameter / 2.0)
        .extrude(outer_diameter, both=True) # Cut all the way Y
    )
    
    # 5. Counterbore (One side only)
    .cut(
        cq.Workplane("XZ")
        .center(hole_loc_x, thickness / 2.0)
        .workplane(offset=outer_diameter/2.0 - 2.0) # Start slightly inside the OD surface
        .circle(screw_head_diameter / 2.0)
        .extrude(10) # Cut outwards towards +Y
    )
)

# Optional: Add chamfers to edges for realism
result = result.edges("|Z").chamfer(0.5)
result = result.edges(cq.selectors.RadiusNthSelector(0)).chamfer(0.5) # Top/Bottom outer edges

# Final check of the variable
result = result