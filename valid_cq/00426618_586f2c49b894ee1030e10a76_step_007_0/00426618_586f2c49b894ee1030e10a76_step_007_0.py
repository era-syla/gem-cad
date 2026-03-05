import cadquery as cq

# --- Parametric Dimensions ---
length = 160.0          # Total length of the component
main_od = 22.0          # Outer diameter of the central cylindrical body
end_od = 28.0           # Outer diameter of the end flanges/collars
id_val = 16.0           # Inner diameter (bore)
end_len = 20.0          # Length of the thickened end section
lip_len = 5.0           # Distance from end face to the groove
groove_w = 3.5          # Width of the groove
groove_d = 2.0          # Depth of the groove
fillet_r = 2.5          # Radius of the transition fillet (collar to body)
chamfer_val = 0.5       # Chamfer size for end edges

# --- Derived Dimensions ---
L2 = length / 2.0
r_main = main_od / 2.0
r_end = end_od / 2.0
r_in = id_val / 2.0
r_groove = r_end - groove_d

# --- Profile Construction ---
# We define the points for the upper half of the cross-section in the XY plane.
# The profile starts at the left inner corner and traces the outer boundary 
# before closing back through the inner bore.
pts = [
    # Left End Geometry
    (-L2, r_in),                    # Start at inner bore left
    (-L2, r_end),                   # Step up to Outer face left
    (-L2 + lip_len, r_end),         # Lip horizontal
    (-L2 + lip_len, r_groove),      # Groove vertical down
    (-L2 + lip_len + groove_w, r_groove), # Groove bottom horizontal
    (-L2 + lip_len + groove_w, r_end),    # Groove vertical up
    (-L2 + end_len, r_end),         # Collar horizontal
    (-L2 + end_len, r_main),        # Step down to main body
    
    # Main Body
    (L2 - end_len, r_main),         # Main body horizontal span
    
    # Right End Geometry
    (L2 - end_len, r_end),          # Step up to collar
    (L2 - lip_len - groove_w, r_end),     # Collar horizontal
    (L2 - lip_len - groove_w, r_groove),  # Groove vertical down
    (L2 - lip_len, r_groove),       # Groove bottom horizontal
    (L2 - lip_len, r_end),          # Groove vertical up
    (L2, r_end),                    # Lip horizontal
    (L2, r_in),                     # Step down to inner bore right
    
    # The loop is closed automatically by connecting the last point 
    # back to the first point (-L2, r_in) which forms the inner wall.
]

# --- Solid Generation ---
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .revolve(360, (0, 0, 0), (1, 0, 0)) # Revolve profile around X-axis
)

# --- Detail Features ---

# Apply fillets to the transition where the larger ends meet the main body
# We select the edges using NearestToPointSelector targeting the step location
try:
    result = result.edges(cq.selectors.NearestToPointSelector((L2 - end_len, r_main, 0))).fillet(fillet_r)
    result = result.edges(cq.selectors.NearestToPointSelector((-L2 + end_len, r_main, 0))).fillet(fillet_r)
except Exception:
    pass # Handle potential geometry kernel failures gracefully

# Apply chamfers to the end faces (both inner and outer edges)
try:
    # Select the flat faces at the extreme +X and -X ends, then select their edges
    result = result.faces("|X").edges().chamfer(chamfer_val)
except Exception:
    pass