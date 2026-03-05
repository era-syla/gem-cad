import cadquery as cq
import math

# --- Parameters ---
length = 120.0          # Total length of the spike
base_height = 25.0      # Height of the vertical base
thickness = 8.0         # Thickness of the material
curvature_sag = 15.0    # Vertical drop of the curve (controls arc shape)
num_teeth = 10          # Number of serrations
connector_len = 6.0     # Length of the rear mounting tab
connector_scale = 0.6   # Size of connector relative to base face
chamfer_val = 1.5       # Chamfer size for the connector

# --- Geometry Construction ---

# 1. Define Control Points
# Tip is at (0,0)
# Base bottom is at (length, -curvature_sag)
# This creates the downward slope. 
# We define a midpoint for the bottom arc to make it concave (curving inward).
p_tip = (0, 0)
p_base_bot = (length, -curvature_sag)
# Midpoint slightly higher than the linear chord creates concavity
p_mid_bot = (length * 0.5, (-curvature_sag * 0.5) + (curvature_sag * 0.15))

# 2. Generate Teeth Profile
# The top edge follows a "spine" curve which is convex.
p_base_top_y = -curvature_sag + base_height
teeth_points = [p_tip]

for i in range(1, num_teeth + 1):
    t = i / num_teeth
    x_curr = length * t
    
    # Spine Curve Logic (Convex Arch)
    # Linear interpolation between Tip Y(0) and Base Top Y
    y_linear = t * p_base_top_y
    # Add sine wave for convex bulge
    y_arch = (curvature_sag * 0.4) * math.sin(t * math.pi)
    y_peak = y_linear + y_arch
    
    # Tooth Depth Logic (Teeth get larger towards base)
    current_tooth_depth = 2.0 + (t * 5.0)
    y_root = y_peak - current_tooth_depth
    
    # Append points
    # 1. The Peak of the current tooth
    teeth_points.append((x_curr, y_peak))
    
    # 2. The Valley (Root) start of the next tooth
    # We don't add a root after the last tooth, as it connects to the back wall
    if i < num_teeth:
        teeth_points.append((x_curr, y_root))

# 3. Create 2D Profile
profile = (
    cq.Workplane("XY")
    .moveTo(*p_tip)
    .polyline(teeth_points)             # Draw the serrated top
    .lineTo(*p_base_bot)                # Draw the vertical back face
    .threePointArc(p_mid_bot, p_tip)    # Draw the curved bottom edge
    .close()
)

# 4. Extrude Main Body
main_body = profile.extrude(thickness)

# 5. Create Connector Tab
# Located on the flat back face at X = length
connector = (
    main_body
    .faces(">X")                        # Select back face
    .workplane()
    .rect(thickness * 0.7, base_height * connector_scale)
    .extrude(connector_len)
)

# 6. Final Detailing (Chamfer the connector)
result = (
    connector
    .faces(">X")                        # Select the new end face
    .edges()
    .chamfer(chamfer_val)
)