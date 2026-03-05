import cadquery as cq

# Parameters for dimensions to allow easy adjustments
width = 50.0       # Width of the base rectangle
height_rect = 50.0 # Height of the rectangular part
depth = 30.0       # Extrusion thickness
text_string = "Test"
text_size = 18.0   # Font size for the text
text_depth = 5.0   # How deep to cut (though we will cut through)

# 1. Create the base profile (Tombstone shape)
# We start with a rectangle and then add a circle/arc on top, or construct a sketch.
# A simpler way in CQ is to make a box and fillet the top edge, or draw the profile.
# Let's draw the 2D profile and extrude.

# Create a sketch on the XY plane
profile = (
    cq.Workplane("XY")
    .lineTo(width, 0)           # Bottom edge
    .lineTo(width, height_rect) # Right vertical edge
    .threePointArc(             # Top arch
        (width / 2.0, height_rect + (width / 2.0)), # Peak of the arc
        (0, height_rect)                            # End of the arc (top-left corner)
    ) 
    .close()
)

# 2. Extrude the profile to create the main solid body
main_body = profile.extrude(depth)

# 3. Create the text cut
# We need to position the text correctly.
# Based on the image, the text is centered horizontally on the face and positioned 
# in the lower half (rectangular section).
# It seems to be cut through the front face (XZ plane relative to our extrusion, 
# or XY if we work on that face).

# Let's select the front face. 
# Since we drew on XY and extruded in Z (positive or negative depending on implementation, 
# usually positive Z), the "front" face is at Z=depth or Z=0.
# Let's assume we want to cut into the face at Z=depth.

text_cut = (
    main_body.faces(">Z") # Select the top Z face (the front of the extrusion)
    .workplane()
    # Position the text. 
    # Center X: width/2
    # Center Y: height_rect/2 (approximately, adjusted visually)
    .center(width/2, height_rect/2) 
    # Create the text geometry. 
    # 'cut=True' makes it a subtractive operation.
    # 'combine=True' applies it to the existing model.
    .text(text_string, fontsize=text_size, distance=-depth - 1.0, cut=True, halign="center", valign="center")
)

# 4. Final result assignment
result = text_cut