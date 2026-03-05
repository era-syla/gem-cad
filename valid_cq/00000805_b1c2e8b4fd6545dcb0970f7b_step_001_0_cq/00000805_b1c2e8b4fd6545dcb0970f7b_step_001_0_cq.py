import cadquery as cq

# --- Parameter Definitions ---
# Shaft/Screw parameters
shaft_diameter = 10.0
shaft_length_total = 80.0
shaft_threaded_length = 60.0 # Length of the "threaded" part

# Flange parameters
flange_outer_diameter = 40.0
flange_thickness = 5.0
flange_hub_diameter = 16.0
flange_hub_height = 2.0  # Height of the small raised ring on the flange face
flange_position_z = 30.0 # Distance from the knob end to the flange

# Mounting holes (pattern of 4)
bolt_circle_diameter = 28.0
hole_diameter = 4.5
num_holes = 4

# Knob/End Cap parameters
knob_diameter = 18.0
knob_thickness = 8.0

# --- Geometry Construction ---

# 1. Create the main shaft
# We orient the shaft along the Z axis.
shaft = cq.Workplane("XY").circle(shaft_diameter / 2).extrude(shaft_length_total)

# 2. Create the End Knob
# Placed at Z=0, extruding downwards (or just unioned at the start)
knob = (
    cq.Workplane("XY")
    .circle(knob_diameter / 2)
    .extrude(knob_thickness)
)

# Move the shaft so it starts on top of the knob
shaft = shaft.translate((0, 0, knob_thickness))

# 3. Create the Flange
# The flange sits further up the shaft.
flange_base = (
    cq.Workplane("XY")
    .circle(flange_outer_diameter / 2)
    .extrude(flange_thickness)
    .translate((0, 0, knob_thickness + flange_position_z))
)

# 4. Create the Flange Hub (raised ring on the flange)
flange_hub = (
    cq.Workplane("XY")
    .circle(flange_hub_diameter / 2)
    .extrude(flange_hub_height)
    .translate((0, 0, knob_thickness + flange_position_z + flange_thickness))
)

# 5. Create Mounting Holes in the Flange
# We create a new workplane on the face of the flange to drill holes.
# We need to find the Z-height of the flange face.
flange_face_z = knob_thickness + flange_position_z

flange_with_holes = (
    flange_base
    .faces(">Z").workplane()
    .polarArray(bolt_circle_diameter / 2, 0, 360, num_holes)
    .circle(hole_diameter / 2)
    .cutThruAll()
)

# 6. Combine all parts
# We union the knob, shaft, flange (with holes), and the hub.
result = knob.union(shaft).union(flange_with_holes).union(flange_hub)

# Optional: Add a visual representation of threads (simple helical cut or just texture in rendering)
# For standard CAD geometry, a simple cylinder is preferred for performance, 
# but we can make it look a bit more like the image by adding a slight chamfer or 
# distinct section if needed. The image shows a threaded texture. 
# CadQuery `thread` operations are computationally expensive, so usually omitted 
# unless specifically required for printing.
# We will leave it as a solid shaft as is standard engineering practice.

# However, looking closely at the image, there is a distinct visual difference 
# between the thread area and the flange hub area. The flange seems to be a nut 
# riding on the screw. Let's ensure the hole through the flange aligns with the shaft.
# The previous union operation merges them solid. If this is an assembly (screw + nut),
# they would be separate, but the prompt asks for a single model result.
# The code above creates a single solid body representing the assembly.

# Let's refine the "threaded" look slightly by ensuring the shaft goes *through* the flange
# which the union handles correctly.

# Final cleanup/fillet if necessary to match the smooth look
# Fillet the transition between knob and shaft
result = result.edges(cq.selectors.NearestToPointSelector((0, 0, knob_thickness))).fillet(1.0)

# Fillet the transition between flange hub and shaft
result = result.edges(cq.selectors.NearestToPointSelector((0, 0, knob_thickness + flange_position_z + flange_thickness + flange_hub_height))).fillet(0.5)