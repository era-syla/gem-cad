import cadquery as cq

# Dimensions
plate_thickness = 2.0
boss_radius = 3.5
boss_length = 8.0
hole_diameter = 2.5

# Generate the main organic profile using splines
# The profile is defined as a series of points simulating the tribal flame shape
# We use separate spline commands to create sharp corners at the flame tips
sketch = (
    cq.Workplane("XY")
    .moveTo(0, 2.0)  # Start at the top intersection with the boss
    
    # First Flame (Top Left)
    .spline([(8, 15)], includeCurrent=True)   # Curve to tip
    .spline([(14, 4)], includeCurrent=True)   # Curve to valley
    
    # Second Flame (Top Middle)
    .spline([(26, 18)], includeCurrent=True)  # Curve to tip
    .spline([(32, 3)], includeCurrent=True)   # Curve to valley
    
    # Third Flame / Transition (Top Right)
    .spline([(45, 12)], includeCurrent=True)  # Curve to tip
    .spline([(50, 1)], includeCurrent=True)   # Curve to spine
    
    # Tail Tip
    .spline([(90, -10)], includeCurrent=True) # Long sweep to the tail point
    
    # Bottom Curve (The "Belly")
    # A continuous smooth curve back to the boss
    .spline([(60, -8), (20, -12), (8, -8), (0, -2.0)], includeCurrent=True)
    .close()
)

# Extrude the 2D profile to create the solid plate
plate = sketch.extrude(plate_thickness)

# Create the cylindrical hinge boss
# Oriented along the Y-axis, centered relative to the plate thickness
boss = (
    cq.Workplane("XZ")
    .workplane(offset=-boss_length / 2.0)
    .moveTo(0, plate_thickness / 2.0)
    .circle(boss_radius)
    .extrude(boss_length)
)

# Combine the plate and the boss
result = plate.union(boss)

# Cut the pivot hole through the boss
result = (
    result
    .faces("<Y")  # Select the negative Y face of the boss
    .workplane()
    .moveTo(0, plate_thickness / 2.0)
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)