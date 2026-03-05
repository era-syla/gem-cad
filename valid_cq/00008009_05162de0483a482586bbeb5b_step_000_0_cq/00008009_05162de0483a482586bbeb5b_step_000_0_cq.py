import cadquery as cq

# Parameters for the bellows/ribbed cylinder
radius = 50.0       # Radius of the main cylinder
rib_radius = 2.0    # Radius of the circular ribs (protrusion size)
total_height = 60.0 # Total height of the object
num_ribs = 6        # Number of ribbed sections
wall_thickness = 2.0 # Thickness of the outer shell (if hollow, but looks solid)

# Calculate derived dimensions
# Each rib section consists of a cycle. 
# It looks like a stack of toruses or a sine wave revolved.
# Let's model it as a solid cylinder with toroidal cuts or toroidal additions.
# Based on the sharp creases between layers, it looks like stacked disks with rounded profiles.

section_height = total_height / num_ribs

# Method: Create a profile wire and revolve it.
# The profile is a vertical line on the inside (or axis) and a wavy line on the outside.

def create_ribbed_cylinder():
    # Define the path for the revolution profile
    # We will draw half the cross-section on the XZ plane
    
    # Start at the top center
    # Actually, simpler to just revolve a profile offset from the Z axis.
    
    # Let's define the outer profile points
    # The profile consists of arcs.
    # Looking closely, it looks like convex circular arcs stacked on top of each other.
    
    # Radius of the cylinder at the "valleys"
    inner_r = radius - rib_radius
    # Radius of the cylinder at the "peaks"
    outer_r = radius + rib_radius
    
    # We will build the profile as a list of edges
    path = cq.Workplane("XZ").moveTo(outer_r, 0)
    
    # Draw the wavy outer wall
    # We iterate upwards. Let's start from bottom (Z=0) to top (Z=total_height)
    # The current Z position
    current_z = 0.0
    
    # Move to starting point at bottom outer edge
    path = path.moveTo(inner_r, 0)
    
    # Create the ribbed profile
    # The profile seems to be a sequence of outward bumps.
    # Let's assume each bump is a 180 degree arc or close to it.
    # If section height is h, and we want a round bump, the radius of the arc is roughly h/2?
    # Or maybe it's shallower. Let's try a simple arc.
    
    # Let's redefine the approach:
    # It looks like a stack of coins with rounded edges, or just a sine wave.
    # A 3-point arc for each rib seems appropriate.
    # Start: (inner_r, z), Mid: (outer_r, z + h/2), End: (inner_r, z + h)
    
    for i in range(num_ribs):
        start_pt = (inner_r, current_z)
        mid_pt = (outer_r, current_z + section_height/2.0)
        end_pt = (inner_r, current_z + section_height)
        
        # If it's the first point, we are already there (or need to move there)
        if i == 0:
            path = path.moveTo(*start_pt)
            
        path = path.threePointArc(mid_pt, end_pt)
        current_z += section_height
        
    # Close the shape to make a solid
    # Draw line to top center (or axis), down axis, back to start
    path = path.lineTo(0, total_height).lineTo(0, 0).close()
    
    # Revolve the profile around the Z axis
    result = path.revolve()
    
    return result

# Execute the creation
result = create_ribbed_cylinder()

# Alternative approach if the top/bottom are flat disks:
# The image shows flat top and bottom surfaces. The revolved profile above creates this.
# The `lineTo(0, total_height)` closes the top flat face.
# The `lineTo(0, 0)` closes the axis.
# The `close()` connects back to `(inner_r, 0)` creating the bottom flat face.