import cadquery as cq
import math

# --- Parametric Dimensions ---
base_diameter = 40.0
base_height = 25.0
wall_thickness = 3.0

# Nozzle parameters
num_fingers = 6  # Looks like a 6-finger array based on typical designs, though only ~4 visible
finger_length_base = 60.0 # Length of the longest finger
finger_width_base = 12.0
finger_thickness_base = 8.0
finger_taper_ratio = 0.5  # Tip width/base width
finger_angle_offset = 15.0 # Angle splay between fingers
finger_bend_angle = 10.0 # Slight outward bend

# Air hole parameters
hole_diameter = 1.5
holes_per_finger = 6

# --- Helper Functions ---

def create_finger(length, width, thickness, angle_y, angle_z):
    """
    Creates a single tapered finger with internal hollow and air holes.
    """
    # Create the outer shape of the finger (lofted profiles)
    
    # Bottom profile (at the base hub)
    p1 = (
        cq.Workplane("XY")
        .rect(width, thickness)
    )
    
    # Top profile (at the tip)
    # We translate and rotate to get the finger direction
    tip_w = width * finger_taper_ratio
    tip_t = thickness * finger_taper_ratio
    
    # Calculate tip position based on length and slight curve
    # Using a simple linear loft for robustness, positioned creatively
    
    # We will build the finger vertically along Z first, then rotate it
    finger_solid = (
        cq.Workplane("XY")
        .rect(width, thickness)
        .workplane(offset=length)
        .rect(tip_w, tip_t)
        .loft(combine=True)
    )
    
    # Round the tip
    finger_solid = finger_solid.edges(">Z").fillet(tip_t/2.1)
    
    # Hollow out the finger (shelling)
    # Since shell can be tricky on lofts, we'll cut a scaled version
    inner_finger = (
        cq.Workplane("XY")
        .rect(width - wall_thickness, thickness - wall_thickness)
        .workplane(offset=length - wall_thickness)
        .rect(tip_w - wall_thickness*0.5, tip_t - wall_thickness*0.5)
        .loft(combine=True)
    )
    
    finger_shell = finger_solid.cut(inner_finger)
    
    # Add air holes
    # Holes are typically on the flat face. 
    # We create a series of cylinders to cut through.
    for i in range(holes_per_finger):
        # Distribute holes along the length
        z_pos = 10.0 + (length - 15.0) * (i / (holes_per_finger - 1))
        
        # Calculate current width at this Z height for centering
        current_width = width - (width - tip_w) * (z_pos / length)
        
        # We assume holes are on the "top" face relative to the spray direction
        # Let's cut through the Y-axis of the un-rotated finger
        hole = (
            cq.Workplane("XZ")
            .workplane(offset=-thickness) # Start outside
            .moveTo(0, z_pos)
            .circle(hole_diameter/2)
            .extrude(thickness * 3) # Cut through
        )
        finger_shell = finger_shell.cut(hole)

    # Rotate the finger into position
    # angle_y: Splay angle (fan shape)
    # angle_z: Forward/Backward tilt (not strictly needed for flat fan, but good for realism)
    
    final_finger = finger_shell.rotate((0,0,0), (0,1,0), angle_y)
    
    return final_finger

# --- Main Construction ---

# 1. Base Connector (Cylinder)
base = (
    cq.Workplane("XY")
    .circle(base_diameter / 2)
    .extrude(base_height)
)

# Hollow out the base
base_hollow = (
    cq.Workplane("XY")
    .circle((base_diameter / 2) - wall_thickness)
    .extrude(base_height)
)
base = base.cut(base_hollow)

# Add a locking notch at the bottom (detail seen in image)
notch = (
    cq.Workplane("XZ")
    .moveTo(base_diameter/2, 2)
    .rect(5, 4)
    .extrude(10, both=True)
)
base = base.cut(notch)

# 2. Transition Hub (Cone connecting base to fingers)
hub_height = 15.0
hub_top_width = base_diameter * 1.2 # Flares out slightly
hub = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .circle(base_diameter / 2)
    .workplane(offset=hub_height)
    .rect(hub_top_width, 15) # Transition to a flattened oval/rect for the fan
    .loft(combine=True)
)

# Shell the hub to allow air passage
hub_inner = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .circle((base_diameter / 2) - wall_thickness)
    .workplane(offset=hub_height)
    .rect(hub_top_width - wall_thickness*2, 15 - wall_thickness*2)
    .loft(combine=True)
)
hub = hub.cut(hub_inner)

# 3. Generate Fingers
fingers = cq.Assembly()

# Based on the image, the fingers are arranged in a flat fan pattern.
# The middle fingers are longer, outer ones shorter.
finger_configs = [
    # (angle, length_scale)
    (-36, 0.7),
    (-18, 0.9),
    (0, 1.0),
    (18, 0.9),
    (36, 0.7),
    # The image shows a side view suggesting depth, but standard nozzles are often single row.
    # However, the image shows a "stacked" appearance or a curved array.
    # Let's approximate the splay.
]

combined_fingers = None

for i, (angle, scale) in enumerate(finger_configs):
    f_len = finger_length_base * scale
    
    # Generate the finger geometry
    f_geo = create_finger(f_len, finger_width_base, finger_thickness_base, angle, 0)
    
    # Move the finger to the top of the hub
    # We need to position them so their bases overlap slightly with the hub top
    f_geo = f_geo.translate((0, 0, base_height + hub_height - 2.0))
    
    if combined_fingers is None:
        combined_fingers = f_geo
    else:
        combined_fingers = combined_fingers.union(f_geo)

# 4. Combine Everything
result = base.union(hub).union(combined_fingers)

# 5. Fillet the Junctions
# Blending the sharp intersection between fingers and hub
# This is computationally expensive, so we select carefully.
# We select edges that are roughly at the height of the junction.
try:
    result = result.edges(cq.nearestToPoint((0, 0, base_height + hub_height))).fillet(2.0)
except Exception:
    # Fallback if fillets fail due to complex geometry intersection
    pass

# Export or display
# cq.exporters.export(result, "air_nozzle.step")