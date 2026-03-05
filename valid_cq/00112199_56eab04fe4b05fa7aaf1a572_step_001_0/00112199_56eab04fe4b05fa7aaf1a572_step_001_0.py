import cadquery as cq

# --- Parameters ---
# Dimensions based on visual estimation of the provided image
prop_diameter = 200.0  # Total diameter of the propeller
hub_diameter = 18.0    # Diameter of the central hub cylinder
hub_height = 14.0      # Height/Thickness of the hub
shaft_hole = 5.0       # Diameter of the central shaft hole

# --- Helper Function ---
def create_blade_section(radius, chord, thickness, angle):
    """
    Creates a wire representing the airfoil cross-section at a specific radius.
    
    Args:
        radius (float): Distance from the propeller center.
        chord (float): Width of the blade at this section.
        thickness (float): Maximum thickness of the blade at this section.
        angle (float): Twist angle (pitch) in degrees.
        
    Returns:
        cq.Wire: A closed wire object positioned and rotated in 3D space.
    """
    # Create a workplane offset along the X axis (radial direction)
    # The cross-section is drawn on the YZ plane (normal to X)
    wp = cq.Workplane("YZ").workplane(offset=radius)
    
    # Define airfoil geometry in local coordinates (Y=Chord, Z=Thickness)
    # We center the twist axis roughly at 30% of the chord length from the Leading Edge
    le_loc = -chord * 0.3   # Leading Edge Y-coord
    te_loc = chord * 0.7    # Trailing Edge Y-coord
    
    # Control points for the spline approximation of an airfoil
    # Top camber point
    p_top = ((le_loc + te_loc) / 2, thickness * 0.55)
    # Bottom camber point (flatter than top)
    p_bot = ((le_loc + te_loc) / 2, -thickness * 0.25)
    
    # Construct the closed wire using splines
    # Sequence: LE -> Top Surface -> TE -> Bottom Surface -> LE
    section = (wp
               .moveTo(le_loc, 0)
               .spline([p_top, (te_loc, 0)], includeCurrent=True)
               .spline([p_bot, (le_loc, 0)], includeCurrent=True)
               .close()
               .wire()
              )
    
    # Rotate the wire around the local origin (Global X-axis) to apply twist
    return section.val().rotate((0,0,0), (1,0,0), angle)

# --- Blade Definition ---
# List of stations defining the blade shape: (Radius, Chord, Thickness, Angle)
# These parameters create the "spoon" shape and twist distribution seen in the image.
stations = [
    (hub_diameter/2 - 1.0, 10.0, 10.0, 60.0), # Root section (buried inside hub)
    (15.0, 14.0, 6.0, 50.0),                  # Neck transition
    (35.0, 24.0, 4.0, 32.0),                  # Widest part of the blade
    (60.0, 19.0, 2.5, 20.0),                  # Mid-span
    (85.0, 11.0, 1.5, 12.0),                  # Tapering towards tip
    (prop_diameter/2, 2.0, 0.5, 10.0)         # Tip section
]

# --- Model Construction ---

# 1. Generate cross-section wires for one blade
blade_wires = []
for s in stations:
    blade_wires.append(create_blade_section(*s))

# 2. Loft the wires to create the first blade geometry
#    We accumulate wires into a Workplane to perform the loft
blade_builder = cq.Workplane("XY")
for w in blade_wires:
    blade_builder = blade_builder.add(w)

blade1 = blade_builder.toPending().loft()

# 3. Create the second blade by rotating a copy of the first blade 180 degrees around Z
blade2 = blade1.rotate((0,0,0), (0,0,1), 180)

# 4. Create the central hub
#    A cylinder centered vertically at Z=0
hub = (cq.Workplane("XY")
       .circle(hub_diameter / 2)
       .extrude(hub_height)
       .translate((0, 0, -hub_height / 2))
      )

# 5. Combine Hub and Blades into a single solid
propeller_solid = hub.union(blade1).union(blade2)

# 6. Cut the shaft mounting hole through the center
result = (propeller_solid
          .faces(">Z")
          .workplane()
          .circle(shaft_hole / 2)
          .cutThruAll()
         )