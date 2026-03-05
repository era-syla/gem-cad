import cadquery as cq

# Parametric Dimensions
flange_diameter = 30.0
flange_thickness = 3.0
body_diameter = 20.0
total_height = 20.0
inner_diameter = 14.0
slit_width = 2.0
chamfer_size = 1.0

# Create the base shape (Revolved profile strategy)
# 1. Start with the flange
# 2. Add the main cylindrical body
# 3. Create the central hole
# 4. Add the slit
# 5. Add the chamfer on top

# Strategy: Construct basic cylinders and boolean operations

# Base Flange
flange = cq.Workplane("XY").circle(flange_diameter / 2.0).extrude(flange_thickness)

# Main Body Cylinder
body = cq.Workplane("XY").workplane(offset=flange_thickness).circle(body_diameter / 2.0).extrude(total_height - flange_thickness)

# Union the flange and body
bushing_solid = flange.union(body)

# Create the through hole
bushing_solid = bushing_solid.faces("<Z").workplane().circle(inner_diameter / 2.0).cutThruAll()

# Create the vertical slit
# We position a rectangle to cut through one side of the wall
slit_cutter = (
    cq.Workplane("XZ")
    .workplane(offset=-total_height / 2.0)  # Center vertically relative to origin if needed, but easier to just position correctly
    .center(0, total_height / 2.0)
    .rect(body_diameter, total_height) # Make it large enough to cut through
    .extrude(slit_width/2.0, both=True) # Extrude symmetrically to get width
)

# Move the cutter to the edge to slice just the wall
# Actually, a simple centered rectangle on the XY plane extruded up works best for a radial slit
slit_cutter_simple = (
    cq.Workplane("XY")
    .rect(body_diameter / 2.0 + 5.0, slit_width) # Length creates radial depth, Width is the slit width
    .extrude(total_height)
    .translate((body_diameter/2.0, 0, 0)) # Shift it out so it cuts one side
)

bushing_solid = bushing_solid.cut(slit_cutter_simple)

# Apply Chamfer to the top outer edge
# Select faces at max Z, then select outer wire
bushing_solid = (
    bushing_solid.faces(">Z")
    .wires()
    .last() # Select the outer wire of the top face
    .chamfer(chamfer_size)
)

result = bushing_solid