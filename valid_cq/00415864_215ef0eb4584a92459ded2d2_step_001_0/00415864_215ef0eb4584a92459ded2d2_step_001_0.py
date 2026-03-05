import cadquery as cq

# Parametric dimensions
length = 120.0        # Total length of the object
end_width = 30.0      # Width of the rectangular profile at the ends
end_height = 10.0     # Thickness of the profile
mid_width = 60.0      # Width of the profile in the middle (bulge)
mid_elevation = 25.0  # Height of the arch/hump in the middle

# Create the model using a loft operation
# We define three cross-sections (start, middle, end) and loft between them
result = (
    cq.Workplane("YZ")  # Start on the YZ plane (Extruding along X axis)
    .rect(end_width, end_height)  # 1. Start Profile at X=0
    .workplane(offset=length / 2.0)
    .center(0, mid_elevation)     # Shift Z up for the middle section
    .rect(mid_width, end_height)  # 2. Middle Profile at X=L/2 (Wider and Higher)
    .workplane(offset=length / 2.0)
    .center(0, -mid_elevation)    # Shift Z back down for the end section
    .rect(end_width, end_height)  # 3. End Profile at X=L
    .loft(combine=True)           # Create a smooth solid through the profiles
)