import cadquery as cq
import math

# --- Parameters ---
base_diameter = 100.0  # Outer diameter of the base plate
base_thickness = 2.0   # Thickness of the base plate
hub_diameter = 15.0    # Diameter of the central hole (shaft)
num_blades = 12        # Number of blades
blade_height = 20.0    # Height of the blades
blade_thickness = 1.5  # Thickness of each blade

# Blade profile control points (relative to center)
# These control the curvature of the blade
# Inner point (near hub)
r_inner = 12.0
angle_inner = 0.0
# Outer point (near rim)
r_outer = 48.0
angle_outer = 60.0 # Degrees of twist
# Mid point control for curvature
r_mid = (r_inner + r_outer) / 2.0
angle_mid = (angle_inner + angle_outer) / 2.0 - 15 # Offset for curve

# Fillet radius at the root of the blades
fillet_radius = 2.0

# --- Geometry Construction ---

# 1. Base Plate
base = cq.Workplane("XY").circle(base_diameter / 2.0).extrude(base_thickness)

# 2. Define a single blade profile
# We'll create a spline curve for the blade centerline, offset it, and extrude
def make_blade_curve():
    # Convert polar to cartesian for control points
    p1 = (r_inner * math.cos(math.radians(angle_inner)), r_inner * math.sin(math.radians(angle_inner)))
    p2 = (r_mid * math.cos(math.radians(angle_mid)), r_mid * math.sin(math.radians(angle_mid)))
    p3 = (r_outer * math.cos(math.radians(angle_outer)), r_outer * math.sin(math.radians(angle_outer)))
    
    # Create the blade cross-section
    # We draw a line (thin rectangle) following the path
    # But a cleaner way in CQ is to make a solid block and intersect or just extrude a shape
    # Let's try extruding a sketch on the face.
    
    # Better approach for curved thin walls: 
    # Create a Workplane, draw the curve, offset it to get thickness, extrude.
    
    path = (
        cq.Workplane("XY")
        .moveTo(p1[0], p1[1])
        .threePointArc(p2, p3)
    )
    return path

# Create the detailed blade shape
# We need a closed wire to extrude. We'll offset the spline.
def make_blade_solid():
    # Points for the spline
    p_start = (r_inner * math.cos(math.radians(angle_inner)), r_inner * math.sin(math.radians(angle_inner)))
    p_mid = (r_mid * math.cos(math.radians(angle_mid)), r_mid * math.sin(math.radians(angle_mid)))
    p_end = (r_outer * math.cos(math.radians(angle_outer)), r_outer * math.sin(math.radians(angle_outer)))
    
    # Calculate offset points approximately or use a thin rectangle that is twisted
    # A robust way is to use a sweep or a loft, but simpler is to draw the profile.
    
    # Let's define the blade as a polyline following the arc with thickness
    # Since offsetting splines perfectly in 2D scripts can be tricky, 
    # we will approximate the blade shape using two concentric arcs.
    
    # Simplified approach: Extrude a curved shape.
    blade = (
        cq.Workplane("XY")
        .workplane(offset=base_thickness)
        .moveTo(p_start[0], p_start[1])
        .threePointArc(p_mid, p_end)
        # Create a wire for the path to sweep a rectangle along? No, standard extrusion is better.
        # Let's try to make a face by offsetting.
    )
    
    # Using the thicken/offset functionality if available, otherwise constructing the closed loop manually.
    # Manual closed loop construction for reliability:
    # Outer curve
    # Inner curve (rotated slightly or scaled)
    
    # Let's use a slot-like approach: define points, make spline, offset curve.
    # Since CQ pure offset can be finicky, we'll build the two sides.
    
    # Define angles for thickness approximation
    ang_offset = math.degrees(blade_thickness / r_mid) # Approximate angular thickness
    
    p1_in = (r_inner * math.cos(math.radians(angle_inner)), r_inner * math.sin(math.radians(angle_inner)))
    p2_in = (r_mid * math.cos(math.radians(angle_mid)), r_mid * math.sin(math.radians(angle_mid)))
    p3_in = (r_outer * math.cos(math.radians(angle_outer)), r_outer * math.sin(math.radians(angle_outer)))
    
    # Shifted points for the other side of the blade
    # We shift perpendicular to the curve, but a simple rotation is often close enough for impellers
    # Or just shift X/Y slightly.
    
    # Let's use CadQuery's wire offset tool which is robust in recent versions.
    wire = (
        cq.Workplane("XY")
        .moveTo(p1_in[0], p1_in[1])
        .threePointArc(p2_in, p3_in)
    )
    
    # Create a thin solid by offsetting the wire in 2D then extruding
    # Note: offset2D requires a closed wire usually, or produces a closed wire from an open one
    blade_face = wire.offset2D(blade_thickness / 2.0)
    blade_solid = blade_face.extrude(blade_height)
    
    return blade_solid

# Generate one blade
single_blade = make_blade_solid()

# 3. Pattern the blades
# We unite the blades into a single compound object before unioning with base
blades = single_blade
for i in range(1, num_blades):
    blades = blades.union(single_blade.rotate((0, 0, 0), (0, 0, 1), i * (360.0 / num_blades)))

# 4. Combine Base and Blades
impeller = base.union(blades)

# 5. Create Central Hub Hole
# Cut through everything
impeller = impeller.faces(">Z").workplane().circle(hub_diameter / 2.0).cutThruAll()

# 6. Apply Fillets
# The image shows fillets where the blades meet the base plate.
# Finding these specific edges can be done by selecting edges at the base Z-level
# that are not the outer rim or the inner hole.

# We select edges that are at the intersection of the blades and the base plate.
# These edges are generally at Z = base_thickness.
try:
    impeller = impeller.edges(
        cq.selectors.AndSelector(
            cq.selectors.BoxSelector(
                (-base_diameter/2, -base_diameter/2, base_thickness - 0.1),
                (base_diameter/2, base_diameter/2, base_thickness + 0.1)
            ),
            cq.selectors.TypeSelector("CIRCLE", result_type=False) # Exclude pure circles (like the hub/rim might be interpreted)
        )
    ).fillet(fillet_radius)
except:
    # Fallback if complex selection fails, just return un-filleted or try broader selection
    # In complex topology, fillets sometimes fail. 
    # Let's try a simpler selector: edges "on top" of the base plate face, minus the outer rim.
    pass

result = impeller