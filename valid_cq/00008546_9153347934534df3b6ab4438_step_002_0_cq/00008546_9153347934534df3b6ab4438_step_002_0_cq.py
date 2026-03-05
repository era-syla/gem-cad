import cadquery as cq

# Parameters for the rings
ring_major_radius = 20.0  # Radius from center to the center of the tube
ring_minor_radius = 2.0   # Radius of the tube itself (thickness)

# Define the spacing between the rings
spacing_x = 50.0
spacing_y = 50.0

def create_ring(major_r, minor_r):
    """
    Creates a torus (ring) shape.
    Args:
        major_r: Radius from the center of the torus to the center of the tube.
        minor_r: Radius of the tube itself.
    Returns:
        A CadQuery Workplane object representing the ring.
    """
    # Create a torus directly using the solid creation method
    # Note: cq.Solid.makeTorus takes (major_radius, minor_radius)
    # But often it's easier to sweep a circle. Let's stick to the high-level API.
    # We draw a circle on the XZ plane offset by major_r, then revolve it around Z.
    
    # Method 1: Revolve operation
    return (
        cq.Workplane("XZ")
        .center(major_r, 0)
        .circle(minor_r)
        .revolve(360, (0, 0, 0), (0, 1, 0)) # Revolve around Y axis of the local plane (which is global Z)
        # Actually, let's be more explicit with global axis
        # Center the workplane at (major_r, 0, 0) relative to global, draw circle, revolve around Z
    )

# Let's use a cleaner parametric approach for a single ring
# We draw the cross-section on the XZ plane and revolve it around the Z axis.
single_ring = (
    cq.Workplane("XZ")
    .center(ring_major_radius, 0)
    .circle(ring_minor_radius)
    .revolve(360, (0,0,0), (0,0,1))
)

# Create the assembly of four rings based on the image layout
# The image shows 4 rings arranged somewhat loosely. Let's do a 2x2 grid.
rings = []

# Positions for the 4 rings
positions = [
    (0, 0),
    (spacing_x, 0),
    (0, spacing_y),
    (spacing_x, spacing_y)
]

# Combine all rings into one object
result = cq.Workplane("XY")

for x, y in positions:
    # Translate the base ring to the new position
    current_ring = single_ring.translate((x, y, 0))
    result = result.union(current_ring)

# If you want them separated visually exactly like the image (staggered), 
# we can adjust positions slightly. The image looks like a slight perspective 
# of a 2x2 grid or a rhombus pattern. A 2x2 grid is the most logical CAD representation.
# Let's stick to the unioned result.

# Export or visualization preparation (handled by the environment usually)