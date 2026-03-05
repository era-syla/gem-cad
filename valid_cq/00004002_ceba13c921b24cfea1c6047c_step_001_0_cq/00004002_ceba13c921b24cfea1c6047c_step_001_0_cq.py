import cadquery as cq

# --- Parametric Dimensions ---

# Main Hexagonal Rod
hex_flat_size = 10.0   # Distance across flats of the hexagon
hex_length = 150.0     # Length of the main hexagonal rod
hex_end_turn_dia = 6.0 # Diameter of the turned down end
hex_end_turn_len = 10.0 # Length of the turned down end

# Side Rails (Thin Rods)
rail_diameter = 2.0    # Diameter of the thin rails
rail_length = 150.0    # Length of the rails
rail_offset_y = 8.0    # Vertical offset from center
rail_offset_x = 8.0    # Horizontal offset from center (approximate)

# Small Bushing/Bearing
bushing_od = 8.0       # Outer diameter
bushing_id = 4.0       # Inner diameter
bushing_width = 4.0    # Width of the bushing
bushing_pos_x = 0.0    # X Position relative to origin
bushing_pos_y = -15.0  # Y Position relative to origin
bushing_pos_z = hex_length - 20.0 # Z position

# Long Thin Rod (Actuator/Screw)
long_rod_dia = 3.0     # Diameter of the long thin rod
long_rod_len = 250.0   # Total length
long_rod_z_start = hex_length - 40.0 # Where it starts relative to hex rod

# --- Modeling ---

# 1. Main Hexagonal Body
# Using a Polygon to create the hexagon profile
# radius = flat_size / sqrt(3) for vertex radius, but CQ usually takes circumradius for polygon? 
# Actually, cq.Workplane("XY").polygon(nSides, diameter) specifies the diameter of the circumcircle.
# For a hex, flat-to-flat distance (d) relates to circumdiameter (D) by d = D * cos(30) = D * sqrt(3)/2
# So D = d / (sqrt(3)/2)
import math
circum_diameter = hex_flat_size / (math.sqrt(3)/2)

main_hex = (
    cq.Workplane("XY")
    .polygon(6, circum_diameter)
    .extrude(hex_length)
)

# Create the turned down end on the hex rod (cylindrical cut or join)
# It looks like a cylindrical stub at the end.
end_stub = (
    cq.Workplane("XY")
    .workplane(offset=hex_length)
    .circle(hex_end_turn_dia / 2)
    .extrude(hex_end_turn_len)
)

main_body = main_hex.union(end_stub)


# 2. Side Rails
# There appear to be two parallel rails or rods. 
# One is clearly visible alongside the hex rod, the other seems to be the very long one extending out.
# Looking closely at the image, there is one separate rod floating parallel, 
# and one very long rod extending axially from the center of the hex rod (or through it).

# Let's model the separate parallel rod.
parallel_rod = (
    cq.Workplane("XY")
    .center(rail_offset_x, rail_offset_y)
    .circle(rail_diameter / 2)
    .extrude(rail_length * 0.8) # Slightly shorter in the image
)

# 3. The Long Axial Rod
# This looks like it goes through the center or extends from the end.
long_rod = (
    cq.Workplane("XY")
    .workplane(offset=long_rod_z_start) # Starts somewhat inside or at a specific point
    .circle(long_rod_dia / 2)
    .extrude(long_rod_len)
)

# 4. Small Bushing/Collar
# This is floating separately in the image.
bushing = (
    cq.Workplane("XY")
    .workplane(offset=bushing_pos_z)
    .center(bushing_pos_x, bushing_pos_y)
    .circle(bushing_od / 2)
    .circle(bushing_id / 2) # Create a hole
    .extrude(bushing_width)
)

# --- Assembly ---

# Combine all solid parts into one object for the 'result'
result = main_body.union(parallel_rod).union(long_rod).union(bushing)

# If you prefer an Assembly object (which keeps parts separate colors/names):
# assembly = cq.Assembly()
# assembly.add(main_body, name="HexRod", color=cq.Color("silver"))
# assembly.add(parallel_rod, name="SideRail", color=cq.Color("gray"))
# assembly.add(long_rod, name="LongRod", color=cq.Color("gray"))
# assembly.add(bushing, name="Bushing", color=cq.Color("darkgray"))
# result = assembly # But the prompt asks for a 'result' variable usually implying a solid or compound.