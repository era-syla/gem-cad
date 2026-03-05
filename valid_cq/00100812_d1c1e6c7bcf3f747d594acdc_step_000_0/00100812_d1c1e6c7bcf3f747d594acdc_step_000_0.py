import cadquery as cq

# --- Parametric Dimensions ---
# Main Cartridge Body
cartridge_diameter = 4.0      # Outer diameter of the heater/probe
cartridge_length = 100.0      # Length of the metal sheath
wall_thickness = 0.5          # Wall thickness for the open tip appearance

# Lead Wires
wire_diameter = 1.2           # Diameter of wire insulation
conductor_diameter = 0.6      # Diameter of the stripped conductor
wire_length = 30.0            # Length of the insulated wire extending from body
stripped_length = 5.0         # Length of the stripped conductor tip
wire_spacing = 1.6            # Center-to-center spacing of the wires

# --- Modeling ---

# 1. Main Cartridge (Sheath)
# Create a cylinder aligned along the X-axis
cartridge = (
    cq.Workplane("YZ")
    .circle(cartridge_diameter / 2.0)
    .extrude(cartridge_length)
)

# Feature: Hollow tip / Potting recess
# Create a shallow cut on the distal face (+X) to simulate the tube wall or potting depth
cartridge = (
    cartridge.faces(">X")
    .workplane()
    .circle((cartridge_diameter / 2.0) - wall_thickness)
    .cutBlind(-1.0)
)

# Feature: Chamfer the proximal end (X=0) for a cleaner transition
cartridge = cartridge.faces("<X").chamfer(0.2)

# 2. Lead Wires
# Function to generate a complete wire (insulation + conductor)
def make_wire(y_offset):
    # Insulation
    # Starts at the back face (X=0) and extrudes backwards (-X direction)
    insulation = (
        cq.Workplane("YZ")
        .workplane(offset=0)
        .center(0, y_offset)
        .circle(wire_diameter / 2.0)
        .extrude(-wire_length)
    )
    
    # Stripped Conductor
    # Select the end face of the insulation and extrude the conductor further
    # Note: The workplane on the face with normal -X will align local Z with -X.
    # Therefore, a positive extrusion value extends the wire further in global -X.
    conductor = (
        insulation.faces("<X")
        .workplane()
        .circle(conductor_diameter / 2.0)
        .extrude(stripped_length)
    )
    
    return insulation.union(conductor)

# Create two wires offset symmetrically along the Y-axis
wire_1 = make_wire(wire_spacing / 2.0)
wire_2 = make_wire(-wire_spacing / 2.0)

# --- Final Assembly ---
# Combine the cartridge body with both wires
result = cartridge.union(wire_1).union(wire_2)