import cadquery as cq

# Parameters
disk_radius = 20.0
disk_thickness = 3.0
chevron_distance = 35.0  # Distance from center to the chevron tip
chevron_angle = 90.0     # Angle of the chevron V-shape
chevron_thickness = 1.0  # Thickness of the chevron lines
chevron_height = 1.0     # Height (extrusion depth) of the chevrons
chevron_gap = 2.0        # Gap between the double chevron lines
chevron_arm_length = 15.0 # Length of the chevron arms

def create_double_chevron(distance, arm_length, angle, thickness, gap, height):
    """
    Creates a double chevron shape pointing away from the origin.
    The 'distance' parameter positions the inner tip of the inner chevron.
    """
    # Helper to create a single V-shape path
    def make_v_wire(offset_dist):
        # Calculate start point based on angle and arm length
        # Assuming the tip is at (offset_dist, 0)
        # We need to calculate the endpoints of the arms
        import math
        half_angle_rad = math.radians(angle / 2.0)
        
        # Tip point
        p_tip = (offset_dist, 0)
        
        # End points
        # x = distance + len * cos(half_angle)
        # y = len * sin(half_angle)
        # However, the V points OUTWARDS. So the arms go BACKWARDS relative to the tip direction?
        # Looking at the image, the chevrons point outwards.
        # Let's assume the tip is the furthest point out for now, or the closest point in?
        # Image: The points of the V are directed away from the center.
        # So the "tip" is at `distance` from center.
        # The arms extend backwards towards the center or sideways.
        # Let's look closer. The V points away. So the tip is at radius R.
        # The arms go back towards the center? No, usually arrows point direction.
        # These look like "expand" icons.
        # Top arrow points UP. Tip is at max Y. Arms go down-left and down-right.
        
        dx = arm_length * math.sin(half_angle_rad)
        dy = arm_length * math.cos(half_angle_rad)
        
        # Let's build it on the XY plane pointing in +Y direction first
        # Tip at (0, offset_dist)
        # Arms go to (-dx, offset_dist - dy) and (dx, offset_dist - dy)
        
        p_tip = (0, offset_dist)
        p_left = (-dx, offset_dist - dy)
        p_right = (dx, offset_dist - dy)
        
        return cq.Workplane("XY").polyline([p_left, p_tip, p_right])

    # Inner chevron wire
    inner_wire = make_v_wire(distance)
    
    # Outer chevron wire
    # The outer one is further away from the center
    outer_wire = make_v_wire(distance + gap + thickness)

    # Create thin rectangular profiles along these paths
    # We can do this by offsetting the wires to create faces
    
    # Method 2: Draw the full 2D profile sketch directly
    # This is often more robust than thickening wires
    import math
    half_angle_rad = math.radians(angle / 2.0)
    sin_a = math.sin(half_angle_rad)
    cos_a = math.cos(half_angle_rad)
    
    # We will construct a shape on the XY plane pointing +Y
    # Then we will rotate/move it
    
    def make_chevron_sketch(tip_y_offset):
        # Centerline is Y-axis
        # Tip is at (0, tip_y_offset)
        # We need a shape with thickness
        
        # Outer points of the V strip
        p_tip_outer = (0, tip_y_offset + thickness/2.0 / sin_a if sin_a !=0 else 0) 
        # Actually, let's keep it simple. perpendicular thickness.
        
        # Let's use the wire offset method which handles corners nicely
        # Create a V wire
        dx = arm_length * sin_a
        dy = arm_length * cos_a
        
        tip = (0, tip_y_offset)
        p1 = (-dx, tip_y_offset - dy)
        p2 = (dx, tip_y_offset - dy)
        
        path = cq.Workplane("XY").polyline([p1, tip, p2])
        
        # Use offset2D to create the thickened shape
        # offset2D creates a closed wire around the path
        # 'kind' parameter controls corners (intersection, arc, tangent)
        return path.toPending().offset2D(thickness/2.0, kind="intersection")

    # Create inner chevron solid
    # Position: "distance" is where the pointy part starts visually
    inner_sketch = make_chevron_sketch(distance)
    inner_solid = inner_sketch.extrude(height)
    
    # Create outer chevron solid
    # Gap is the empty space between them
    # Shift by thickness (of inner) + gap + thickness/2?
    # Let's say distance is the centerline of the V stroke.
    # Spacing between centerlines = thickness + gap? No.
    # Visual gap = gap. 
    # Centerline shift = (thickness/2) + gap + (thickness/2) = thickness + gap
    outer_sketch = make_chevron_sketch(distance + thickness + gap)
    outer_solid = outer_sketch.extrude(height)
    
    return inner_solid.union(outer_solid)

# 1. Create the central disk
disk = cq.Workplane("XY").circle(disk_radius).extrude(disk_thickness)

# 2. Create the four chevron sets
chevrons = cq.Workplane("XY")

# We create one set pointing UP (+Y)
# Based on the image, the top set points UP.
base_chevron = create_double_chevron(
    distance=chevron_distance,
    arm_length=chevron_arm_length,
    angle=chevron_angle,
    thickness=chevron_thickness,
    gap=chevron_gap,
    height=chevron_height
)

# Rotate and unite for all 4 directions
top = base_chevron
right = base_chevron.rotate((0,0,0), (0,0,1), -90)
bottom = base_chevron.rotate((0,0,0), (0,0,1), 180)
left = base_chevron.rotate((0,0,0), (0,0,1), 90)

all_chevrons = top.union(right).union(bottom).union(left)

# Combine everything
result = disk.union(all_chevrons)

# Export or Display (standard requirement)
if "show_object" in locals():
    show_object(result)