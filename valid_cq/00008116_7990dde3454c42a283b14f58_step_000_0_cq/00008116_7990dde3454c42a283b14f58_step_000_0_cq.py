import cadquery as cq

# --- Parametric Dimensions ---
# Central Body
body_width = 15.0
body_depth = 20.0
body_height = 40.0
body_fillet_radius = 2.0  # Fillet on the top edges
front_rounding_radius = body_width / 2.0 # To make the front perfectly round

# Curved Arms
arm_radius_inner = 35.0
arm_thickness = 5.0
arm_width = 8.0 # Width (Z-height in drawing plane) of the arm
arm_angle = 100.0 # How far the arc sweeps

# Locking features on arm tips
tip_lock_height = 3.0
tip_lock_width = 3.0
tip_recess_depth = 2.0

# --- Geometry Construction ---

# 1. Create the Central Body
# A rectangular block that is rounded on the front face.
# We'll create a sketch on the XY plane and extrude it in Z.
# The shape is a rectangle with a semi-circle on one side.

def create_body_profile():
    # Rectangle part
    rect_part = (
        cq.Workplane("XY")
        .rect(body_width, body_depth - front_rounding_radius)
        .translate((0, -front_rounding_radius / 2.0, 0))
    )
    
    # Circle part for the front
    circle_part = (
        cq.Workplane("XY")
        .circle(front_rounding_radius)
        .translate((0, (body_depth - front_rounding_radius)/2.0, 0))
    )
    
    # Combined profile (Note: fusing sketches directly can be tricky, 
    # often easier to fuse solids or use a single polyline)
    
    # Let's try a simpler approach: Extrude a rectangle, then fillet the front edges heavily.
    # Or create a custom polygon.
    pts = [
        (-body_width/2, -(body_depth - front_rounding_radius)), # Bottom Left
        (body_width/2, -(body_depth - front_rounding_radius)),  # Bottom Right
        (body_width/2, 0),    # Top Right (start of arc)
        (-body_width/2, 0)    # Top Left (end of arc)
    ]
    
    sketch = (
        cq.Workplane("XY")
        .moveTo(pts[0][0], pts[0][1])
        .lineTo(pts[1][0], pts[1][1])
        .lineTo(pts[2][0], pts[2][1])
        .threePointArc((0, front_rounding_radius), pts[3])
        .close()
    )
    return sketch

# Extrude the main body
central_body = create_body_profile().extrude(body_height)

# Add small fillets to the top edge for aesthetics as seen in image
central_body = central_body.faces(">Z").edges().fillet(body_fillet_radius)


# 2. Create the Curved Arms
# We will create one arm and mirror it.
# The arm is an arc in the Front plane (XZ or similar relative to body).

# Defined relative to the back of the body
arm_center_y = -body_depth + 5.0 # Center of the arc relative to body
arm_center_z = body_height / 4.0 # Vertical position of arc center

def create_arm_shape(direction=1):
    # direction: 1 for right, -1 for left
    
    # Create the profile of the arm (rectangular cross-section)
    # We sweep this profile along a path or extrude a ring segment.
    # Let's extrude a ring segment (Workplane based approach).
    
    # We'll draw on the YZ plane (side view) and extrude width-wise? 
    # No, looking at the image, the curve is in the Front plane (XZ plane of the object).
    # So we draw the arc shape on the Front plane and extrude it in Y (depth).
    
    # Calculating outer radius
    arm_radius_outer = arm_radius_inner + arm_thickness
    
    # Construct the arm sketch
    arm_sketch = (
        cq.Workplane("XZ")
        .moveTo(arm_radius_inner, 0)
        .lineTo(arm_radius_outer, 0)
        # Create outer arc
        .ellipseArc(x_radius=arm_radius_outer, y_radius=arm_radius_outer, 
                    angle1=0, angle2=arm_angle, sense=1)
        # Line back to inner radius
        .lineTo(
            arm_radius_inner * cq.np.cos(cq.np.radians(arm_angle)), 
            arm_radius_inner * cq.np.sin(cq.np.radians(arm_angle))
        )
        # Inner arc back to start
        .ellipseArc(x_radius=arm_radius_inner, y_radius=arm_radius_inner, 
                    angle1=arm_angle, angle2=0, sense=-1)
        .close()
    )
    
    # Extrude the arm
    arm_solid = arm_sketch.extrude(arm_width)
    
    # The default extrusion is centered or positive normal. 
    # We need to position this arm relative to the central body.
    # The arm seems to attach near the bottom-back.
    
    # Rotate to orient correctly (standing up like a U)
    # Currently it's starting at X-axis going CCW.
    # We want it to start at bottom (-Z) and go up.
    # Let's rotate -90 degrees around Y to stand it up? No, around Y rotates in XZ plane.
    # Actually, let's just rotate the solid in the scene.
    
    # Move arm to correct position
    # Rotate so the start of the arc is at the bottom
    arm_solid = arm_solid.rotate((0,0,0), (0,1,0), -90)
    
    # Translate to position
    # We want the "bottom" of the U to be near the bottom of the body.
    arm_solid = arm_solid.translate((
        0, # X center
        -(body_depth - front_rounding_radius) - arm_width/2.0, # Y: Back of body
        arm_radius_outer # Z: Lift up so bottom is at 0 roughly
    ))
    
    # Add the locking details at the tip of the arm
    # Select the top face of the arm tip
    tip_face = arm_solid.faces(">Z").val()
    
    # Create the small block on the tip (locking mechanism)
    # This is a simplification based on the visual
    tip_detail = (
        cq.Workplane(obj=tip_face)
        .workplane(offset=0)
        .rect(arm_thickness, arm_width) # Base rect
        .extrude(tip_lock_height)
    )
    
    # Cut a notch in the tip detail
    tip_detail = (
        tip_detail.faces(">Z").workplane()
        .rect(arm_thickness/2.0, arm_width - 2.0)
        .cutBlind(-tip_recess_depth)
    )
    
    arm_complete = arm_solid.union(tip_detail)
    
    # Center the arm structure on the X axis before mirroring
    # The arm construction started at x=radius.
    # We need to shift it so the center of the arc assembly is at X=0
    # Actually, the way we constructed it:
    # 1. Sketch on XZ.
    # 2. Rotated -90 around Y.
    # The "center" of the arc rotation is at (0,0,0) locally before translation.
    # After translation, the center of curvature is at (0, Y_pos, Z_pos).
    # So the left/right symmetry plane is the YZ plane.
    
    return arm_complete

