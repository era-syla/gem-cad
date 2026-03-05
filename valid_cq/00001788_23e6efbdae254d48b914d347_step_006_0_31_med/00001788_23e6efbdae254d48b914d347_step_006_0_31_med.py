import cadquery as cq

# Parameters for the base plate
thickness = 2.0
w_left = 80.0
w_right = 90.0
w_total = w_left + w_right
h_left = 100.0
h_right = 140.0
fillet_r = 3.0

# Define the outer profile
profile_pts = [
    (0, 0),
    (w_total, 0),
    (w_total, h_right),
    (w_left, h_right),
    (w_left, h_left),
    (0, h_left)
]

# Create the base solid and fillet the vertical edges
base = (cq.Workplane("XY")
        .polyline(profile_pts)
        .close()
        .extrude(thickness)
        .edges("|Z").fillet(fillet_r))

# Create a workplane on the top face for features
wp = base.faces(">Z").workplane()

# Screen window (Left region)
wp = wp.pushPoints([(w_left / 2, 65)]).rect(55, 35).cutBlind(-thickness)

# Small square/rectangular cutouts (Right region)
wp = wp.pushPoints([(w_left + 30, 110)]).rect(15, 20).cutBlind(-thickness)
wp = wp.pushPoints([(w_left + 60, 115)]).rect(8, 8).cutBlind(-thickness)

# Bottom edge notch
wp = wp.pushPoints([(w_left / 2 + 5, 0)]).rect(16, 12).cutBlind(-thickness)

# Vertical ventilation slots (Left region)
left_slot_pts = [(16 + i * 12, 26) for i in range(5)]
wp = wp.pushPoints(left_slot_pts).slot2D(24, 5, 90).cutBlind(-thickness)

# Vertical ventilation slots (Right region)
right_slot_pts = [(w_left + 15 + i * 15, 45) for i in range(5)]
wp = wp.pushPoints(right_slot_pts).slot2D(46, 6, 90).cutBlind(-thickness)

# Coordinates for all mounting holes
hole_pts = [
    # Left region corners
    (4, 4), (4, h_left - 4), (w_left - 4, h_left - 4), (w_left - 4, 4),
    # Right region corners & edges
    (w_left + 4, 4), (w_total - 4, 4), (w_total - 4, h_right / 2),
    (w_total - 4, h_right - 4), (w_left + 4, h_right - 4),
    # Holes around the left screen window
    (10, 80), (w_left - 10, 80), (10, 50), (w_left - 10, 50),
    # Additional visible structural holes
    (w_left - 20, 42), (18, 42), (w_left + 4, h_left + 4)
]

# Apply countersunk holes across defined points
result = wp.pushPoints(hole_pts).cskHole(2.5, 4.5, 90)