import cadquery as cq
import math

def make_gear(num_teeth, module, thickness, bore_radius, center=(0, 0, 0)):
    pitch_radius = num_teeth * module / 2
    addendum = module
    dedendum = 1.25 * module
    outer_radius = pitch_radius + addendum
    root_radius = pitch_radius - dedendum
    base_radius = pitch_radius * math.cos(math.radians(20))
    
    # Build gear profile using tooth geometry
    tooth_angle = 2 * math.pi / num_teeth
    
    # Generate points for one tooth using involute approximation
    def involute_point(base_r, t):
        x = base_r * (math.cos(t) + t * math.sin(t))
        y = base_r * (math.sin(t) - t * math.cos(t))
        return (x, y)
    
    # Build the gear as a series of arcs and lines
    # Use simplified tooth profile: trapezoid approximation
    points = []
    
    for i in range(num_teeth):
        angle_center = i * tooth_angle
        half_tooth = tooth_angle * 0.3
        half_gap = tooth_angle * 0.2
        
        # Root points of this tooth (start of tooth)
        r1_angle = angle_center - half_tooth - half_gap * 0.5
        r2_angle = angle_center - half_tooth
        t1_angle = angle_center + half_tooth
        r3_angle = angle_center + half_tooth + half_gap * 0.5
        
        # Root arc point (between teeth)
        points.append((root_radius * math.cos(r1_angle), root_radius * math.sin(r1_angle)))
        # Tooth flank left
        points.append((pitch_radius * 0.98 * math.cos(r2_angle - 0.01), pitch_radius * 0.98 * math.sin(r2_angle - 0.01)))
        # Tooth tip left
        points.append((outer_radius * math.cos(angle_center - half_tooth * 0.4), outer_radius * math.sin(angle_center - half_tooth * 0.4)))
        # Tooth tip right
        points.append((outer_radius * math.cos(angle_center + half_tooth * 0.4), outer_radius * math.sin(angle_center + half_tooth * 0.4)))
        # Tooth flank right
        points.append((pitch_radius * 0.98 * math.cos(t1_angle + 0.01), pitch_radius * 0.98 * math.sin(t1_angle + 0.01)))
        # Root arc point (end of tooth, start of gap)
        points.append((root_radius * math.cos(r3_angle), root_radius * math.sin(r3_angle)))
    
    # Close the polygon
    points.append(points[0])
    
    # Create the gear body
    gear = (
        cq.Workplane("XY")
        .workplane()
        .polyline(points)
        .close()
        .extrude(thickness)
    )
    
    # Cut bore hole
    gear = (
        gear
        .faces(">Z")
        .workplane()
        .circle(bore_radius)
        .cutThruAll()
    )
    
    # Translate to center position
    gear = gear.translate(center)
    
    return gear

# Gear parameters
module = 1.0

# Large gear
num_teeth_large = 60
thickness_large = 5
bore_large = 6
pitch_radius_large = num_teeth_large * module / 2

# Small gear
num_teeth_small = 30
thickness_small = 5
bore_small = 3
pitch_radius_small = num_teeth_small * module / 2

# Distance between centers (gears mesh)
center_distance = pitch_radius_large + pitch_radius_small

# Create large gear centered at origin
large_gear = make_gear(num_teeth_large, module, thickness_large, bore_large, center=(0, 0, 0))

# Create small gear positioned to mesh with large gear
small_gear = make_gear(num_teeth_small, module, thickness_small, bore_small, center=(center_distance, 0, 0))

# Combine both gears
result = large_gear.union(small_gear)