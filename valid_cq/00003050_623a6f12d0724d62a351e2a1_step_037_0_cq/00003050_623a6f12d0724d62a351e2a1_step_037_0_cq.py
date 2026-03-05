import cadquery as cq

# Parameters for a standard 2020 T-Slot Aluminum Profile
profile_size = 20.0
length = 100.0  # Length of the extrusion
center_hole_dia = 4.2
corner_radius = 1.5
slot_width_opening = 6.2  # The width of the slot at the surface
slot_width_inner = 11.5   # The wider inner part of the slot (estimated for generic 2020)
slot_depth = 6.0          # Total depth from surface
slot_lip_thickness = 1.8  # Thickness of the lip holding the T-nut
wall_thickness = 1.5      # Approximate wall thickness

# Calculate derived dimensions to help sketch construction
half_size = profile_size / 2.0
slot_start_offset = slot_width_opening / 2.0
slot_inner_offset = slot_width_inner / 2.0

# Define the 2D profile sketch
# We will create one quadrant and mirror it to ensure symmetry

def create_t_slot_sketch():
    # Start with a base square
    base = cq.Sketch().rect(profile_size, profile_size)
    
    # Create the cutting tool for the T-slots
    # We will make one "T" shape and rotate/copy it for all 4 sides
    
    # Define the T-slot shape using a polyline for one slot
    # Coordinates are relative to the center of the profile
    # Focusing on the top slot (Positive Y)
    
    t_slot_cutter = (
        cq.Sketch()
        .push([(0, half_size)]) # Move to top edge center
        .rect(slot_width_opening, slot_depth * 2) # Vertical part (opening), make it deep enough to cut
        .push([(0, half_size - slot_lip_thickness - (slot_depth - slot_lip_thickness)/2)])
        .rect(slot_width_inner, slot_depth - slot_lip_thickness) # Horizontal part (inner cavity)
    )
    
    # Combine the vertical and horizontal parts of the top slot
    full_top_slot = t_slot_cutter
    
    # Create the full profile by cutting slots from the base square
    # Since Sketch logic can be tricky with complex boolean subtractions of multiple objects,
    # we'll use solid modeling operations (extrude then cut) which is often more robust for T-slots in CQ.
    return base

# Alternative approach: Construct the face directly using 2D points or standard boolean operations on solids.
# Let's use the Solid modeling approach for clarity and robustness.

# 1. Base Block
base_block = cq.Workplane("XY").box(profile_size, profile_size, length)

# 2. Create the T-slot profile cutter
# We draw the profile of the CUT on the top face
slot_sketch = (
    cq.Workplane("XY")
    .workplane(offset=length/2.0) # Move to top face
    # Draw the main opening rectangle
    .rect(slot_width_opening, profile_size * 2) # Vertical slot
    .rect(profile_size * 2, slot_width_opening) # Horizontal slot
    .extrude(-slot_depth) # Cut down
)

# 3. Create the inner wider part of the T-slot
# We need to position these "inside" the block
inner_slot_sketch = (
    cq.Workplane("XY")
    .workplane(offset=length/2.0 - slot_lip_thickness) # Start below the surface
    .rect(slot_width_inner, profile_size * 2) # Vertical inner
    .rect(profile_size * 2, slot_width_inner) # Horizontal inner
    .extrude(-(slot_depth - slot_lip_thickness)) # Cut the rest of the depth
)

# 4. Center Hole
center_hole = (
    cq.Workplane("XY")
    .circle(center_hole_dia / 2.0)
    .extrude(length)
)

# 5. Apply cuts to the base block
result = (
    base_block
    .cut(slot_sketch)
    .cut(inner_slot_sketch)
    .cut(center_hole)
)

# 6. Add Fillets to the outer corners
result = result.edges("|Z").fillet(corner_radius)

# Optional: Add small fillets to the slot edges for realism (often 0.2-0.5mm)
# Selecting these specific edges programmatically can be complex, 
# but selecting edges on the top/bottom face that are not the outer perimeter works.
# For simplicity in this generated code, we stick to the main geometry features.