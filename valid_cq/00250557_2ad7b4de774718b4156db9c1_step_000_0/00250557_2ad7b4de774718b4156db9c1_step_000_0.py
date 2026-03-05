import cadquery as cq

# Dimensions based on visual estimation from the image
length = 90.0        # Total length of the base
width = 24.0         # Width of the base
thickness = 6.0      # Thickness of the base plate
hole_diam = 10.0     # Diameter of the holes
tab_radius = 10.0    # Radius of the vertical semi-circular tab
tab_thickness = 5.0  # Thickness of the vertical tab

# 1. Create the base: A slot shape extruded
# slot2D creates a shape with rounded ends along the X-axis
# length is the total length, width is the diameter of the rounded ends
result = cq.Workplane("XY").slot2D(length, width).extrude(thickness)

# 2. Add the holes
# Calculate the position of the hole centers. 
# For a slot, centers are at +/- (Length - Width) / 2
hole_offset = (length - width) / 2
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(-hole_offset, 0), (hole_offset, 0)])
    .hole(hole_diam)
)

# 3. Create and add the vertical tab
# The tab is located on the side edge (Y = width/2) and stands vertically (XZ plane)
# We create a separate solid for the tab and union it
tab = (
    cq.Workplane("XZ")
    .workplane(offset=width/2)  # Offset to the outer edge of the base
    .center(0, thickness)       # Move origin to the top surface of the base
    .moveTo(-tab_radius, 0)     # Start at the left corner of the semi-circle base
    .threePointArc((0, tab_radius), (tab_radius, 0))  # Draw semi-circle arc
    .close()                    # Close the profile with a line at the bottom
    .extrude(-tab_thickness)    # Extrude inwards (negative Y direction)
)

# Combine the tab with the base
result = result.union(tab)