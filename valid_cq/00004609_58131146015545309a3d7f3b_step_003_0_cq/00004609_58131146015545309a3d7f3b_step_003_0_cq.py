import cadquery as cq

# Parametric dimensions
head_diameter = 10.0   # Diameter of the top of the head
shank_diameter = 4.0   # Diameter of the cylindrical body
total_length = 20.0    # Total length of the part
head_height = 3.0      # Height of the conical head section
end_taper_height = 1.5 # Height of the tapered end section
end_taper_dia = 2.5    # Diameter at the very tip

# Create the profile for revolution
# We sketch half the profile on the XZ plane and revolve around the Z axis
result = (
    cq.Workplane("XZ")
    .moveTo(0, total_length)                  # Start at center top (though we want head at top usually, let's orient it like a standard screw)
    # Let's orient it so head is at Z=0 and pointing -Z, or head at Z=head_height.
    # Actually, easiest is to just draw the profile line by line.
    
    # Start at the center axis, bottom of the shank
    .moveTo(0, 0)
    .lineTo(end_taper_dia / 2.0, 0)           # Bottom flat tip radius
    .lineTo(shank_diameter / 2.0, end_taper_height) # Taper up to shank diameter
    .lineTo(shank_diameter / 2.0, total_length - head_height) # Straight shank
    .lineTo(head_diameter / 2.0, total_length) # Conical head flare
    .lineTo(0, total_length)                  # Back to center axis
    .close()
    .revolve()
)

# Optional: If you prefer the head at the "bottom" (Z=0) like the image suggests a bit,
# you can rotate it. But structurally, the above is a valid solid.
# The image shows the head on the left/top-ish. Revolve creates it along Z.
# Let's align it roughly with the image view: rotate around X or Y.
result = result.rotate((0, 0, 0), (1, 0, 0), -90)