import cadquery as cq

# Parametric dimensions
num_columns = 16
num_rows = 2
pitch_x = 2.54      # Standard pitch spacing (approx 0.1 inch)
pitch_y = 2.54
pin_diameter = 0.6  # Diameter of the cylindrical pins
pin_height = 6.0    # Height of the pins

# Create the model
# 1. Start with a workplane on the XY plane
# 2. Create a rectangular array of points corresponding to the pin locations
# 3. Draw a circle at each point
# 4. Extrude all circles simultaneously to create the pins
result = (
    cq.Workplane("XY")
    .rarray(
        xSpacing=pitch_x, 
        ySpacing=pitch_y, 
        xCount=num_columns, 
        yCount=num_rows, 
        center=True
    )
    .circle(pin_diameter / 2.0)
    .extrude(pin_height)
)