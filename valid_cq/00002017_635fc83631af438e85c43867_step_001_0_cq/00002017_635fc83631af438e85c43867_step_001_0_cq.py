import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions
length = 100.0  # Total length of the extrusion
height = 50.0   # Total height of the bracket
thickness_max = 30.0 # Maximum thickness at the base

# Blade/Curved section
curve_radius = 40.0 # Radius of the large curved face
tip_thickness = 1.0 # Thickness of the sharp edge at the bottom

# Top mounting rail/features
rail_height = 12.0
rail_thickness = 8.0
rail_fillet = 3.0   # Radius of the top rounded edge

# Mounting Holes
hole_diameter = 4.0
hole_spacing = 40.0 # Distance between hole centers
hole_height_from_bottom = 35.0 # Vertical position
hex_width = 7.0 # Width across flats for hex nut recess
hex_depth = 3.0 # Depth of the hex recess

# --- Modeling ---

# 1. Create the main profile
# We will draw this on the YZ plane and extrude along X
# The profile consists of a vertical back, a top shelf, a rail, and a curved front face.

# Calculate points for the profile
# Origin (0,0) is bottom-back corner
p_bottom_back = (0, 0)
p_top_back = (0, height)
p_rail_top_back = (0, height + rail_height)
p_rail_top_front = (rail_thickness, height + rail_height)
p_rail_base_front = (rail_thickness, height)

# The curved face is trickier. It's an arc.
# It starts at the bottom front tip and ends somewhere on the front face.
# Let's approximate the shape based on the image:
# It looks like a solid block with a large concave cut or a profile defined by an arc.
# Let's define the profile points counter-clockwise starting from bottom-back.

