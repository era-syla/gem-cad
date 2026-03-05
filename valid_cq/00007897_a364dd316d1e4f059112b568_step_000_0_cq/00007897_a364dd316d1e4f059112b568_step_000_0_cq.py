import cadquery as cq

# Parametric dimensions for the lightbulb
bulb_radius = 30.0
neck_length = 25.0
neck_radius = 15.0
base_radius = 12.0
base_height = 18.0
contact_radius = 6.0
contact_height = 2.0
wall_thickness = 1.0  # For hollowing out (optional, but realistic)

# 1. The Glass Bulb (Sphere)
# Create a sphere and move it up so the neck connects cleanly
bulb_sphere = cq.Workplane("XY").sphere(bulb_radius).translate((0, 0, bulb_radius + neck_length))

# 2. The Neck (Loft or Smooth Transition)
# We need to transition from the sphere radius down to the base radius.
# A loft is a good way to handle the curve, but a revolved spline is often smoother for lightbulbs.
# Let's use a Revolve operation to create the main profile (Bulb + Neck).

def lightbulb_profile(bulb_r, neck_r, neck_l, base_r, base_h):
    # Calculate key points
    # Top of sphere (relative to center of sphere)
    sphere_center_z = neck_l + base_h
    
    # Create the profile on the XZ plane
    # Start at the bottom of the neck (top of the base)
    p = cq.Workplane("XZ").moveTo(base_r, base_h)
    
    # Draw line up slightly for the neck straight section
    p = p.lineTo(neck_r, base_h + 5)
    
    # Create a spline curve to the widest part of the sphere
    # Control points help define the "S" curve shape of a lightbulb neck
    p = p.spline([(bulb_r, sphere_center_z)], 
                 tangents=[(0, 1), (0, 1)], 
                 includeCurrent=True)
    
    # Complete the top hemisphere arc
    p = p.radiusArc((0, sphere_center_z + bulb_r), bulb_r)
    
    # Close the shape to the axis
    p = p.lineTo(0, base_h)
    p = p.close()
    
    return p

# Create the glass body by revolving the profile
glass_body = (
    lightbulb_profile(bulb_radius, neck_radius, neck_length, base_radius, base_height)
    .revolve()
)

# 3. The Metal Base (Threaded Cylinder representation)
# For simplicity and robustness, we'll model rings instead of a true helix thread, 
# as true helix threads can be computationally expensive and tricky in pure constructive geometry.
# However, a stack of toruses or simply a cylinder with grooves works well visually.

base_cylinder = cq.Workplane("XY").circle(base_radius).extrude(base_height)

# Create "threads" by cutting grooves
thread_pitch = 3.0
thread_depth = 1.5
num_threads = int(base_height / thread_pitch) - 1

for i in range(num_threads):
    z_pos = (i + 1) * thread_pitch
    cutter = (
        cq.Workplane("XZ")
        .workplane(offset=z_pos)
        .moveTo(base_radius + 1, 0) # Start outside
        .circle(thread_depth / 2)   # Simple semi-circular groove profile
        .revolve(360, (0,0,0), (0,0,1))
    )
    base_cylinder = base_cylinder.cut(cutter)

# 4. The Electrical Contact (Bottom tip)
insulator = cq.Workplane("XY").circle(base_radius - 1).extrude(2).translate((0, 0, -2))
contact = cq.Workplane("XY").circle(contact_radius).extrude(contact_height).translate((0, 0, -2 - contact_height))
contact = contact.edges(">Z").fillet(1.0) # Round off the contact point

# 5. Assembly
# Combine the glass body and the base.
# The glass body starts at Z = base_height based on the profile logic, but let's ensure overlaps are handled.

# Since the glass profile started at base_height, we just union them.
# The base cylinder is at Z=0 to Z=base_height.
result = glass_body.union(base_cylinder).union(insulator).union(contact)

# Optional: Fillet the transition between glass and metal base for realism
try:
    result = result.edges(cq.selectors.NearestToPointSelector((base_radius, base_height, 0))).fillet(1.0)
except:
    pass # Skip if geometry is too complex for this specific fillet

# Optional: Fillet the very bottom of the threads
try:
    result = result.edges(cq.selectors.NearestToPointSelector((base_radius, 0, 0))).fillet(0.5)
except:
    pass

# Export or Display
# show_object(result) # Only used in CQ-editor environment