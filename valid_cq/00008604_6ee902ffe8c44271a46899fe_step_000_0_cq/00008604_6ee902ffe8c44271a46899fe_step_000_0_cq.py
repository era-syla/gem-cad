import cadquery as cq

# Parametric dimensions
outer_size = 100.0        # Size of the outer cube frame
inner_size = 50.0         # Size of the inner cube frame
beam_thickness = 5.0      # Thickness of the square beams

# Helper to create a wireframe box (edges only)
def create_wireframe_box(size, thickness):
    # Start with a solid cube
    box = cq.Workplane("XY").box(size, size, size)
    
    # Create the hollow inside to leave walls
    # We do this by cutting a smaller box from the center
    # But wait, the image shows a frame, not a hollow box with thin walls.
    # It's 12 edges.
    
    # Let's try a different approach: Build the frame by cutting faces.
    # Create solid block
    solid = cq.Workplane("XY").box(size, size, size)
    
    # Cut through X
    cut_x = cq.Workplane("YZ").box(size - 2*thickness, size - 2*thickness, size + 10)
    # Cut through Y
    cut_y = cq.Workplane("XZ").box(size - 2*thickness, size + 10, size - 2*thickness)
    # Cut through Z
    cut_z = cq.Workplane("XY").box(size + 10, size - 2*thickness, size - 2*thickness)
    
    frame = solid.cut(cut_x).cut(cut_y).cut(cut_z)
    return frame

# 1. Create the outer cube frame
outer_frame = create_wireframe_box(outer_size, beam_thickness)

# 2. Create the inner cube frame
inner_frame = create_wireframe_box(inner_size, beam_thickness)

# 3. Create diagonal connecting beams
# These connect the corners of the inner cube to the corners of the outer cube.
# We can define a single strut and mirror/rotate it, or construct them parametrically.

connectors = cq.Workplane("XY")

# Calculate geometry for the connector
# It goes from inner corner to outer corner.
# Let's work in one octant (positive x, y, z)
# Inner corner coords (center of beam intersection):
p_inner = inner_size / 2.0
# Outer corner coords:
p_outer = outer_size / 2.0

# Vector from inner to outer corner
vec = (p_outer - p_inner)

# We create a path from inner corner to outer corner
p1 = (p_inner, p_inner, p_inner)
p2 = (p_outer, p_outer, p_outer)

# To make the geometry clean at junctions, we simply loft or sweep a square profile 
# along the diagonal path.
# However, simple boxes rotated appropriately are often more robust.

def create_diagonal_strut(x_factor, y_factor, z_factor):
    # Start point (inner corner offset by beam thickness to avoid overlap clipping issues if needed, 
    # but exact corner to corner is mathematically cleaner for unions)
    start = (p_inner * x_factor, p_inner * y_factor, p_inner * z_factor)
    end = (p_outer * x_factor, p_outer * y_factor, p_outer * z_factor)
    
    # Create a line segment
    path = cq.Workplane("XY").polyline([start, end])
    
    # Create a square profile perpendicular to the path
    # CadQuery's plane creation on path can be tricky for diagonals.
    # An easier way for a simple square beam is to extrude along a normal vector, 
    # or create a box and rotate it.
    
    # Let's use the box and rotate method or construction plane method.
    # Method: Plane defined by the vector.
    
    center_point = ((start[0]+end[0])/2, (start[1]+end[1])/2, (start[2]+end[2])/2)
    diff_vector = (end[0]-start[0], end[1]-start[1], end[2]-start[2])
    length = (diff_vector[0]**2 + diff_vector[1]**2 + diff_vector[2]**2)**0.5
    
    # Normal plane at the center
    plane = cq.Plane(origin=center_point, normal=diff_vector)
    
    # Draw rectangle and extrude both ways
    strut = (cq.Workplane(plane)
             .rect(beam_thickness, beam_thickness)
             .extrude(length / 2.0, both=True))
    
    return strut

# Generate all 8 diagonals
diagonals = []
for x in [-1, 1]:
    for y in [-1, 1]:
        for z in [-1, 1]:
            diagonals.append(create_diagonal_strut(x, y, z))

# 4. Combine all parts
result = outer_frame.union(inner_frame)

for diag in diagonals:
    result = result.union(diag)

# Optional: Filleting edges to match the smooth look in the render
# This can be computationally expensive on complex unions, but improves visual fidelity.
# We select edges that are not effectively infinite lines (vertical/horizontal) to catch junctions
try:
    result = result.edges().fillet(beam_thickness * 0.1)
except Exception:
    # Fallback if filleting fails due to complex geometry intersections
    pass
