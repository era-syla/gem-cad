import cadquery as cq
import math

# --- Dimensions ---
length = 240.0         # Total length of the channel
width = 42.0           # Outer width
height = 42.0          # Outer height
thickness = 2.5        # Wall thickness

# --- Pattern Parameters ---
pitch = 32.0           # Distance between repeating pattern units
center_hole_dia = 12.0 # Diameter of the large center hole
sat_hole_dia = 3.5     # Diameter of the satellite holes
mid_hole_dia = 3.5     # Diameter of the intermediate holes
sat_radius = 10.0      # Radius of the satellite hole circle
num_satellites = 8     # Number of satellite holes

# --- 1. Base Geometry: U-Channel ---
# Define the U-profile on the XY plane.
# The Web is at Y=0. The flanges extend towards +Y.
# The profile is centered on the X-axis.
pts = [
    (-width/2, height),
    (-width/2, 0),
    (width/2, 0),
    (width/2, height),
    (width/2 - thickness, height),
    (width/2 - thickness, thickness),
    (-width/2 + thickness, thickness),
    (-width/2 + thickness, height)
]

# Create the solid by extruding along Z
result = cq.Workplane("XY").polyline(pts).close().extrude(length)

# --- 2. Pattern Generation Helper ---
def get_pattern_points(face_type):
    """
    Generates lists of (x, y) points for the holes on a 2D workplane.
    For 'web': x is transverse, y is longitudinal (Z).
    For 'flange': x is longitudinal (Z), y is transverse (Y).
    """
    c_pts, s_pts, m_pts = [], [], []
    
    # Start the pattern offset from the bottom (Z=0)
    current_z = pitch / 2.0
    
    while current_z < length:
        # Determine center coordinates based on face type
        if face_type == 'web':
            # Centered on width (x=0), positioned at current_z
            center_pos = (0, current_z)
            mid_pos = (0, current_z + pitch / 2.0)
        else: # flange
            # Positioned at current_z, centered on flange height
            center_pos = (current_z, height / 2.0)
            mid_pos = (current_z + pitch / 2.0, height / 2.0)

        # Add Main Hole
        c_pts.append(center_pos)
        
        # Add Satellite Holes
        for i in range(num_satellites):
            angle = math.radians(i * (360.0 / num_satellites))
            dx = sat_radius * math.cos(angle)
            dy = sat_radius * math.sin(angle)
            s_pts.append((center_pos[0] + dx, center_pos[1] + dy))
            
        # Add Intermediate Hole (if it fits)
        if (current_z + pitch / 2.0) < length:
            m_pts.append(mid_pos)
            
        current_z += pitch
        
    return c_pts, s_pts, m_pts

# --- 3. Cut Holes on Web (Bottom Face) ---
# Select the bottom face (Y=0, Normal -Y)
# Use ProjectedOrigin to set (0,0) at the geometric center of the projection
web_c, web_s, web_m = get_pattern_points('web')

result = (
    result.faces("<Y")
    .workplane(centerOption="ProjectedOrigin")
    .pushPoints(web_c).circle(center_hole_dia / 2).cutBlind(-thickness * 2)
    .pushPoints(web_s).circle(sat_hole_dia / 2).cutBlind(-thickness * 2)
    .pushPoints(web_m).circle(mid_hole_dia / 2).cutBlind(-thickness * 2)
)

# --- 4. Cut Holes on Flanges ---
# Generate points for side faces
flange_c, flange_s, flange_m = get_pattern_points('flange')

# Left Flange (Face <X)
result = (
    result.faces("<X")
    .workplane(centerOption="ProjectedOrigin")
    .pushPoints(flange_c).circle(center_hole_dia / 2).cutBlind(-thickness * 2)
    .pushPoints(flange_s).circle(sat_hole_dia / 2).cutBlind(-thickness * 2)
    .pushPoints(flange_m).circle(mid_hole_dia / 2).cutBlind(-thickness * 2)
)

# Right Flange (Face >X)
result = (
    result.faces(">X")
    .workplane(centerOption="ProjectedOrigin")
    .pushPoints(flange_c).circle(center_hole_dia / 2).cutBlind(-thickness * 2)
    .pushPoints(flange_s).circle(sat_hole_dia / 2).cutBlind(-thickness * 2)
    .pushPoints(flange_m).circle(mid_hole_dia / 2).cutBlind(-thickness * 2)
)

# --- 5. Miter Cut ---
# Create a 45-degree cut at the top end of the channel.
# The web (Y=0) remains full length, the open side (Y=height) is cut shorter.
# We define a triangular profile on the YZ plane to subtract from the solid.
cutter_profile = [
    (0, length),               # Point at Web tip
    (height, length),          # Point at top corner (to be removed)
    (height, length - height)  # Point down the flange
]

# Create the cutter solid (extruded in X to cover the width)
cutter = (
    cq.Workplane("YZ")
    .polyline(cutter_profile)
    .close()
    .extrude(width + 10, both=True)
)

# Apply the cut
result = result.cut(cutter)