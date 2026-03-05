import cadquery as cq

# Parameters for a generic 2020 T-slot aluminum extrusion
# Dimensions are based on standard 20mm x 20mm profile specifications
profile_width = 20.0
profile_height = 20.0
length = 100.0  # Length of the extrusion

# Slot dimensions
slot_opening = 6.0    # Width of the slot opening
slot_depth = 6.0      # Depth from surface to bottom of slot
slot_bottom_width = 11.0 # Width of the wider part of the T-slot
slot_lip_thickness = 1.5 # Thickness of the lip holding the nut
center_hole_diam = 4.2   # Diameter of the central hole (usually tap-ready for M5)
corner_radius = 1.5      # Radius of the external corners

# Helper calculation for the T-slot geometry
# We will create a sketch of the cross-section and extrude it.

# Create the main square body
base = cq.Workplane("XY").box(profile_width, profile_height, length)

# Create a sketch for the T-slot cutout
# We'll define one T-slot shape and rotate it around the center
def create_slot_sketch():
    s = (
        cq.Sketch()
        .rect(slot_opening, slot_depth * 2) # Vertical part of the T (made extra long to cut through)
        .push([(0, -slot_depth/2)]) # Position for the bottom horizontal part
        .rect(slot_bottom_width, slot_depth - slot_lip_thickness) # Bottom wide part
    )
    return s

# Create the full cross-section profile by starting with a square and subtracting slots
# Instead of boolean operations on 3D solids which can be slow, let's draw the 2D profile.

# Define the 2D profile sketch
profile_sketch = (
    cq.Sketch()
    .rect(profile_width, profile_height) # Start with the base square
    .vertices()
    .fillet(corner_radius) # Round the outer corners
    
    # Cut the central hole
    .circle(center_hole_diam / 2, mode='s')
    
    # Cut the Top Slot
    .push([(0, profile_height/2 - slot_depth/2 + slot_lip_thickness/2)])
    .rect(slot_opening, slot_depth, mode='s') # Neck
    .push([(0, profile_height/2 - slot_depth + (slot_depth-slot_lip_thickness)/2)])
    .rect(slot_bottom_width, slot_depth - slot_lip_thickness, mode='s') # Base
    
    # Cut the Bottom Slot
    .push([(0, -(profile_height/2 - slot_depth/2 + slot_lip_thickness/2))])
    .rect(slot_opening, slot_depth, mode='s') # Neck
    .push([(0, -(profile_height/2 - slot_depth + (slot_depth-slot_lip_thickness)/2))])
    .rect(slot_bottom_width, slot_depth - slot_lip_thickness, mode='s') # Base
    
    # Cut the Right Slot
    .push([(profile_width/2 - slot_depth/2 + slot_lip_thickness/2, 0)])
    .rect(slot_depth, slot_opening, mode='s') # Neck (rotated rect dimensions)
    .push([(profile_width/2 - slot_depth + (slot_depth-slot_lip_thickness)/2, 0)])
    .rect(slot_depth - slot_lip_thickness, slot_bottom_width, mode='s') # Base
    
    # Cut the Left Slot
    .push([(-(profile_width/2 - slot_depth/2 + slot_lip_thickness/2), 0)])
    .rect(slot_depth, slot_opening, mode='s') # Neck
    .push([(-(profile_width/2 - slot_depth + (slot_depth-slot_lip_thickness)/2), 0)])
    .rect(slot_depth - slot_lip_thickness, slot_bottom_width, mode='s') # Base
)

# Extrude the profile to create the final object
result = cq.Workplane("XY").placeSketch(profile_sketch).extrude(length)

# Optional: Add small fillets to the internal slot corners for realism (often skipped for simple CAD)
# In this script, we keep sharp internal corners for cleaner code, as per standard simple CAD representations.