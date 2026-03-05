import cadquery as cq

# Parametric dimensions
plate_height = 200.0
plate_width = 120.0
plate_thickness = 10.0
hole_diameter = 4.0

# Hole pattern definition
# Based on the visual layout, there are 10 holes arranged symmetrically
# Coordinate system assumption: Center of the plate is (0,0)
# Holes seem to be arranged in rows. Let's approximate their positions relative to center.

# Top row (narrower spread)
y_top = plate_height * 0.35
x_top = plate_width * 0.25

# Second row (wider spread)
y_second = plate_height * 0.20
x_second = plate_width * 0.35

# Third row (single center hole)
y_third = plate_height * 0.10
x_third = 0.0

# Fourth row (wider spread)
y_fourth = -plate_height * 0.05
x_fourth = plate_width * 0.35

# Fifth row (single center hole)
y_fifth = -plate_height * 0.20
x_fifth = 0.0

# Sixth row (narrower spread)
y_sixth = -plate_height * 0.35
x_sixth = plate_width * 0.35

# List of hole coordinates (x, y)
hole_locations = [
    # Top Row
    (-x_top, y_top), (x_top, y_top),
    # Second Row
    (-x_second, y_second), (x_second, y_second),
    # Third Row (Center)
    (x_third, y_third),
    # Fourth Row
    (-x_fourth, y_fourth), (x_fourth, y_fourth),
    # Fifth Row (Center)
    (x_fifth, y_fifth),
    # Bottom Row
    (-x_sixth, y_sixth) # Based on image, seems asymmetric or bottom right missing? 
    # Looking closely at the image, let's re-evaluate the pattern.
    # It looks like a standard mounting plate.
    # Top row: 2 holes
    # Second row: 2 holes (wider)
    # Center hole
    # Fourth row: 2 holes (wider)
    # Fifth row: 1 hole center
    # Bottom left hole visible.
    
    # Let's refine the list based strictly on visual markers:
    # 1. Top Right
    # 2. Top Left
    # 3. Upper Mid Right
    # 4. Upper Mid Left
    # 5. Center
    # 6. Lower Mid Right
    # 7. Lower Mid Left
    # 8. Lower Center
    # 9. Bottom Left
    # 10. Bottom Right seems missing or obscured, but likely exists for symmetry.
    # However, looking extremely closely at the specific pattern:
    # Top Row: 2 holes
    # Row 2: 2 holes wider
    # Row 3: 1 hole center
    # Row 4: 2 holes wider
    # Row 5: 1 hole center
    # Row 6: 1 hole on the left? It looks like there's a hole at bottom left.
    
    # Let's build a standard symmetric pattern and assume the render lighting hides one, 
    # or build exactly what is seen.
    # Visible holes:
    # Top: (-30, 70), (30, 70)
    # Mid-Upper: (-45, 35), (45, 35)
    # Center: (0, 10)
    # Mid-Lower: (-45, -15), (45, -15)
    # Lower Center: (0, -40)
    # Bottom Left: (-45, -65)
    
    # Re-evaluating the image coordinates more precisely visually:
    # Let's assume w=100, h=160 for ease of ratio calculation.
    # Holes:
    # 1. ( 25,  60) - Top Right
    # 2. (-25,  60) - Top Left
    # 3. ( 40,  30) - Mid Top Right
    # 4. (-40,  30) - Mid Top Left
    # 5. (  0,   5) - Centerish
    # 6. ( 40, -25) - Mid Low Right
    # 7. (-40, -25) - Mid Low Left
    # 8. (  0, -50) - Low Center
    # 9. (-40, -70) - Bottom Left
]

# Let's stick to a clean coordinate list that matches the visual distribution
pts = [
    ( 30,  70), (-30,  70),  # Top row
    ( 45,  35), (-45,  35),  # Second row
    (  0,  10),              # Center
    ( 45, -15), (-45, -15),  # Fourth row
    (  0, -40),              # Fifth row
    (-45, -65)               # Bottom left
]

# Create the base plate
result = (
    cq.Workplane("XY")
    .box(plate_width, plate_height, plate_thickness)
    .faces(">Z")
    .workplane()
    .pushPoints(pts)
    .hole(hole_diameter)
)