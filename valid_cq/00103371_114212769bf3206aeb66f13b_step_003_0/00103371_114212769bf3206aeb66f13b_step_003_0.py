import cadquery as cq
import math

# --- Parameters ---
total_length = 150.0       # Total length of the shaft
shaft_diameter = 6.0       # Diameter of the threaded/smooth shaft
flange_diameter = 13.0     # Diameter of the integrated washer/flange
flange_thickness = 1.5     # Thickness of the flange
hex_flat_to_flat = 10.0    # Hex head size (wrench size)
hex_height = 5.0           # Height of the hex part of the head
chamfer_size = 0.5         # Size of chamfers at tip and head
fillet_radius = 0.4        # Fillet radius under the head

# --- Helper Calculations ---
# Calculate the outer diameter of the hexagon (across corners)
# Relationship: AcrossCorners = AcrossFlats / cos(30 degrees)
hex_across_corners = hex_flat_to_flat / math.cos(math.radians(30))

# --- Modeling ---

# 1. Create the Shaft (Extruding downwards from Z=0)
# We model the shaft as a single cylinder. 
# While the image shows threaded sections, valid solid CAD often simplifies threads 
# to the major diameter cylinder to keep geometry lightweight.
shaft = cq.Workplane("XY").circle(shaft_diameter / 2.0).extrude(-total_length)

# 2. Create the Flange (Extruding upwards from Z=0)
flange = cq.Workplane("XY").circle(flange_diameter / 2.0).extrude(flange_thickness)

# 3. Create the Hex Head (Extruding upwards from top of flange)
head_hex = (cq.Workplane("XY")
            .workplane(offset=flange_thickness)
            .polygon(6, hex_across_corners)
            .extrude(hex_height))

# 4. Union the base components
# Combining shaft, flange, and hex head into one solid object
result = shaft.union(flange).union(head_hex)

# 5. Add Detailed Features

# Chamfer the top of the hex head (standard bolt manufacturing style)
# We select the highest face (>Z) and chamfer its edges
result = result.faces(">Z").edges().chamfer(chamfer_size)

# Optional: Add a slight recessed dish on top of the head (visual detail often seen on flange bolts)
result = (result.faces(">Z").workplane()
          .circle(hex_flat_to_flat * 0.4) # Small circle in center
          .cutBlind(-0.2)) # Slight depression

# Chamfer the bottom tip of the shaft (start of threads)
# Select the lowest face (<Z) and chamfer its edges
result = result.faces("<Z").edges().chamfer(chamfer_size)

# Add a stress-relief fillet where the shaft meets the flange
# We select the edge closest to the shaft radius at the Z=0 plane
# Point to select: (radius, 0, 0)
edge_under_head = result.edges(cq.NearestToPointSelector((shaft_diameter/2.0, 0, 0)))
result = edge_under_head.fillet(fillet_radius)

# 'result' now contains the final solid geometry