# Adjusting strategy: Sketch the cross-section
def make_profile(h_total, t_max, r_curve, tip_t, rail_h, rail_t):
    # Base block dimensions before curve
    # Let's define the curve starting from the tip and going up to the "shoulder"
    
    # Point at the very bottom tip (sharp edge)
    # The back is at x=0. The tip is at some x. Let's say back face is x=0.
    # Actually, let's keep the back flat at x=0.
    
    s = cq.Sketch()
    s = s.moveTo(0, 0) # Bottom-back corner
    s = s.lineTo(0, h_total + rail_h) # Top-back corner
    s = s.lineTo(rail_t, h_total + rail_h) # Top-front of rail
    
    # Top rail rounded edge (approximated with a line for now, fillet later or arc here)
    # Let's just use lines and fillet the solid later for the top rail
    
    s = s.lineTo(rail_t, h_total) # Bottom of rail front face
    
    # Now the "shoulder" or top flat part of the main body
    s = s.lineTo(t_max, h_total)
    
    # Now the big curve down to the tip.
    # The tip is at y=0, x = some value.
    # Looking at the image, the tip seems to be the forward-most point, or close to it.
    # However, a common scraper shape has the back vertical.
    # Let's assume the curve is a tangent arc or a 3-point arc.
    # The curve goes from (t_max, h_total) to (t_max, 0)? No, that would be a quarter cylinder.
    # The tip looks thinner.
    
    # Let's try a 3-point arc.
    # Start: (t_max, h_total) -> this is the top front corner of the main block
    # End: (t_max, 0) -> Bottom front corner.
    # But wait, the image shows a concave curve.
    # So the material is thicker at the top and thins out at the bottom.
    # Or, the back is vertical, and the front face curves *inwards* towards the back?
    # No, the image shows a "scoop" shape.
    # Let's assume back is flat vertical.
    # The front face is a large radius arc.
    
    # Let's define the tip position.
    tip_x = t_max # It aligns with the top front in X? Or sticks out?
    # In the image, the bottom tip (left side of image) sticks out significantly.
    # The top part (right side of image, where the holes are) is the vertical wall.
    # Ah, orientation:
    # The flat face with the holes is the "front" or "back" depending on perspective.
    # Let's assume the flat face with hex holes is the REAR (or mounting face).
    # But wait, usually hex recesses are on the accessible side.
    # Let's assume the flat vertical face with the holes is the FRONT.
    # Then the curved part sweeps *backwards*.
    
    # Alternative interpretation:
    # The object is a blade holder.
    # The flat face with holes is vertical.
    # There is a ledge/step.
    # Then a large curved surface extends downwards and outwards.
    
    # Let's build it on the YZ plane, extruding along X.
    # Origin (0,0) is bottom-left of the profile.
    
    # Points:
    # 1. (0,0) - The sharp tip at the bottom.
    # 2. Curve upwards and rightwards to the shoulder.
    # 3. Vertical face up for the rail.
    # 4. Top rail geometry.
    # 5. Back down vertical wall.
    
    # Let's refine dimensions based on visual proportions.
    base_width = 30.0 # Width at bottom (tip to back)
    shoulder_height = 35.0 # Height where the curve meets the vertical wall
    wall_thickness = 8.0 # Thickness of the vertical wall part
    
    # Let's try drawing:
    # Start at bottom-left tip (0,0)
    # This is the sharp edge.
    
    # Draw the back vertical line (The flat face with holes)
    # Let's place the flat face with holes at X = base_width.
    # So (base_width, 0) is bottom-back corner.
    # (base_width, height) is top-back corner.
    
    # The curve connects (0,0) to a point on the front face.
    # Let's assume the curve starts at (0,0) and goes to (base_width - wall_thickness, height).
    # That creates the scoop.
    
    s = cq.Workplane("YZ")
    
    # Let's define the points explicitly
    pt_tip = (0, 0)
    pt_back_bottom = (base_width, 0)
    pt_back_top = (base_width, height + rail_height)
    pt_rail_front = (base_width - rail_thickness, height + rail_height)
    pt_rail_bottom = (base_width - rail_thickness, height)
    pt_shoulder = (base_width - wall_thickness, height)
    
    # Draw profile
    s = s.moveTo(*pt_tip)
    s = s.lineTo(*pt_back_bottom)
    s = s.lineTo(*pt_back_top)
    s = s.lineTo(*pt_rail_front)
    
    # Now we need the rail profile.
    # It seems to have a rounded front.
    # Let's just go down to rail bottom for now.
    s = s.lineTo(*pt_rail_bottom)
    
    # Now the shoulder, small horizontal step if any?
    # The image shows the rail is slightly thinner than the main block?
    # Or maybe the rail is the same thickness.
    # Let's assume a small step for visual accuracy.
    s = s.lineTo(*pt_shoulder)
    
    # Now the big curve back to the tip.
    # It's a concave curve.
    s = s.threePointArc((base_width * 0.4, height * 0.25), pt_tip)
    
    return s.close().extrude(length)

# 2. Generate the Base Solid
base_width = 35.0
wall_thickness = 10.0 # Thickness of the part with holes
# Adjusting based on image: The curved part looks like a separate functional surface.
# Let's construct.

# Define the points for the profile on YZ plane
pts = [
    (0, 0),  # Tip
    (base_width, 0), # Back bottom
    (base_width, height + rail_height), # Back top (top of rail)
    (base_width - rail_thickness, height + rail_height), # Front top of rail
    (base_width - rail_thickness, height), # Underside of rail lip
    (base_width - wall_thickness, height), # Shoulder
]

# Create the main extrusion
solid = (
    cq.Workplane("YZ")
    .moveTo(pts[0][0], pts[0][1])
    .lineTo(pts[1][0], pts[1][1])
    .lineTo(pts[2][0], pts[2][1])
    .lineTo(pts[3][0], pts[3][1])
    .lineTo(pts[4][0], pts[4][1])
    .lineTo(pts[5][0], pts[5][1])
    # Create the concave curve from shoulder to tip
    # A generic radius or 3-point arc is needed. 
    # To get a nice sweep, we pick a mid-point for the arc.
    .threePointArc(
        (base_width - wall_thickness - 5.0, height * 0.6), # Control point
        pts[0] # End point (Tip)
    )
    .close()
    .extrude(length)
)

