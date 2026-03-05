import cadquery as cq
import math

# --- Parameters ---
wire_diameter = 2.0         # Diameter of the wire material
coil_diameter = 15.0        # Mean diameter of the coil
num_active_coils = 10       # Number of main helical coils
coil_pitch = 4.0            # Distance between coils (center-to-center). For extension springs, typically ~= wire_diameter for close-wound.
hook_height = 15.0          # Height of the hook loop from the last coil
hook_radius = coil_diameter / 2.0  # Radius of the hook (usually matches coil radius)

# Derived Parameters
coil_radius = coil_diameter / 2.0
total_height = num_active_coils * coil_pitch

# --- Helper Function for Helix ---
def make_helix(r, p, n, wire_r):
    """
    Creates the main helical body of the spring.
    r: Mean radius of coil
    p: Pitch
    n: Number of turns
    wire_r: Radius of the wire
    """
    path = cq.Workplane("XY").parametricCurve(
        lambda t: (
            r * math.cos(t * 2 * math.pi),
            r * math.sin(t * 2 * math.pi),
            p * t
        )
    ).val()
    
    # Sweep a circle along the path
    # We create a new workplane at the start of the path for the profile
    profile = cq.Workplane("XZ").center(r, 0).circle(wire_r)
    return profile.sweep(path, isFrenet=True)

# --- Generate Main Coil ---
# Create the central helical section
main_coil = make_helix(coil_radius, coil_pitch, num_active_coils, wire_diameter / 2.0)

# --- Helper Function for Extension Hooks ---
# Extension spring hooks are complex 3D curves. 
# A common simplified way to model them in code is to define a spline path 
# that transitions from the helix end to a vertical loop.

def create_hook(start_point, is_top=True):
    """
    Creates a hook geometry attached to a specific point.
    This uses a spline to approximate the transition from the coil to the center loop.
    """
    # Define key points relative to the start point
    # Start point is on the helix circumference
    x0, y0, z0 = start_point
    
    # Direction factor based on top or bottom hook
    dir_factor = 1 if is_top else -1
    
    # The hook needs to bend from the coil tangent towards the center axis,
    # then form a loop.
    
    # 1. Transition Point: Move towards center and up
    p1 = (0, y0, z0 + (dir_factor * hook_height * 0.3))
    
    # 2. Top/Bottom of the loop (on the axis)
    p2 = (0, y0 - (coil_radius * 1.0), z0 + (dir_factor * hook_height * 0.8)) # Outer edge of loop
    
    # 3. Closing the loop
    # We will create a path that goes: Start -> Center Axis Transition -> Loop -> Back to Axis
    
    # Let's try a simpler approach: A path composed of segments to form the 'question mark' shape
    # We construct a path starting from the wire end
    
    wp = cq.Workplane("XY")
    
    if is_top:
        # Constructing the top hook
        # Assuming the helix ends at a certain angle, we need to continue tangent
        # For simplicity in this procedural generation, we will approximate a "Machine Hook"
        # 1. Curve up and in
        # 2. 3/4 Circle loop
        
        # Center of the hook loop
        loop_center_z = z0 + hook_height/2.0
        
        # Create a path for the hook
        # This is tricky without exact tangency, so we use a spline through points
        path_pts = [
            (x0, y0, z0),                                       # Start at coil end
            (x0*0.8, y0, z0 + dir_factor * wire_diameter),      # Lift off
            (0, y0, z0 + dir_factor * hook_height * 0.4),       # Move to center
            (0, y0 + coil_radius, loop_center_z),               # Top/Bottom of loop arc
            (0, y0 - coil_radius*0.2, loop_center_z)            # End of loop (approx)
        ]
        
        # To make a proper ring, we often just make a torus and a connecting bend.
        # Let's try a spline sweep approach.
        path = cq.Workplane("XY").spline(path_pts, includeCurrent=False)
        
    else:
        # Bottom hook (mirrored logic essentially)
        loop_center_z = z0 + hook_height/2.0 # z0 is 0, so this moves down relative to shape if dir is neg, but here z0 is 0
        
        path_pts = [
            (x0, y0, z0),
            (x0*0.8, y0, z0 + dir_factor * wire_diameter),
            (0, y0, z0 + dir_factor * hook_height * 0.4),
            (0, y0 + coil_radius, z0 + dir_factor * hook_height * 0.7), 
            (0, y0 - coil_radius*0.2, z0 + dir_factor * hook_height * 0.7) 
        ]
        path = cq.Workplane("XY").spline(path_pts, includeCurrent=False)

    return path

