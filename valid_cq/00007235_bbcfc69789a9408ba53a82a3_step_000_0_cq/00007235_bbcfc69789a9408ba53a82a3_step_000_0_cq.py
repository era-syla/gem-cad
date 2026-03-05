import cadquery as cq

# Parametric dimensions
plate_width = 150.0   # Width of the square plate
plate_height = 150.0  # Height of the square plate
thickness = 3.0       # Thickness of the plate

# Main center hole
center_hole_dia = 6.0

# Small pin hole near center
pin_hole_dia = 2.0
pin_hole_offset_y = -15.0 # Distance below the center

# Mounting holes
mount_hole_dia = 4.0
mount_hole_inset = 10.0   # Distance from edges
# Calculate mount hole positions relative to center
mh_x = (plate_width / 2.0) - mount_hole_inset
mh_y = (plate_height / 2.0) - mount_hole_inset

# Create the main plate
result = (
    cq.Workplane("XY")
    .box(plate_width, plate_height, thickness)
    
    # Add the central hole
    .faces(">Z").workplane()
    .hole(center_hole_dia)
    
    # Add the small pin hole below the center
    .faces(">Z").workplane()
    .center(0, pin_hole_offset_y)
    .hole(pin_hole_dia)
    
    # Add the four mounting holes near the corners
    # The image shows holes in corners and one in the middle of the right side?
    # Let's look closer at the image.
    # It has holes at: Top Left, Top Right, Bottom Left.
    # It seems to be missing a hole at Bottom Right, but has one on the Right Edge middle.
    # Actually, looking at the crop images:
    # Top-Left corner hole.
    # Top-Right corner hole.
    # Bottom-Left corner hole.
    # There is a hole on the right edge, approximately halfway down the bottom half? Or just centered vertically?
    # Wait, let's re-examine the full image.
    # It looks like a standard 4-corner pattern, but the lighting makes the bottom-right one hard to see?
    # No, there is clearly a hole on the right edge, lower than the center line.
    # And there is a hole at bottom-left.
    # Let's assume a standard pattern first, but the image is specific.
    # Image features:
    # 1. Top Left Corner
    # 2. Top Right Corner
    # 3. Bottom Left Corner
    # 4. Right Edge, vertically centered between bottom and middle? No, it looks like a specific mounting pattern.
    
    # Let's assume a more standard 4-corner mounting plate first, as that is most likely, 
    # but looking really closely at the 4th crop (bottom right area), there is a hole on the right edge, 
    # but it's not in the corner. It's up from the bottom.
    # And there is a hole in the bottom left corner.
    # Let's place holes explicitly to match the visual asymmetry if needed, 
    # but often these are standard VESA or similar plates. 
    # Let's stick to the visual evidence: 
    # - Top Left
    # - Top Right
    # - Bottom Left
    # - Right side, roughly 1/4 up from bottom? Or maybe it's just a 3-hole mount?
    # Actually, looking at the right edge, there is a hole on the right side, maybe mid-way between center and bottom.
    
    # Let's define specific coordinates based on visual estimation for a generic representation
    # Top-Left: (-x, y)
    # Top-Right: (x, y)
    # Bottom-Left: (-x, -y)
    # Right-Mid-Low: (x, -y_offset)
    
    # Revisiting the "Right Edge" hole. It looks like it might be at the same Y level as the center hole?
    # No, it's lower.
    # Let's implement the standard 4 corners + countersink details if visible (they look like simple countersunk holes).
    # The hole on the right side is weird. It might be a reflection or a specific design.
    # However, for a robust generative model, a 4-corner pattern is the safest "standard" interpretation 
    # unless specific asymmetry is requested. 
    # Wait, looking at the 4th crop again. The hole is definitely on the right edge, slightly above the bottom.
    # It looks like the hole corresponding to the bottom-right corner is shifted up.
    
    # Let's go with a symmetrical 4-corner pattern as it's the standard engineering default 
    # and "missing/shifted" holes in renders can sometimes be lighting artifacts or very specific undisclosed specs.
    # BUT, to be most faithful to the image:
    # - Top Left
    # - Top Right
    # - Bottom Left
    # - Right Side (shifted up from bottom corner)
    
    # Let's use a list of points for the holes.
    # Points based on approximate visual location:
    # TL: (-65, 65)
    # TR: (65, 65)
    # BL: (-65, -65)
    # Right-Side: (65, -15) -- This looks like the one on the right edge.
    
    # Actually, looking very closely at the full image again:
    # There is a hole in the Top Left.
    # There is a hole in the Top Right.
    # There is a hole in the Bottom Left.
    # There is a hole on the Right edge, roughly at height Y=-30 (if center is 0).
    # This is an asymmetrical pattern.
    
    .faces(">Z").workplane()
    .pushPoints([
        (-mh_x, mh_y),   # Top Left
        (mh_x, mh_y),    # Top Right
        (-mh_x, -mh_y),  # Bottom Left
        (mh_x, -15.0)    # Right side, shifted up from bottom. 
                         # Visually it looks aligned with the small pin hole's Y level or slightly below.
                         # Let's approximate it.
    ])
    .cskHole(mount_hole_dia, mount_hole_dia * 2.0, 82.0) # Countersunk holes
)

# Note: I've chosen countersunk (cskHole) because the holes in the image 
# have that characteristic conical rim shading.