# 3. Add Top Rail Fillet
# The top edge of the rail is rounded in the image.
# We select edges: >Z (top), >Y (back/right in our YZ coordinates -> check local coordinates)
# In global coords: Extrusion is along X. Profile is YZ.
# Top face is at Z = height + rail_height.
# The edge to fillet is the top-front edge of the rail.
# Selector: Z max, and Min Y relative to the rail thickness?
# The rail is at Y approx base_width.
# Wait, Y is horizontal in the 2D profile, Z is vertical.
# In the 3D object:
# X = Length
# Y = Width/Depth
# Z = Height
# We extruded YZ plane along X.
# Profile Y becomes Global Y. Profile Z becomes Global Z.
# Rail is at max Y, max Z.
# The edge to fillet is at (max Z, min Y of the rail part).
# Let's use coordinate selectors for robustness.

edge_selector = (
    cq.selectors.BoxSelector(
        (0, base_width - rail_thickness - 1, height + rail_height - 1),
        (length, base_width - rail_thickness + 1, height + rail_height + 1)
    )
)
# Actually, simpler: Select edges on the top face, filter for the 'front' one relative to the rail.
solid = solid.edges(cq.selectors.NearestToPointSelector((length/2, base_width - rail_thickness, height + rail_height))).fillet(rail_fillet)


# 4. Create Holes with Hex Recesses
# The holes are on the "wall" section.
# This face is at Y = base_width (the back face) or Y = base_width - wall_thickness (front face).
# In the image, the hex nuts are recessed into the flat face.
# The flat face is facing the viewer.
# Based on the "scoop" shape, the scoop is usually the front.
# The image shows the flat face with holes clearly.
# Let's assume the "back" (flat vertical) is actually the face with the holes.
# Face Plane: The face at Y = base_width - wall_thickness (approx).
# We want to drill into the solid.

# Let's locate the face to sketch on.
# It's the vertical face above the curve.
# We will select the face by normal or point.
# Normal is -Y (pointing towards origin).
face_selector = cq.selectors.NearestToPointSelector((length/2, base_width, height/2))

# We need to create the holes.
# Positions along X:
center_x = length / 2
pos_x_1 = center_x - hole_spacing / 2
pos_x_2 = center_x + hole_spacing / 2
# Height Z:
pos_z = height - 15.0 # Adjusted based on visual from top shoulder

# Cut the through holes
solid = (
    solid.faces(">Y") # Select the back face (flat face)
    .workplane()
    .pushPoints([(pos_x_1, pos_z), (pos_x_2, pos_z)])
    .hole(hole_diameter)
)

# Cut the Hex Recesses
# The hexes are on the "front" of that wall section (facing the scoop).
# Wait, in the image, the hexes are on the flat face above the scoop.
# That face normal points in the -Y direction (if back is +Y).
# Let's identify that face. It connects the shoulder to the rail bottom.
target_face = solid.faces(cq.selectors.NearestToPointSelector((length/2, base_width - wall_thickness, height - 5)))

solid = (
    target_face
    .workplane(centerOption="ProjectedOrigin")
    # Coordinate system transformation might be tricky here depending on face normal.
    # Usually easier to rely on absolute coordinates relative to the face center or projected origin.
    # The projected origin of the workplane on that face keeps X aligned with global X.
    # We need to find the Z coordinate relative to the face.
    # Let's just use absolute coordinates matching the holes.
    .pushPoints([(pos_x_1, pos_z), (pos_x_2, pos_z)])
    .polygon(6, hex_width / 1.732) # circumradius = width_across_flats / sqrt(3) approx. Or just use diameter.
    # polygon takes diameter or radius? CQ polygon usually takes radius (circumradius).
    # circumradius = (width_across_flats / 2) / (sqrt(3)/2) * ... no, standard hex math.
    # Side length s. Width flat-to-flat w = s * sqrt(3).
    # Circumradius R = s = w / sqrt(3).
    # Using hex_width (flats) -> Radius = hex_width / 1.732
    .cutBlind(hex_depth) 
)

# 5. Final Rotate for Orientation
# The image shows the part standing up.
# Our model is Z-up, Extruded X. It matches the image orientation generally.

result = solid