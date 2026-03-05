import cadquery as cq

# --- Parameters ---
# Dimensions estimated from the image aspect ratio
length = 200.0         # Total length of the truss structure
width = 25.0           # Width of the truss (constant)
h_start = 25.0         # Height at the narrow end (left)
h_end = 65.0           # Height at the tall end (right)
num_bays = 7           # Number of truss bays/sections
tube_size = 2.5        # Thickness of the square tubing

# --- Helper Function ---
def create_strut(p1, p2, thickness):
    """
    Creates a square tube strut connecting two 3D points.
    Uses a sweep operation along the path between points.
    """
    v1 = cq.Vector(p1)
    v2 = cq.Vector(p2)
    diff = v2 - v1
    dist = diff.Length
    
    # Avoid creating zero-length members
    if dist < 0.001:
        return None

    # Define a local plane at the start point, perpendicular to the strut axis
    # CadQuery automatically calculates an appropriate x_dir for the plane
    plane = cq.Plane(origin=v1, normal=diff)
    
    # Define the path as a straight line wire between the two points
    path = cq.Workplane().polyline([v1, v2])
    
    # Create a square profile on the plane and sweep it along the path
    # .val() extracts the underlying Solid object for efficient storage
    return cq.Workplane(plane).rect(thickness, thickness).sweep(path).val()

# --- Geometry Generation ---

# 1. Calculate Node Coordinates
# We generate "stations" along the length of the truss.
# Each station has 4 nodes: Bottom-Left, Bottom-Right, Top-Right, Top-Left.
stations = []

for i in range(num_bays + 1):
    # Normalized position (0.0 to 1.0)
    t = i / num_bays
    
    # Calculate X position
    x = t * length
    
    # Calculate Height at this position (Linear Interpolation)
    h = h_start + t * (h_end - h_start)
    
    # Define coordinates (Z is up, Y is width, X is length)
    bl = (x, 0, 0)        # Bottom Left
    br = (x, width, 0)    # Bottom Right
    tr = (x, width, h)    # Top Right
    tl = (x, 0, h)        # Top Left
    
    stations.append([bl, br, tr, tl])

# List to collect all generated solid members
members = []

# 2. Build Structure
for i in range(len(stations)):
    curr = stations[i]
    
    # --- Cross-Section Frames ---
    # Vertical Struts at the current station
    members.append(create_strut(curr[0], curr[3], tube_size)) # Left Vertical
    members.append(create_strut(curr[1], curr[2], tube_size)) # Right Vertical
    
    # Horizontal Struts (Rungs) at the current station
    members.append(create_strut(curr[0], curr[1], tube_size)) # Bottom Rung
    members.append(create_strut(curr[3], curr[2], tube_size)) # Top Rung

    # --- Longitudinal & Bracing ---
    # Connect current station to the next station
    if i < len(stations) - 1:
        next_s = stations[i+1]
        
        # Longitudinal Chords (The 4 main rails)
        members.append(create_strut(curr[0], next_s[0], tube_size)) # Bottom Left Chord
        members.append(create_strut(curr[1], next_s[1], tube_size)) # Bottom Right Chord
        members.append(create_strut(curr[2], next_s[2], tube_size)) # Top Right Chord
        members.append(create_strut(curr[3], next_s[3], tube_size)) # Top Left Chord
        
        # X-Bracing Patterns
        
        # Left Side Face X-Bracing
        members.append(create_strut(curr[0], next_s[3], tube_size)) # BL -> Next TL
        members.append(create_strut(curr[3], next_s[0], tube_size)) # TL -> Next BL
        
        # Right Side Face X-Bracing
        members.append(create_strut(curr[1], next_s[2], tube_size)) # BR -> Next TR
        members.append(create_strut(curr[2], next_s[1], tube_size)) # TR -> Next BR
        
        # Top Face X-Bracing
        members.append(create_strut(curr[3], next_s[2], tube_size)) # TL -> Next TR
        members.append(create_strut(curr[2], next_s[3], tube_size)) # TR -> Next TL
        
        # Bottom Face X-Bracing
        members.append(create_strut(curr[0], next_s[1], tube_size)) # BL -> Next BR
        members.append(create_strut(curr[1], next_s[0], tube_size)) # BR -> Next BL

# Filter out any potential None objects
members = [m for m in members if m is not None]

# Combine all individual members into a single Compound object
# This is efficient and treats the assembly as a single geometry entity
compound_solid = cq.Compound.makeCompound(members)

# Return result as a CadQuery Workplane object containing the compound
result = cq.Workplane(obj=compound_solid)