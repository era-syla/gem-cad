import cadquery as cq

# Parameters
outer_r = 20
inner_r = 16
thickness = 6
tab_width = 12
tab_length = 15
tab_thickness = 6
hole_r = 2
wall_thickness = outer_r - inner_r  # 4

def make_clip_with_hole(x_offset=0):
    """Create U-shaped clip with a hole tab (left piece)"""
    # Create the U-shape profile by sweeping or extruding
    # Build as 2D profile and extrude
    
    # Outer U shape: semicircle + two straight arms
    arm_length = 15
    
    # Create the profile in XY plane
    # The U opens upward (positive Y direction)
    # Bottom of U is at y=0, arms go up
    
    pts_outer = []
    pts_inner = []
    
    import math
    
    # Build outer profile as a closed wire
    # Left arm top -> left arm bottom -> semicircle -> right arm bottom -> right arm top -> tab -> back
    
    result_clip = (
        cq.Workplane("XY")
        .moveTo(-outer_r, arm_length)
        .lineTo(-outer_r, 0)
        .threePointArc((0, -outer_r), (outer_r, 0))
        .lineTo(outer_r, arm_length)
        .lineTo(outer_r - wall_thickness, arm_length)
        .lineTo(outer_r - wall_thickness, wall_thickness * 0.5)
        .threePointArc((0, -inner_r), (-(outer_r - wall_thickness), wall_thickness * 0.5))
        .lineTo(-outer_r + wall_thickness, arm_length)
        .close()
        .extrude(thickness)
    )
    
    # Add tab on the right side
    tab = (
        cq.Workplane("XY")
        .moveTo(outer_r, arm_length)
        .rect(tab_length, thickness, centered=False)
        .extrude(thickness)
    )
    
    # Actually build tab properly
    tab = (
        cq.Workplane("XY")
        .box(tab_length, thickness, thickness)
        .translate((outer_r + tab_length/2, arm_length - thickness/2, thickness/2))
    )
    
    combined = result_clip.union(tab)
    
    # Add hole to tab
    hole_x = outer_r + tab_length/2
    hole_y = arm_length - thickness/2
    
    combined = (
        combined
        .faces(">Z")
        .workplane()
        .moveTo(hole_x, hole_y)
        .circle(hole_r)
        .cutThruAll()
    )
    
    return combined.translate((x_offset, 0, 0))


def make_clip_with_notch(x_offset=0):
    """Create U-shaped clip with notch tab (right piece)"""
    arm_length = 15
    
    result_clip = (
        cq.Workplane("XY")
        .moveTo(-outer_r, arm_length)
        .lineTo(-outer_r, 0)
        .threePointArc((0, -outer_r), (outer_r, 0))
        .lineTo(outer_r, arm_length)
        .lineTo(outer_r - wall_thickness, arm_length)
        .lineTo(outer_r - wall_thickness, wall_thickness * 0.5)
        .threePointArc((0, -inner_r), (-(outer_r - wall_thickness), wall_thickness * 0.5))
        .lineTo(-outer_r + wall_thickness, arm_length)
        .close()
        .extrude(thickness)
    )
    
    # Add tab on left side with notch cutout
    tab = (
        cq.Workplane("XY")
        .box(tab_length, thickness, thickness)
        .translate((-outer_r - tab_length/2, arm_length - thickness/2, thickness/2))
    )
    
    combined = result_clip.union(tab)
    
    # Add notch cutout in tab
    notch_w = 3
    notch_h = 3
    notch = (
        cq.Workplane("XY")
        .box(notch_w, thickness + 2, notch_h)
        .translate((-outer_r - tab_length + notch_w, arm_length - thickness/2, thickness - notch_h/2))
    )
    
    combined = combined.cut(notch)
    
    return combined.translate((x_offset, 0, 0))


clip1 = make_clip_with_hole(x_offset=-30)
clip2 = make_clip_with_notch(x_offset=30)

result = clip1.union(clip2)