# --- Alternative Hook Construction: Torus + Bend ---
# The spline method is often unstable. A constructive geometry approach is more robust.

def make_hook_solid(z_start, top=True):
    sign = 1 if top else -1
    
    # 1. Vertical Bend (Transition from Helix Pitch to Vertical)
    # We assume the helix ends at (r, 0, z)
    
    # Create the loop (The "eye" of the hook)
    # It is a partial torus centered above the spring
    loop_center_z = z_start + (sign * (hook_height * 0.6))
    
    # Create the loop torus
    # We orient it on the YZ plane (vertical ring)
    loop = (
        cq.Workplane("YZ")
        .workplane(offset=0) # X=0
        .center(0, loop_center_z)
        .circle(coil_radius) # Radius of the ring
        .circle(coil_radius - wire_diameter) # Inner radius to make it a tube? No, sweep is better.
    )
    # Actually, simpler to make a torus directly
    loop_solid = (
        cq.Workplane("XY")
        .transformed(rotate=(0, 90, 0)) # Rotate to stand up
        .center(loop_center_z, 0)       # Position
        .torus(coil_radius, wire_diameter/2.0)
    )
    
    # We only want roughly 3/4 of this torus or a full ring. 
    # Extension springs usually have a 3/4 loop or full loop.
    # Let's assume a full loop for robustness, but we need to cut the gap or connect it.
    
    # 2. The Connector (Bend from Helix to Loop)
    # The helix ends at X=radius, Y=0. The Loop is centered at X=0.
    # We need a sweep from (r, 0, z_start) to (0, r, loop_bottom) or similar.
    
    # Let's simply sweep a path for the hook to ensure connectivity
    # Points for spline: Start (Helix End) -> Mid (Curve in) -> End (Top of loop)
    
    p0 = (coil_radius, 0, z_start)
    p1 = (coil_radius, 0, z_start + sign * wire_diameter) # Go slightly up/down
    p2 = (0, 0, z_start + sign * hook_height * 0.5) # Center axis
    
    # Define the hook arc in the YZ plane (or XZ depending on orientation)
    # Let's make a semi-circle path on top
    
    path_plane = cq.Workplane("XZ").workplane(offset=0)
    
    if top:
        # Top Hook
        # 1. Bend from helix end to center
        bend_path = (
            cq.Workplane("XY")
            .moveTo(coil_radius, 0)
            .spline([(0, 0, hook_height/2.0)], tangents=[(0,0,1), (-1,0,0)], includeCurrent=True)
            .val()
        )
        # 2. The loop
        # Arc centered at (0, 0, hook_height/2 + radius)
        loop_path = (
             cq.Workplane("YZ")
             .workplane(centerOption="ProjectedOrigin", origin=(0, 0, hook_height/2.0))
             .threePointArc((0, coil_radius*2, hook_height/2.0 + coil_radius*2), (0, 0, hook_height/2.0 + coil_radius*2)) # Half circle
        )
        # Since joining separate paths is hard in CQ, let's just model the "Bend" and "Loop" separately and union them.
        
        # Solid 1: The Bend
        # Sweep circle along bend_path
        # We need to orient the profile correctly at the start of the path
        # At start of bend_path (coil_radius, 0, 0), tangent is roughly Up/Z.
        # Helix ends tangent (0, 1, pitch/circumf). 
        
        # Simplified: Just create a parametric curve for the whole hook
        hook_path = (
            cq.Workplane("XY")
            .moveTo(coil_radius, 0)
            .spline(
                [
                    (coil_radius*0.8, 0, wire_diameter),  # Transition
                    (0, 0, hook_height * 0.4),            # Center
                    (-coil_radius, 0, hook_height * 0.8), # Top loop far side
                    (0, 0, hook_height * 1.2)             # Loop return
                ],
                includeCurrent=True
            )
        )
        
        # Shift the path to the top of the spring
        path_wire = hook_path.val().translate((0,0, total_height))
        
        # Profile
        profile = cq.Workplane("XZ").center(coil_radius, total_height).circle(wire_diameter/2.0)
        top_hook = profile.sweep(path_wire, isFrenet=True)
        
        return top_hook

    else:
        # Bottom Hook (Mirrored logic)
        hook_path = (
            cq.Workplane("XY")
            .moveTo(coil_radius, 0)
            .spline(
                [
                    (coil_radius*0.8, 0, -wire_diameter),   
                    (0, 0, -hook_height * 0.4),           
                    (-coil_radius, 0, -hook_height * 0.8), 
                    (0, 0, -hook_height * 1.2)            
                ],
                includeCurrent=True
            )
        )
        
        path_wire = hook_path.val() # Starts at 0,0,0
        
        # Profile at 0,0,0 (Start of helix)
        profile = cq.Workplane("XZ").center(coil_radius, 0).circle(wire_diameter/2.0)
        bottom_hook = profile.sweep(path_wire, isFrenet=True)
        
        return bottom_hook

