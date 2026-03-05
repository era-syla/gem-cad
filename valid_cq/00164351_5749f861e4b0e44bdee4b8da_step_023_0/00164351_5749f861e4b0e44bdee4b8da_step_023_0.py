import cadquery as cq
import math

# --- Parameters ---
thickness = 6.0          # Plate thickness
lobe_radius = 15.0       # Radius of the rounded corners
hole_diameter = 8.0      # Diameter of mounting holes
cut_radius = 100.0       # Radius of the concave edge cuts

# Coordinates of the three main lobes
p_top = (0, 50)
p_right = (55, -40)
p_left = (-55, -40)
lobe_centers = [p_top, p_right, p_left]

# Coordinate of the central hole
p_center = (0, 0)

# --- Helper Function ---
def calculate_cut_center(p1, p2, r_lobe, r_cut):
    """
    Calculates the center of a cutting circle that is tangent to two lobe circles.
    Returns the center point that creates an external concave cut.
    """
    x1, y1 = p1
    x2, y2 = p2
    
    # Distance between lobe centers
    dx = x2 - x1
    dy = y2 - y1
    d = math.hypot(dx, dy)
    
    # Distance from lobe center to cut circle center
    # The cut circle is tangent to the lobe circle, so distance is sum of radii
    R = r_lobe + r_cut
    
    # Calculate intersection of two circles of radius R centered at p1 and p2
    if d > 2 * R:
        raise ValueError("Lobe circles are too far apart for the cut radius.")
        
    a = d / 2.0
    h = math.sqrt(R**2 - a**2)
    
    # Midpoint of the chord
    x0 = x1 + a * (dx / d)
    y0 = y1 + a * (dy / d)
    
    # Perpendicular offsets to find the two intersection points
    rx = -dy * (h / d)
    ry = dx * (h / d)
    
    c1 = (x0 + rx, y0 + ry)
    c2 = (x0 - rx, y0 - ry)
    
    # Heuristic: Pick the center further from the origin (approx part centroid)
    # to ensure the cut comes from the "outside"
    if math.hypot(*c1) > math.hypot(*c2):
        return c1
    return c2

# --- 3D Modeling ---

# 1. Create the base structure
# Start with a triangle connecting the centers to fill the core
result = cq.Workplane("XY").polyline(lobe_centers).close().extrude(thickness)

# Union the cylindrical lobes at the corners
for pt in lobe_centers:
    lobe = cq.Workplane("XY").center(*pt).circle(lobe_radius).extrude(thickness)
    result = result.union(lobe)

# 2. Cut the concave sides
# Pairs of points defining the edges: (Top, Right), (Right, Left), (Left, Top)
edges = [(p_top, p_right), (p_right, p_left), (p_left, p_top)]

for p1, p2 in edges:
    # Calculate position for the cutting cylinder
    c_center = calculate_cut_center(p1, p2, lobe_radius, cut_radius)
    
    # Create and subtract the cutter
    cutter = cq.Workplane("XY").center(*c_center).circle(cut_radius).extrude(thickness)
    result = result.cut(cutter)

# 3. Drill the holes
# Combine all hole locations
hole_points = lobe_centers + [p_center]

# Cut holes through the top face
result = result.faces(">Z").workplane().pushPoints(hole_points).hole(hole_diameter)