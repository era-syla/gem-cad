import cadquery as cq

# Parameters for the geometry
ring_outer_radius = 20.0
ring_inner_radius = 15.0
ring_thickness = 8.0

arm_thickness_main = 8.0
arm_thickness_stepped = 4.0  # The thinner part of the S-curve
hole_diameter = 2.0

# Define the overall height and curvature control points for the "S" shape
# We will construct the main body using a sketch or spline approach.
# Let's use coordinate points to define the complex S-curve profile.

# Coordinates for the outer profile of the arm
# Starting from the top of the ring connection
p_ring_top_left = (-12, 18)
p_ring_top_right = (12, 10)

# The tip of the hook/arm
p_tip_top = (-20, 110)
p_tip_bottom = (-15, 105)

# Intermediate control points for the S-curve (approximate from visual)
# Left side curve
p_mid_left_1 = (-15, 50)
p_mid_left_2 = (-25, 80)

# Right side curve
p_mid_right_1 = (5, 40)
p_mid_right_2 = (-5, 80)


def create_s_hook():
    # 1. Create the bottom ring
    ring = (
        cq.Workplane("XY")
        .circle(ring_outer_radius)
        .circle(ring_inner_radius)
        .extrude(ring_thickness)
    )

    # 2. Create the main arm body (the S-shape)
    # We'll define a closed profile for the main arm.
    # We need to ensure it connects cleanly to the ring.
    
    # Points defining the main outline
    pts_outline = [
        (ring_outer_radius * 0.8, 10),      # Bottom Right (connect to ring)
        (10, 30),                           # Lower curve right
        (-5, 60),                           # Middle curve right
        (-10, 85),                          # Upper curve right
        (-18, 105),                         # Tip Top Right
        (-25, 108),                         # Tip Top Left
        (-25, 95),                          # Upper curve left
        (-15, 65),                          # Middle curve left
        (-8, 35),                           # Lower curve left
        (-ring_outer_radius * 0.5, 15)      # Bottom Left (connect to ring)
    ]

    # Create the main solid extrusion
    arm_main = (
        cq.Workplane("XY")
        .moveTo(pts_outline[0][0], pts_outline[0][1])
        .spline(pts_outline[1:], includeCurrent=True)
        .close()
        .extrude(arm_thickness_main)
    )
    
    # 3. Create the stepped cutout (the "ridge" effect)
    # This is effectively a cut that follows the right edge of the shape
    # but only goes halfway down.
    
    # Points for the cut profile. This needs to be slightly larger than the 
    # right side of the main arm to ensure a clean cut, but follow the inner contour.
    pts_cut = [
        (20, 10),                           # Start outside right
        (10, 30),                           # Follows curve
        (-5, 60),                           # Follows curve
        (-10, 85),                          # Follows curve
        (-18, 105),                         # Tip
        (-30, 120),                         # Way outside top
        (30, 120),                          # Way outside right
        (30, 10)                            # Back to start Y
    ]
    
    # However, looking closely at the image, it looks more like an Additive process 
    # or a specific shape subtraction on the left side. 
    # Actually, looking at the render, there is a "recessed" area on the right/top face.
    # Let's model it as a full thickness part, then cut away a layer from the right side contour.
    
    # Let's refine the shape logic: The "ridge" follows the left/inner curve.
    # The cut happens on the right/outer curve side.
    
    # Let's define the cut tool shape.
    cut_spline_points = [
        (0, 35),      # Start of the ridge cut
        (-10, 60),
        (-15, 80),
        (-20, 100),   # Near tip
        (10, 120),    # Outside
        (20, 20),     # Outside
    ]
    
    cutter = (
        cq.Workplane("XY")
        .workplane(offset=arm_thickness_stepped) # Start cutting halfway up Z
        .moveTo(cut_spline_points[0][0], cut_spline_points[0][1])
        .spline(cut_spline_points[1:], includeCurrent=True)
        .close()
        .extrude(arm_thickness_main) # Extrude enough to cut through the top
    )

    # 4. Join Ring and Arm
    # Move the arm slightly up to sit on top of the ring's tangent or merge properly
    # In this specific design, the arm base seems to conform to the ring.
    # The spline points started near the ring, so a simple union should work, 
    # but we might need a rectangular block to bridge the gap if the spline didn't touch perfectly.
    
    # Create a small transition block to ensure solidity between ring and arm
    transition = (
        cq.Workplane("XY")
        .moveTo(-10, 0)
        .lineTo(10, 0)
        .lineTo(12, 15)
        .lineTo(-12, 15)
        .close()
        .extrude(arm_thickness_main)
    )

    combined = ring.union(transition).union(arm_main)
    
    # Apply the step cut
    stepped_body = combined.cut(cutter)

    # 5. Add the Holes
    # Hole 1: Lower
    hole1_loc = (-5, 28)
    # Hole 2: Upper
    hole2_loc = (-10, 70)
    
    final_part = (
        stepped_body
        .faces(">Z")
        .workplane()
        .pushPoints([hole1_loc, hole2_loc])
        .hole(hole_diameter)
    )
    
    # 6. Fillets (optional but makes it look like the image)
    # The image shows sharp edges mostly, but maybe slight rounding on the ring connection.
    # We will leave edges sharp as per standard CAD defaults unless specified, 
    # but clean up the ring intersection if needed.
    
    return final_part

# Generate the result
result = create_s_hook()