# --- Refined Hook Generation using Geometric Primitives ---
# The spline sweep often twists (Frenet frame issues). 
# A cleaner visual result for this prompt is often achieved by combining a partial helix and tori.

def create_machine_hook(z_pos, is_top):
    """
    Creates a 'machine hook' style loop.
    """
    sign = 1 if is_top else -1
    
    # 1. The Bend: 90 degree bend from helix radius to center
    # We approximate this with a quarter torus
    bend_radius = coil_radius
    bend = (
        cq.Workplane("XY")
        .transformed(rotate=(90, 0, 0)) # YZ plane
        .center(0, z_pos)               # Center at helix end height
        .moveTo(bend_radius, 0)         
    )
    
    # Since aligning separate primitives is complex, we will stick to the parametric path method
    # but refine the points to look more like the reference image (Crossover hooks).
    
    pts = []
    
    if is_top:
        # Start at helix end: (coil_radius, 0, z_pos)
        # End of helix tangent is roughly (0, 1, pitch)
        
        # 1. Rise and curve in
        pts.append((coil_radius, 0, z_pos))
        pts.append((coil_radius * 0.1, 0, z_pos + hook_height * 0.4))
        
        # 2. The loop (approximate circular shape on YZ plane)
        # Center of loop roughly at (0, 0, z_pos + hook_height * 0.8)
        loop_z = z_pos + hook_height * 0.8
        pts.append((-coil_radius * 0.8, 0, loop_z))
        pts.append((0, 0, z_pos + hook_height * 1.2)) # Top of loop
        pts.append((coil_radius * 0.6, 0, loop_z)) # Coming down
        
    else:
        # Bottom
        pts.append((coil_radius, 0, z_pos))
        pts.append((coil_radius * 0.1, 0, z_pos - hook_height * 0.4))
        
        loop_z = z_pos - hook_height * 0.8
        pts.append((-coil_radius * 0.8, 0, loop_z))
        pts.append((0, 0, z_pos - hook_height * 1.2)) 
        pts.append((coil_radius * 0.6, 0, loop_z))

    path_spline = cq.Workplane("XY").spline(pts, includeCurrent=False).val()
    
    # Create profile at the start point
    # We define a plane normal to the start of the spline
    profile = (
        cq.Workplane("XY")
        .center(pts[0][0], pts[0][1])
        .workplane(offset=pts[0][2])
        .transformed(rotate=(0, 90, 0)) # Rotate to be vertical (XZ plane-ish)
        .circle(wire_diameter / 2.0)
    )
    
    # Adjust profile orientation slightly if needed, but simple circle is usually forgiving
    # For better robustness, construct profile perpendicular to path tangent
    
    return profile.sweep(path_spline, isFrenet=True)

# Generate Hooks
# Note: The helix function ends at angle t*2pi. 
# Our helix has 'num_active_coils' turns.
# If num_active_coils is integer, it starts at (r,0,0) and ends at (r,0,total_height).

top_hook = create_machine_hook(total_height, is_top=True)
bottom_hook = create_machine_hook(0, is_top=False)

# --- Assembly ---
result = main_coil.union(top_hook).union(bottom_hook)