# Create the Right Arm
# Since we rotated -90, the arc sits on the X-axis. 
# We need to shift it in X to make room for the central body? 
# No, the U-shape implies the arms are one continuous piece or joined at the center.
# The image shows them coming out of the sides/bottom of the main block.
# Let's construct the "U" shape in one go to align better.

def create_u_bracket():
    path = (
        cq.Workplane("XZ")
        .moveTo(-arm_radius_inner, arm_radius_inner) # Top Left tip
        .threePointArc((0, 0), (arm_radius_inner, arm_radius_inner)) # Bottom center, Top Right tip
    )
    
    # Create the profile rectangle
    # We need to define the profile on the plane normal to the start of the path?
    # Or simpler: Make the U-shape by cutting two circles.
    
    outer_u = (
        cq.Workplane("XZ")
        .moveTo(-arm_radius_inner - arm_thickness, arm_radius_inner)
        .threePointArc((0, -arm_thickness), (arm_radius_inner + arm_thickness, arm_radius_inner))
        .lineTo(arm_radius_inner, arm_radius_inner)
        .threePointArc((0, 0), (-arm_radius_inner, arm_radius_inner))
        .close()
        .extrude(arm_width)
    )
    
    # Move to align with body
    # The body is centered at X=0.
    # The U-shape center is (0,0) in XZ.
    # Extrusion went into +Y (default).
    
    outer_u = outer_u.translate((0, -(body_depth) + arm_width/2.0, body_height/2.0 - 5.0))
    
    # Add tip details
    # Left Tip
    left_tip = (
        cq.Workplane("XY")
        .rect(arm_thickness, arm_width)
        .extrude(tip_lock_height)
        .translate((-arm_radius_inner - arm_thickness/2.0, -(body_depth) + arm_width, arm_radius_inner + body_height/2.0 - 5.0))
    )
    
    # Right Tip
    right_tip = (
        cq.Workplane("XY")
        .rect(arm_thickness, arm_width)
        .extrude(tip_lock_height)
        .translate((arm_radius_inner + arm_thickness/2.0, -(body_depth) + arm_width, arm_radius_inner + body_height/2.0 - 5.0))
    )

    # Cut notches (simplified)
    notch_cutout = cq.Workplane("XY").rect(2.0, arm_width).extrude(10)
    
    # Apply notches
    left_tip = left_tip.cut(notch_cutout.translate((-arm_radius_inner - arm_thickness/2.0 + 1.0, -(body_depth) + arm_width, arm_radius_inner + body_height/2.0 - 5.0 + tip_lock_height - 1.5)))
    right_tip = right_tip.cut(notch_cutout.translate((arm_radius_inner + arm_thickness/2.0 - 1.0, -(body_depth) + arm_width, arm_radius_inner + body_height/2.0 - 5.0 + tip_lock_height - 1.5)))

    return outer_u.union(left_tip).union(right_tip)

# Let's refine the U-bracket to match the image better. 
# The arms connect to the BACK of the central body.
bracket = create_u_bracket()

# Shift bracket to attach to back of body properly
# Body back face is at Y = -(body_depth - front_rounding_radius) roughly
# Let's adjust based on visual overlap
bracket = bracket.translate((0, -3.0, -5.0)) 


# Combine Result
result = central_body.union(bracket)

# Final orientation adjustment to match isometric view in image
# (CadQuery usually defaults to Z-up, the image looks like Y-up or Z-up isometric)
# No specific rotation needed for 'result' standard, but code is valid.