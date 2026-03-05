import cadquery as cq
import math

# Parameters
outer_radius = 40
inner_radius = 8
blade_count = 12
base_height = 12
blade_height = 30
blade_thickness = 3
blade_width = 12

# Create hexagonal base
base = (
    cq.Workplane("XY")
    .polygon(6, outer_radius * 2)
    .extrude(base_height)
)

# Add center hub
hub = (
    cq.Workplane("XY")
    .circle(inner_radius + 4)
    .extrude(blade_height + base_height)
)

base = base.union(hub)

# Create curved blades arranged radially
def make_blade(angle_deg):
    angle_rad = math.radians(angle_deg)
    
    # Blade profile - curved shape
    # Start at hub, curve outward and twist
    r_start = inner_radius + 4
    r_end = outer_radius - 5
    
    blade = (
        cq.Workplane("XZ")
        .transformed(offset=cq.Vector(0, 0, base_height))
    )
    
    # Create a swept blade using a path
    # Define path points for the blade curve
    path_pts = []
    steps = 8
    for i in range(steps + 1):
        t = i / steps
        r = r_start + (r_end - r_start) * t
        # Add twist angle
        twist = math.radians(60 * t)
        x = r * math.cos(twist)
        y = r * math.sin(twist)
        z = blade_height * t * 0.8
        path_pts.append((x, y, z))
    
    # Build blade as a simple swept shape
    # Use loft approach with profiles at different heights
    profile1 = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(r_start, 0, base_height))
        .rect(blade_thickness, blade_width)
    )
    
    mid_r = (r_start + r_end) / 2
    mid_twist = math.radians(30)
    profile2 = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(mid_r * math.cos(mid_twist), 
                                       mid_r * math.sin(mid_twist), 
                                       base_height + blade_height * 0.4))
        .rect(blade_thickness, blade_width * 0.9)
    )
    
    end_twist = math.radians(60)
    profile3 = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(r_end * math.cos(end_twist),
                                       r_end * math.sin(end_twist),
                                       base_height + blade_height * 0.8))
        .rect(blade_thickness, blade_width * 1.1)
    )
    
    # Simple extrusion blade approach
    blade_solid = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(r_start + (r_end - r_start)/2, 0, base_height + blade_height/2))
        .box(r_end - r_start, blade_thickness, blade_height)
    )
    
    return blade_solid

# Build blades by creating individual blade shapes and rotating them
blades_combined = None

for i in range(blade_count):
    angle = i * (360.0 / blade_count)
    angle_rad = math.radians(angle)
    
    r_mid = (inner_radius + 4 + outer_radius - 5) / 2
    length = outer_radius - 5 - (inner_radius + 4)
    
    # Create a blade as a curved box
    blade = (
        cq.Workplane("XY")
        .box(length, blade_thickness, blade_height * 0.85)
        .translate((r_mid, 0, base_height + blade_height * 0.425))
    )
    
    # Rotate blade to its position
    blade = blade.rotate((0, 0, 0), (0, 0, 1), angle)
    
    if blades_combined is None:
        blades_combined = blade
    else:
        blades_combined = blades_combined.union(blade)

# Combine base with blades
result = base.union(blades_combined)

# Add a separate curved guard piece (visible in image as separate arc piece)
guard_outer = 38
guard_inner = 32
guard_height = 20
guard_angle = 70  # degrees of arc

guard = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, 0, 0))
    .circle(guard_outer)
    .circle(guard_inner)
    .extrude(guard_height)
)

# Cut guard to arc shape
cut_box = (
    cq.Workplane("XY")
    .box(200, 200, 100)
    .translate((0, -100, 50))
)

# Position guard away from main body
guard = guard.translate((outer_radius * 1.8, 0, 0))

result = result.union(guard)