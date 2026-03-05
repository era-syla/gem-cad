import cadquery as cq

# --- Parameter Definitions ---
# Main plate dimensions (estimated from visual proportions)
plate_length = 100.0  # X direction
plate_width = 100.0   # Y direction
plate_thickness = 10.0 # Z direction

# Center hole
center_hole_diam = 25.0

# Inner hole circle pattern
inner_bcd = 50.0  # Bolt Circle Diameter for the 6 inner holes
inner_hole_diam = 6.0
num_inner_holes = 6

# Corner mounting holes
corner_hole_dist_x = 85.0 # Distance between centers in X
corner_hole_dist_y = 85.0 # Distance between centers in Y
corner_hole_diam = 5.0

# Side holes (visible on the front-left edge)
side_hole_diam = 4.0
side_hole_depth = 15.0 # Blind holes
side_hole_spacing = 60.0 # Distance between the two side holes

# --- Geometry Construction ---

# 1. Base Plate
result = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# 2. Center Large Hole
result = result.faces(">Z").workplane().hole(center_hole_diam)

# 3. Inner Bolt Circle Pattern (6 holes)
# We select the top face, create a workplane, and use polarArray
result = (result.faces(">Z").workplane()
          .polarArray(radius=inner_bcd/2.0, startAngle=0, angle=360, count=num_inner_holes)
          .hole(inner_hole_diam))

# 4. Corner Mounting Holes (4 holes)
# We use rectArray to position holes in a rectangular pattern centered on the plate
result = (result.faces(">Z").workplane()
          .rect(corner_hole_dist_x, corner_hole_dist_y, forConstruction=True)
          .vertices()
          .hole(corner_hole_diam))

# 5. Side Holes
# These appear to be on the "front" face (relative to the isometric view), typically -Y face
# The view suggests two holes spaced apart.
result = (result.faces("<Y").workplane()
          .center(0, 0) # Center on the face
          .rect(side_hole_spacing, 0, forConstruction=True) # Establish spacing along X
          .vertices()
          .hole(side_hole_diam, depth=side_hole_depth))

# Export or Render
if __name__ == "__main__":
    # If running in CQ-Editor, this will show the model
    try:
        show_object(result)
    except NameError:
        pass