import cadquery as cq

# --- Parameter Definitions ---

# Object 1: The Bulbous Turnbuckle/Vase Shape
bulb_radius = 12.0      # Radius of the central bulbous part
rim_radius = 8.0        # Radius of the top and bottom rims
rim_height = 2.0        # Thickness of the rims
neck_radius = 5.0       # Radius of the narrow neck connecting rim to bulb
neck_height = 2.0       # Height of the neck
total_bulb_height = 20.0 # Approximate height of the central bulb section
hole_diameter_1 = 4.0   # Diameter of the through hole

# Object 2: The Hexagonal Prism
hex_circumradius = 5.0  # Distance from center to a vertex of the hexagon
hex_height = 60.0       # Height of the hexagonal pillar
hole_diameter_2 = 4.0   # Diameter of the through hole
spacing = 40.0          # Distance between the two objects

# --- Construction ---

# 1. Create the Bulbous Shape
# We will create this by revolving a profile.
# The profile consists of a central arc and straight lines for the rims/necks.

def create_bulb_shape():
    # Define vertical positions relative to center (0,0,0)
    h_bulb_half = total_bulb_height / 2
    h_neck_top = h_bulb_half + neck_height
    h_rim_top = h_neck_top + rim_height
    
    # Create the solid using workplane operations
    # Bottom Rim
    s1 = cq.Workplane("XY").center(0, 0).workplane(offset=-h_rim_top).circle(rim_radius).extrude(rim_height)
    
    # Bottom Neck
    s2 = cq.Workplane("XY").center(0, 0).workplane(offset=-(h_neck_top)).circle(neck_radius).extrude(neck_height)
    
    # Central Bulb
    # We create a sphere and cut off the top and bottom to make it merge nicely,
    # or create a revolution. A sphere is simplest for a "bulbous" look.
    # Let's adjust the sphere radius to match the height somewhat.
    # To get a height of 20 with flat tops/bottoms, we need a sphere bigger than 10 radius cut at +/- 10.
    # Let's just use a sphere and intersect it with a cylinder or box to flatten ends?
    # Actually, simpler approach: Revolve a spline.
    
    # Alternative: Revolve a profile.
    pts = [
        (0, -h_rim_top), (rim_radius, -h_rim_top), (rim_radius, -h_neck_top), # Bottom Rim outer edge
        (neck_radius, -h_neck_top), (neck_radius, -h_bulb_half),              # Bottom Neck and start of bulb
        # Arc for bulb? Let's use a spline for smooth transition or a 3-point arc
        # Middle of bulb is at (bulb_radius, 0)
        (neck_radius, h_bulb_half),                                            # End of bulb
        (neck_radius, h_neck_top), (rim_radius, h_neck_top),                   # Top Neck and start of rim
        (rim_radius, h_rim_top), (0, h_rim_top)                                # Top Rim outer edge
    ]
    
    # Let's refine the bulb part. It looks like a sphere section.
    # Sphere radius R. Cut at z = +/- h_bulb_half.
    # R^2 = x^2 + z^2. At z=h_bulb_half, x=neck_radius.
    # R^2 = neck_radius^2 + h_bulb_half^2 = 5^2 + 10^2 = 125. R = sqrt(125) approx 11.18
    sphere_R = (neck_radius**2 + h_bulb_half**2)**0.5
    
    # Let's construct it piece-wise to ensure validity.
    part_rim_bot = cq.Workplane("XY").workplane(offset=-h_rim_top).circle(rim_radius).extrude(rim_height)
    part_neck_bot = cq.Workplane("XY").workplane(offset=-h_neck_top).circle(neck_radius).extrude(neck_height)
    
    # The central bulb as a sphere intersected with a slab to flatten top/bottom
    part_bulb = cq.Workplane("XY").sphere(sphere_R)
    # Cut the top and bottom of the sphere flat to attach necks
    # A large box cut is easy, or intersecting with a cylinder of height total_bulb_height
    cutter = cq.Workplane("XY").workplane(offset=-h_bulb_half).rect(sphere_R*3, sphere_R*3).extrude(total_bulb_height, combine=False)
    part_bulb = part_bulb.intersect(cutter)

    part_neck_top = cq.Workplane("XY").workplane(offset=h_bulb_half).circle(neck_radius).extrude(neck_height)
    part_rim_top = cq.Workplane("XY").workplane(offset=h_neck_top).circle(rim_radius).extrude(rim_height)

    solid = part_rim_bot.union(part_neck_bot).union(part_bulb).union(part_neck_top).union(part_rim_top)
    
    # Add the through hole
    solid = solid.faces(">Z").workplane().hole(hole_diameter_1)
    
    return solid

bulb_obj = create_bulb_shape()

# 2. Create the Hexagonal Prism
# This is a simple extrusion of a polygon
hex_obj = (cq.Workplane("XY")
           .polygon(nSides=6, diameter=hex_circumradius*2)
           .extrude(hex_height)
           .faces(">Z").workplane()
           .hole(hole_diameter_2)
           )

# Move the hex object to the side to match the image layout
# In the image, the bulb is low and to the left (ish), the hex is tall and to the right.
# We'll shift the hex object along X.
hex_obj = hex_obj.translate((spacing, 0, -15)) # -15 to align roughly with the bottom visually if desired, or just keep at Z=0 base.
# Looking at the image, the bulb is floating or sitting on a plane. The hex is also sitting there.
# Let's align their bottoms.
# Bulb bottom is at z = -(h_bulb_half + neck_height + rim_height) = -(10 + 2 + 2) = -14
# Hex bottom is at z = 0 (before translate).
# Let's move hex to z = -14.
hex_obj = hex_obj.translate((0, 0, -14))

# Combine both into the result
result = bulb_obj.union(hex_obj)

# Export (optional, for verification)
# cq.exporters.export(result, "result.step")