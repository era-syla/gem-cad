import cadquery as cq

# --- Parametric Dimensions ---
# Main block dimensions
width = 60.0        # Overall width/height of the block
thickness = 20.0    # Thickness of the main block

# Corner and side features
corner_radius = 8.0 # Radius of the rounded corners
side_radius = 40.0  # Radius of the concave cutout on the sides (approximate)

# Hole dimensions
center_hole_diam = 15.0
mounting_hole_diam = 6.0
mounting_hole_spacing = 42.0 # Distance between centers of mounting holes

# Top hole dimensions
top_hole_diam = 8.0

# --- Modeling ---

# 1. Create the base profile
# We'll start with a square, round the corners, and then cut the sides to get the "dogbone" or "scalloped" look.
# Alternatively, we can construct the sketch more directly.

# Let's use a technique of creating a block and then applying fillets and cuts.
# A box centered on XY plane.
base = cq.Workplane("XY").box(width, width, thickness)

# 2. Apply Corner Fillets
# Select the vertical edges (Z-parallel) at the corners
base = base.edges("|Z").fillet(corner_radius)

# 3. Create Concave Sides
# We need to cut a curved shape out of the four flat sides.
# We can do this by placing cylinders on the midpoints of the sides and subtracting them.
# The side_radius determines how deep the cut is.
# Calculate offset to place the cutting cylinder so it just grazes or cuts slightly deep.
# If we want a subtle curve, the cylinder center needs to be far out.
# Let's try a different approach: constructing the profile with a sketch might be cleaner, 
# but modifying the solid is often more robust in simple CSG.

# Let's estimate the side cut. It looks like a large radius arc cutting into the flat face.
# Distance from center to flat face is width/2 = 30.
# If we put a cylinder of radius R at distance D from center, such that D - R < width/2, we get a cut.
# Let's assume the cut depth is about 2-3mm.
cut_depth = 3.0
# We need a circle that passes through (width/2 - cut_depth, 0) and has a certain curvature.
# Let's just pick a reasonable large radius for the cut tool.
cut_tool_radius = 30.0
cut_tool_center_offset = (width / 2.0) + cut_tool_radius - cut_depth

# Create the cutting tool (a cylinder)
cut_tool = cq.Workplane("XY").circle(cut_tool_radius).extrude(thickness * 2).translate((cut_tool_center_offset, 0, 0))

# Subtract the tool from all 4 sides by rotating the tool and cutting
result = base
for angle in [0, 90, 180, 270]:
    # We need to recreate or rotate the tool for each side. 
    # Since CadQuery operations are immutable-ish or chainable, we handle position relative to the object.
    # An easier way in CQ is using a sketch or just 4 cylinders.
    
    # Position a cylinder on the side
    cutter = (cq.Workplane("XY")
              .workplane(offset=-thickness) # Start lower to ensure full cut
              .center(cut_tool_center_offset, 0)
              .circle(cut_tool_radius)
              .extrude(thickness*3)) # Extrude plenty
    
    # Rotate the cutter around the Z axis to the correct position
    cutter = cutter.rotate((0,0,0), (0,0,1), angle)
    
    result = result.cut(cutter)


# 4. Create the Central Hole
result = result.faces(">Z").workplane().hole(center_hole_diam)

# 5. Create the 4 Mounting Holes
# We can use a rect pattern for this.
result = (result.faces(">Z").workplane()
          .rect(mounting_hole_spacing, mounting_hole_spacing, forConstruction=True)
          .vertices()
          .hole(mounting_hole_diam))

# 6. Create the Top/Radial Hole
# The image shows a hole entering from one of the curved sides (let's say the top Y+) going towards the center.
# We need to select a face or plane on the side.
# Since the side is curved, we best establish a plane from the origin or tangent.
# Looking at the image, there is a hole on the "top" face (relative to the camera view, could be Y+ or Z+ depending on orientation). 
# The part looks extruded in Z. The hole is on the cylindrical side surface (or the scalloped surface).
# Let's assume it's on the +Y side, drilling inwards towards the center.

result = (result.faces(">Y").workplane(centerOption="CenterOfMass")
          .center(0, 0) # Center on the face. Note: The face might be complex due to the cut.
          # Ideally, we define a plane offset from center.
          .workplane(centerOption="ProjectedOrigin") 
          # Reset to global origin relative plane, then move up to top surface
          .transformed(offset=cq.Vector(0, width/2.0 - cut_depth, 0), rotate=cq.Vector(90, 0, 0))
          # Now we are looking "down" Y axis (or up, depending on rotation convention).
          # Actually, easiest is to just grab the XZ plane and extrude a cut cylinder.
         )

# Alternative robust way for the side hole:
# Create a cylinder along Y axis and cut.
side_hole = (cq.Workplane("XZ")
             .circle(top_hole_diam / 2.0)
             .extrude(width) # Make it long enough
             .translate((0, width/2.0, 0)) # Move to Y+ side
             )
# We want the hole to go *into* the part, stopping at the center hole or going through. 
# The image shows it going into the center.
# Let's construct a cylinder that starts outside and goes to the center.
side_hole_cutter = (cq.Workplane("XZ")
                    .workplane(offset=width/2.0) # Move plane to Y=width/2 approx
                    .circle(top_hole_diam/2.0)
                    .extrude(-width/2.0 - center_hole_diam) # Extrude inwards (negative normal)
                    )

# Because the side is concave, we need to ensure the cutter starts *outside* the geometry.
# width/2 might be slightly inside the "corners" but outside the "cut".
# The cut depth brings the surface to (width/2 - 3). 
# Starting at width/2 + 5 is safe.
side_hole_cutter = (cq.Workplane("XZ")
                    .workplane(offset=(width/2.0) + 10.0) 
                    .circle(top_hole_diam/2.0)
                    .extrude(-((width/2.0) + 10.0)) # Cut all the way to center
                    )

result = result.cut(side_hole_cutter)

# 7. Final Polish
# The image shows slight fillets on the top and bottom edges of the main shape?
# It's hard to tell if there's a chamfer or fillet. It looks relatively sharp but maybe a small break.
# Let's add a small fillet to the outer edges for realism, as typical in machined/cast parts.
try:
    result = result.edges("|Z").invert().fillet(1.0)
except:
    # Sometimes complex topology fails to fillet all at once
    pass 

# The "result" variable is required
# Just to be safe with the orientation matching the image:
# The image shows the side hole on the "top left" relative to the face. 
# Our code put it on Y+. If Z is the view axis, Y+ is up.
# This matches the "Top" feature.

# Return result
result = result