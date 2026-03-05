import cadquery as cq
import math

def wood_screw(
    length=30.0,
    head_diameter=8.0,
    head_angle=90.0,
    shank_diameter=4.0,
    thread_diameter=5.0,
    thread_pitch=2.5,
    drive_size=2.5,  # Width of square drive
    drive_depth=2.5
):
    """
    Generates a countersunk wood screw with a square (Robertson) drive.
    """
    
    # --- 1. Create the base shaft and head ---
    
    # Calculate head height based on diameter and angle
    # tan(angle/2) = (head_diam/2) / height
    head_height = (head_diameter / 2) / math.tan(math.radians(head_angle / 2))
    
    # Total shaft length excluding the head taper
    shaft_length = length - head_height
    
    # Create the main body (Head + Cylindrical Shaft)
    # We start drawing on the XZ plane to revolve
    
    pts = [
        (0, 0),
        (head_diameter / 2, 0),
        (shank_diameter / 2, -head_height),
        (shank_diameter / 2, -(length - shank_diameter)), # Taper start point
        (0, -length) # Tip point
    ]
    
    # Create the solid body by revolving the profile
    body = (
        cq.Workplane("XZ")
        .polyline(pts)
        .close()
        .revolve()
    )

    # --- 2. Create the Threads ---
    
    # We will sweep a thread profile along a helix
    
    # Define helical path properties
    thread_length = shaft_length - (shank_diameter) # Leave some room for the tip taper
    num_turns = thread_length / thread_pitch
    
    # Create the helix path
    path = cq.Workplane("XY").transformed(offset=(0,0,-head_height)).parametricCurve(
        lambda t: (
            (shank_diameter / 2) * math.cos(t * num_turns * 2 * math.pi),
            (shank_diameter / 2) * math.sin(t * num_turns * 2 * math.pi),
            -t * thread_length
        )
    )

    # Define the thread profile
    # A triangular profile for a wood screw
    thread_depth = (thread_diameter - shank_diameter) / 2
    
    # We create the profile perpendicular to the helix start
    profile = (
        cq.Workplane("XZ")
        .transformed(offset=(shank_diameter/2, 0, -head_height))
        # Rotate to align with helix pitch angle roughly
        .transformed(rotate=(0, 0, 0)) 
        .polyline([
            (0, thread_pitch * 0.1), # Inner top
            (thread_depth, -thread_pitch / 2), # Outer tip
            (0, -thread_pitch * 0.9), # Inner bottom
        ])
        .close()
    )
    
    # Sweep the profile along the path
    # frenet=True helps keep orientation correct along the helix
    thread = profile.sweep(path, isFrenet=True, transition='round')
    
    # Combine thread with body
    # Note: Unioning complex sweeps can sometimes be slow or fragile in kernels.
    # In this specific visual case, the sweep adds material.
    result_body = body.union(thread)

    # --- 3. Create the Square Drive (Robertson) ---
    
    # Create the square profile on the top face
    result_body = (
        result_body
        .faces(">Z")
        .workplane()
        .rect(drive_size, drive_size)
        .cutBlind(-drive_depth)
    )
    
    # Optional: Add a small chamfer to the drive opening for realism
    # Getting the specific edges can be tricky, so we rely on the last cut operation
    try:
        result_body = (
            result_body.faces(">Z").edges("%SQUARE") # Select edges of the square cut
            .chamfer(0.2)
        )
    except:
        pass # Skip if selection fails, cosmetic only

    return result_body

# Generate the model
result = wood_screw()

# Export is not requested, but standard practice in some viewers
# if 'show_object' in globals():
#     show_object(result)