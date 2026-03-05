import cadquery as cq

# Define parameters for the I-beam
# These dimensions are chosen to represent a typical structural I-beam shape
length = 500.0   # Total length of the beam
height = 50.0    # Total height of the I-section (web height + 2 * flange thickness)
width = 30.0     # Width of the flanges
web_thickness = 4.0     # Thickness of the vertical web
flange_thickness = 4.0  # Thickness of the horizontal flanges

# Create the I-beam profile sketch
# We will draw half of the profile and mirror it, or draw the full profile using a polyline
# Here, drawing the full profile centered on the origin is straightforward.

def create_ibeam(length, height, width, web_thickness, flange_thickness):
    # Calculate half dimensions for easier coordinate definition
    h_half = height / 2.0
    w_half = width / 2.0
    web_half = web_thickness / 2.0
    
    # Define points for the I-profile
    # Starting from top-right corner and going counter-clockwise
    pts = [
        (w_half, h_half),               # Top-right outer
        (-w_half, h_half),              # Top-left outer
        (-w_half, h_half - flange_thickness), # Top-left inner
        (-web_half, h_half - flange_thickness), # Top web start
        (-web_half, -(h_half - flange_thickness)), # Bottom web end
        (-w_half, -(h_half - flange_thickness)), # Bottom-left inner
        (-w_half, -h_half),             # Bottom-left outer
        (w_half, -h_half),              # Bottom-right outer
        (w_half, -(h_half - flange_thickness)),  # Bottom-right inner
        (web_half, -(h_half - flange_thickness)), # Bottom web end (right side)
        (web_half, h_half - flange_thickness),    # Top web start (right side)
        (w_half, h_half - flange_thickness),      # Top-right inner
        (w_half, h_half)                # Closing the loop
    ]
    
    # Create the profile and extrude
    # We create the profile on the YZ plane so the length runs along the X axis
    result = (
        cq.Workplane("YZ")
        .polyline(pts)
        .close()
        .extrude(length)
    )
    
    # Center the beam along the X-axis (optional, but good practice)
    # The extrusion goes from 0 to length, so we translate back by length/2
    result = result.translate((-length / 2.0, 0, 0))
    
    return result

# Generate the model
result = create_ibeam(length, height, width, web_thickness, flange_thickness)