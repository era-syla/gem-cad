import cadquery as cq

# --- Parameter Definitions ---

# Base Plate Dimensions
plate_length = 100.0  # Total length of the rectangular base
plate_width = 30.0    # Total width of the rectangular base
plate_thickness = 5.0 # Thickness of the base plate

# Central Post Dimensions
post_diameter = 15.0  # Diameter of the main vertical cylinder
post_height = 40.0    # Height of the post from the top surface of the plate

# Post Base (Reinforcement/Collar) Dimensions
collar_diameter = 20.0
collar_height = 10.0  # Height of the collar from the top surface of the plate
collar_flat_dist = 18.0 # Distance between parallel flats on the collar (wrench size)

# Mounting Holes Dimensions
hole_spacing_x = 85.0 # Distance between hole centers along the length
hole_spacing_y = 20.0 # Distance between hole centers along the width
hole_diameter = 4.0   # Through-hole diameter
cbore_diameter = 7.0  # Counterbore diameter (optional, image looks like cbore or countersink)
cbore_depth = 2.0     # Counterbore depth

# End Notches Dimensions
notch_width = 4.0     # Width of the rectangular cutout on ends
notch_depth = 3.0     # Depth of the rectangular cutout on ends

# --- Geometry Construction ---

# 1. Create the Base Plate
# We center it on the origin for easier symmetry operations
base = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# 2. Create the Mounting Holes
# The box is centered, so we define hole locations relative to center
hole_locs = [
    ( hole_spacing_x/2,  hole_spacing_y/2),
    ( hole_spacing_x/2, -hole_spacing_y/2),
    (-hole_spacing_x/2,  hole_spacing_y/2),
    (-hole_spacing_x/2, -hole_spacing_y/2)
]

# Adding Counterbored holes
base = (base.faces(">Z")
            .workplane()
            .pushPoints(hole_locs)
            .cboreHole(hole_diameter, cbore_diameter, cbore_depth))

# 3. Create End Notches
# Notches are on the short edges (X-axis extremes)
notch_locs = [
    ( plate_length/2, 0),
    (-plate_length/2, 0)
]

base = (base.faces(">Z")
            .workplane()
            .pushPoints(notch_locs)
            .rect(notch_depth * 2, notch_width) # Depth is doubled to ensure cut goes through edge
            .cutThruAll())

# 4. Create the Central Post Assembly
# This consists of a base collar with flats and a top cylinder

# Collar (Cylinder first)
collar = (base.faces(">Z")
              .workplane()
              .circle(collar_diameter/2)
              .extrude(collar_height))

# Create flats on the collar
# We cut away material to create the flats
# Calculate cut dimensions to achieve the flat-to-flat distance
cut_width = collar_diameter  # Arbitrary large width for cutting tool
cut_offset = collar_flat_dist / 2 + cut_width / 2

collar = (collar.faces(">Z").workplane()
          .pushPoints([(0, cut_offset), (0, -cut_offset)])
          .rect(collar_diameter * 2, cut_width)
          .cutBlind(-collar_height))


# Main Post Cylinder
post = (collar.faces(">Z")
              .workplane()
              .circle(post_diameter/2)
              .extrude(post_height - collar_height))

# Add a small chamfer to the top of the post for a finished look
result = post.faces(">Z").edges().chamfer(0.5)

# If you want to explicitly combine them (though extrude usually combines)
# In CadQuery 2, operations on a Workplane maintain the solid stack.
# The `result` variable holds the final modified solid.