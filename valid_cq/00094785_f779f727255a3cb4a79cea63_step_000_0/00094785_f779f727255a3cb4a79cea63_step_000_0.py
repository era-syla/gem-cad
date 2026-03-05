import cadquery as cq

# --- Parameters ---
# Top Frame Dimensions
top_side = 100.0          # Side length of the top square
frame_height = 5.0        # Thickness of the plate extrusions
beam_thickness = 3.0      # Thickness of the structural beams
top_fillet = 5.0          # Fillet radius for top corners
top_hub_radius = 6.0      # Radius of the central hub

# Bottom Frame Dimensions
bottom_radius = 80.0      # Radius of the bottom sector
bottom_angle = 90.0       # Angle of the sector (approx 90 degrees)
bottom_hub_radius = 12.0  # Radius of the bottom hub

# Vertical Connection
rod_length = 120.0        # Distance between the two frame levels
rod_radius = 3.0          # Radius of the vertical connecting rod

# --- Top Frame Construction ---
# Define the workplane for the top frame
top_plane = cq.Workplane("XY").workplane(offset=rod_length)

# 1. Outer Rim with Fillets
# Create a solid square, fillet corners, then cut the interior to make a frame
top_rim_solid = (
    top_plane
    .rect(top_side, top_side)
    .extrude(frame_height)
    .edges("|Z")
    .fillet(top_fillet)
)

top_rim_cutout = (
    top_plane
    .rect(top_side - 2*beam_thickness, top_side - 2*beam_thickness)
    .extrude(frame_height)
)

top_rim = top_rim_solid.cut(top_rim_cutout)

# 2. Cross Beams (X-Shape)
# Diagonal length sufficient to cross the frame
diag_length = top_side * 1.5
beam_x1 = (
    top_plane
    .rect(diag_length, beam_thickness)
    .extrude(frame_height)
    .rotate((0,0,1), (0,0,0), 45)
)

beam_x2 = (
    top_plane
    .rect(diag_length, beam_thickness)
    .extrude(frame_height)
    .rotate((0,0,1), (0,0,0), -45)
)

# 3. Top Hub
top_hub = top_plane.circle(top_hub_radius).extrude(frame_height)

# Union the top components
top_assembly = top_rim.union(beam_x1).union(beam_x2).union(top_hub)

# 4. Add Holes
# Center hole
top_assembly = top_assembly.faces(">Z").workplane().circle(1.5).cutThruAll()

# Corner holes
hole_offset = (top_side / 2) - (top_fillet / 2) - 1.0
top_assembly = (
    top_assembly.faces(">Z").workplane()
    .pushPoints([
        (hole_offset, hole_offset), 
        (hole_offset, -hole_offset), 
        (-hole_offset, hole_offset), 
        (-hole_offset, -hole_offset)
    ])
    .circle(1.5).cutThruAll()
)


# --- Bottom Frame Construction ---
# Define the workplane for the bottom frame at Z=0
bot_plane = cq.Workplane("XY")

# 1. Bottom Hub
bot_hub = bot_plane.circle(bottom_hub_radius).extrude(frame_height)

# Add pattern of 4 holes to bottom hub
bot_hub = (
    bot_hub.faces(">Z").workplane()
    .pushPoints([(7, 0), (-7, 0), (0, 7), (0, -7)])
    .circle(1.6).cutThruAll()
)

# 2. Outer Arc Rim
# Create a profile on XZ plane shifted by radius, then revolve
rim_profile = (
    cq.Workplane("XZ")
    .moveTo(bottom_radius, frame_height / 2)
    .rect(beam_thickness, frame_height)
)

# Revolve 90 degrees and rotate to center on X-axis (-45 to +45 degrees)
bot_rim = (
    rim_profile
    .revolve(90, (0,0,0), (0,0,1))
    .rotate((0,0,1), (0,0,0), -45)
)

# 3. Radial Spokes
# Base spoke extending along X-axis from center
spoke_length = bottom_radius
spoke_base = (
    bot_plane
    .rect(spoke_length, beam_thickness) # Centered at origin
    .extrude(frame_height)
    .translate((spoke_length / 2, 0, 0)) # Shift so it starts at origin
)

# Create 3 spokes: Center, Left (-45), Right (+45)
spoke_c = spoke_base
spoke_l = spoke_base.rotate((0,0,1), (0,0,0), -45)
spoke_r = spoke_base.rotate((0,0,1), (0,0,0), 45)

# Union the bottom components
bot_assembly = bot_hub.union(bot_rim).union(spoke_c).union(spoke_l).union(spoke_r)


# --- Vertical Rod ---
rod = (
    cq.Workplane("XY")
    .circle(rod_radius)
    .extrude(rod_length + frame_height) # Extrude up to top frame
)


# --- Final Assembly ---
result = top_assembly.union(bot_assembly).union(rod)