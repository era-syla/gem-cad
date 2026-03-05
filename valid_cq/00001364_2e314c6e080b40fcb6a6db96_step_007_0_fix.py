import cadquery as cq
import math

# Parameters for T-slot aluminum extrusion profile (40x40mm)
profile_size = 40
slot_width = 8
slot_depth = 6
slot_neck = 6
center_hole_r = 4
extrusion_length = 120

def make_40x40_profile(length):
    """Create a 40x40 T-slot aluminum extrusion profile"""
    s = profile_size
    sw = slot_width
    sd = slot_depth
    sn = slot_neck
    
    # Main square profile
    result = (
        cq.Workplane("XY")
        .rect(s, s)
        .extrude(length)
    )
    
    # Cut center hole
    result = (
        result
        .faces(">Z")
        .workplane()
        .circle(center_hole_r)
        .cutThruAll()
    )
    
    # Cut T-slots on all 4 sides
    # Top slot
    slot_profile = (
        cq.Workplane("XY")
        .polyline([
            (-sn/2, 0),
            (-sn/2, sd - sw/2),
            (-sw/2, sd - sw/2),
            (-sw/2, sd),
            (sw/2, sd),
            (sw/2, sd - sw/2),
            (sn/2, sd - sw/2),
            (sn/2, 0),
            (-sn/2, 0),
        ])
        .close()
        .extrude(length)
    )
    
    # Top slot
    top_slot = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(0, s/2, 0), rotate=cq.Vector(0, 0, 0))
        .polyline([
            (-sn/2, 0),
            (-sn/2, -sd + sw/2),
            (-sw/2, -sd + sw/2),
            (-sw/2, -sd),
            (sw/2, -sd),
            (sw/2, -sd + sw/2),
            (sn/2, -sd + sw/2),
            (sn/2, 0),
        ])
        .close()
        .extrude(length)
    )
    result = result.cut(top_slot)
    
    # Bottom slot
    bottom_slot = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(0, -s/2, 0))
        .polyline([
            (-sn/2, 0),
            (-sn/2, sd - sw/2),
            (-sw/2, sd - sw/2),
            (-sw/2, sd),
            (sw/2, sd),
            (sw/2, sd - sw/2),
            (sn/2, sd - sw/2),
            (sn/2, 0),
        ])
        .close()
        .extrude(length)
    )
    result = result.cut(bottom_slot)
    
    # Left slot
    left_slot = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(-s/2, 0, 0))
        .polyline([
            (0, -sn/2),
            (sd - sw/2, -sn/2),
            (sd - sw/2, -sw/2),
            (sd, -sw/2),
            (sd, sw/2),
            (sd - sw/2, sw/2),
            (sd - sw/2, sn/2),
            (0, sn/2),
        ])
        .close()
        .extrude(length)
    )
    result = result.cut(left_slot)
    
    # Right slot
    right_slot = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(s/2, 0, 0))
        .polyline([
            (0, -sn/2),
            (-sd + sw/2, -sn/2),
            (-sd + sw/2, -sw/2),
            (-sd, -sw/2),
            (-sd, sw/2),
            (-sd + sw/2, sw/2),
            (-sd + sw/2, sn/2),
            (0, sn/2),
        ])
        .close()
        .extrude(length)
    )
    result = result.cut(right_slot)
    
    return result

# Create two extrusions at an angle (like a bent joint ~135 degrees)
angle_deg = 45  # angle from horizontal

# First extrusion - horizontal going left
extr1 = make_40x40_profile(extrusion_length)
extr1 = extr1.translate((-extrusion_length/2, 0, 0))

# Rotate first extrusion to go at 180 degrees (pointing left)
extr1 = extr1.rotate((0, 0, 0), (0, 0, 1), 180)

# Second extrusion - angled going upper right at 45 degrees
extr2 = make_40x40_profile(extrusion_length)
extr2 = extr2.rotate((0, 0, 0), (0, 1, 0), -90)
extr2 = extr2.rotate((0, 0, 0), (0, 0, 1), 45)
extr2 = extr2.translate((extrusion_length/2 * math.cos(math.radians(45)),
                          extrusion_length/2 * math.sin(math.radians(45)), 0))

# Combine both extrusions
result = extr1.union(extr2)