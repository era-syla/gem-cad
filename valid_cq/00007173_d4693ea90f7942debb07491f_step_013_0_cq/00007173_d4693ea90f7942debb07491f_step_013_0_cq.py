import cadquery as cq
import math

def button_head_socket_screw(
    thread_diameter=5.0,   # M5
    thread_pitch=0.8,      # Standard pitch for M5
    length=20.0,           # Threaded length
    head_diameter=9.5,     # Typical for ISO 7380 M5
    head_height=2.75,      # Typical for ISO 7380 M5
    socket_size=3.0,       # Hex key size (SW)
    socket_depth=1.56      # Socket depth
):
    """
    Generates a simplified ISO 7380 Button Head Socket Cap Screw.
    Threads are simulated as cosmetic annular rings to keep performance high
    while maintaining visual fidelity.
    """
    
    # 1. Create the Head
    # The head of a button screw is essentially a sphere segment intersected with a cylinder, 
    # but a simple arc revolution works best for parametric control.
    
    # Calculate radius of the sphere that would form this head height and diameter
    # r^2 = (d/2)^2 + (r-h)^2
    # r^2 = d^2/4 + r^2 - 2rh + h^2
    # 2rh = d^2/4 + h^2
    # r = (d^2/4 + h^2) / (2h)
    
    d_half = head_diameter / 2.0
    sphere_radius = (d_half**2 + head_height**2) / (2 * head_height)
    
    # Create the profile for revolution
    # We place the top of the head at z=head_height and the base at z=0
    head = (
        cq.Workplane("XZ")
        .moveTo(0, head_height)
        .lineTo(0, 0)
        .lineTo(d_half, 0)
        .radiusArc((0, head_height), -sphere_radius) # Create the dome
        .close()
        .revolve()
    )
    
    # 2. Create the Hex Socket
    head = (
        head.faces(">Z")
        .workplane()
        .polygon(6, socket_size * 2 / math.sqrt(3)) # Convert flat-to-flat to circumradius
        .cutBlind(-socket_depth)
    )
    
    # 3. Create the Shank (Bolt Shaft)
    # We'll chamfer the tip slightly for realism
    chamfer_len = 0.5
    
    shank = (
        cq.Workplane("XY")
        .circle(thread_diameter / 2.0)
        .extrude(-length)
    )
    
    # Add chamfer to the end of the bolt
    shank = shank.edges("<Z").chamfer(chamfer_len)
    
    # 4. Create Cosmetic Threads
    # Instead of actual helical threads (computationally expensive), we make rings.
    
    # Define thread cutter shape
    # 60-degree V-thread standard profile approximation
    thread_depth = 0.61343 * thread_pitch 
    
    # We create a tool to cut the threads. 
    # Since we can't easily pattern a cut operation along a path in a single step with 
    # just basic CQ, we can construct the "negative" of the threads and cut it, 
    # or make the shank slightly smaller and fuse rings.
    # Let's use the cut method for better visual accuracy.
    
    num_threads = int((length - chamfer_len) / thread_pitch)
    
    # Create the cutter profile
    # It's a triangle pointing inward
    cutter = (
        cq.Workplane("XZ", origin=(0, 0, -thread_pitch))
        .moveTo(thread_diameter/2.0, 0)
        .lineTo(thread_diameter/2.0 - thread_depth, -thread_pitch/2.0)
        .lineTo(thread_diameter/2.0, -thread_pitch)
        .close()
        .revolve()
    )
    
    # Union all cutters into one object (much faster than individual cuts)
    cutters = cutter
    for i in range(1, num_threads):
        # Offset each cutter
        cutters = cutters.union(cutter.translate((0, 0, -i * thread_pitch)))
    
    # Cut the threads from the shank
    shank_threaded = shank.cut(cutters)
    
    # 5. Assemble Head and Shank
    result = head.union(shank_threaded)
    
    return result

# Generate the model
result = button_head_socket_screw()