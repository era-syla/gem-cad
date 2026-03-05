import cadquery as cq

# --- Parameters ---

# Main Building (the longer section)
main_length = 100.0
main_width = 40.0
main_eave_height = 30.0
main_roof_height = 20.0  # Height from eave to peak

# Side Wing (the shorter section intersecting at 90 degrees)
wing_length = 50.0  # Length protruding from the main building
wing_width = 30.0
wing_eave_height = 25.0 # Slightly lower than main eave
wing_roof_height = 15.0 # Height from eave to peak
wing_offset = 20.0 # Distance from the end of the main building

# --- Helper Function for a House Shape ---

def make_house(length, width, eave_height, roof_height):
    """
    Creates a simple house shape (box + gable roof) along the Y axis.
    """
    # Create the base box
    base = cq.Workplane("XY").box(width, length, eave_height)
    
    # Create the roof prism
    # We'll sketch the triangle profile on the XZ plane and extrude along Y
    roof_profile = (
        cq.Workplane("XZ")
        .moveTo(-width/2, eave_height/2)
        .lineTo(0, eave_height/2 + roof_height)
        .lineTo(width/2, eave_height/2)
        .close()
    )
    
    roof = roof_profile.extrude(length)
    
    # Combine base and roof
    # Note: Extrusion centers on the plane, so we need to move the roof to align
    # The base box is centered at (0,0,0). Its top face is at Z = eave_height/2.
    # The roof profile was drawn relative to the origin, but we need to shift it.
    # Actually, it's easier to just union them relative to global coordinates.
    
    # Let's adjust Z of the base so its bottom is at 0
    base = base.translate((0, 0, eave_height/2))
    
    # The roof profile was drawn starting at Z=eave_height/2 (relative to origin being 0,0)
    # But the Workplane("XZ") is at Y=0. The extrude centers the extrusion.
    # So the roof is centered at Y=0.
    # We need to ensure the Z-levels match.
    # Let's redraw the roof profile specifically to sit on top of the base.
    
    pts = [
        (-width/2, eave_height),
        (0, eave_height + roof_height),
        (width/2, eave_height)
    ]
    
    roof = (
        cq.Workplane("XY")
        .transformed(rotate=(90, 0, 0)) # Rotate to sketch on XZ plane equivalent
        .polyline(pts).close()
        .extrude(length) # Extrudes along local normal (Y)
    )
    
    # Since extrude centers the result along the extrusion vector, translate it back if needed?
    # No, standard extrude is symmetric if 'both=True' is used, otherwise it's directional.
    # By default, CadQuery extrude is directional.
    # Let's use `both=True` on the base box construction to center it, or manage offsets carefully.
    
    # Approach 2: More robust sketches
    
    # 1. Base
    part_base = cq.Workplane("XY").box(width, length, eave_height, centered=(True, True, False))
    
    # 2. Roof
    # Sketch triangle on the front face of the bounding box volume
    # Or just construct a wedge using a prism logic
    
    part_roof = (
        cq.Workplane("XZ")
        .workplane(offset=-length/2) # Move to the back face
        .moveTo(-width/2, eave_height)
        .lineTo(0, eave_height + roof_height)
        .lineTo(width/2, eave_height)
        .close()
        .extrude(length)
    )
    
    return part_base.union(part_roof)

# --- Modeling ---

# 1. Create the Main Building
# Oriented along the Y axis
main_building = make_house(main_length, main_width, main_eave_height, main_roof_height)

# 2. Create the Wing
# Create it initially oriented along Y, then rotate and move it
wing_raw = make_house(wing_length + main_width/2, wing_width, wing_eave_height, wing_roof_height)

# Rotate the wing 90 degrees around Z to orient along X
wing_rotated = wing_raw.rotate((0,0,0), (0,0,1), 90)

# Translate the wing into position
# It needs to intersect the side of the main building.
# `wing_offset` determines position along the main building's Y axis.
# The `wing_length` calculation included `main_width/2` to ensure overlap for clean boolean.
# We shift it so it protrudes out.
wing_x_shift = -(wing_length + main_width/2)/2 + (main_width/2 + wing_length/2) # Simplified: shift center to desired spot
# Let's calculate precise translation
# Center of wing_rotated is currently at (0, 0, 0) in X/Y (roughly)
# We want it sticking out the -X side of the main building.
wing_final = wing_rotated.translate((-main_width/2, -main_length/2 + wing_offset + wing_width/2, 0))

# 3. Combine
result = main_building.union(wing_final)

# Export or Render
if 'show_object' in globals():
    show_object(result)