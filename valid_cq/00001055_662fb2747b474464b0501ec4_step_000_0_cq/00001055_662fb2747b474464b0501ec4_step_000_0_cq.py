import cadquery as cq

# --- Parameters ---
width = 100.0      # Total width of the enclosure (X-axis)
depth = 60.0       # Total depth of the enclosure (Y-axis)
height_back = 40.0 # Height of the back wall (Z-axis)
height_front = 15.0 # Height of the front wall (Z-axis)
wall_thickness = 2.0 # Thickness of the walls and bottom
bottom_thickness = 2.0 # Thickness of the bottom plate
hole_diameter = 3.0 # Diameter of the small mounting holes

# --- Construct the Base Wedge Shape ---
# We'll create the outer shape first, then shell it.
# A wedge is best defined by a side profile extruded across the width.

# Create the side profile points (YZ plane)
# Starting from bottom-left (front) going counter-clockwise
pts = [
    (0, 0),                 # Front-Bottom
    (depth, 0),             # Back-Bottom
    (depth, height_back),   # Back-Top
    (0, height_front)       # Front-Top
]

# Create the solid wedge
wedge = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(width)
)

# Center the wedge on X for symmetry convenience
wedge = wedge.translate((-width/2.0, 0, 0))

# --- Create the "Shell" (Hollow Box) ---
# We want an open top. The "top" face is the slanted one.
# We select the slanted face based on its normal direction (mostly +Z, slightly angled).
# The selector ">Z" usually grabs the highest face, but here we want the one facing up.
# Let's try selecting faces by normal.
slanted_face_normal = (0, height_front - height_back, depth) # Roughly perpendicular vector
# Actually, CadQuery's shell command is robust. Selecting face with normal closest to +Z should work.

result = wedge.faces("+Z").shell(-wall_thickness)

# --- Add Mounting Holes ---
# The image shows small holes on the side faces.
# Let's assume one hole centered on each side face.

# Right side hole
result = (
    result.faces(">X")
    .workplane()
    .center(0, (height_back + height_front)/4) # Approximate center height relative to the slope average
    .circle(hole_diameter / 2)
    .cutThruAll()
)

# Left side hole
result = (
    result.faces("<X")
    .workplane()
    .center(0, (height_back + height_front)/4)
    .circle(hole_diameter / 2)
    .cutThruAll()
)

# Optional: Add a lip or specific edge detail if strictly visible, 
# but the shell command creates the internal lip shown in the image naturally.
# The image shows a slight inset or ridge on the top edge, typical of a shelled part.

# Final orientation adjustment if needed to match the view (Isometric)
# The default creation is typically aligned.

# Explicitly export the result variable
if __name__ == "__main__":
    # If running in CQ-editor, this will render it
    try:
        show_object(result)
    except NameError:
        pass