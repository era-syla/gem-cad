import cadquery as cq

# Parametric dimensions
main_diameter = 10.0  # Diameter of the main long cylinder
main_length = 100.0   # Length of the main long cylinder
pin_diameter = 4.0    # Diameter of the smaller pin at the bottom
pin_length = 10.0     # Length of the smaller pin

# Create the main cylinder
# We'll center it on the XY plane for convenience, but build it vertically along Z.
main_body = cq.Workplane("XY").circle(main_diameter / 2).extrude(main_length)

# Create the pin
# We select the bottom face of the main cylinder (at Z=0 since we extruded up)
# Then we draw the smaller circle and extrude it downwards (negative direction)
# Or we can simply extrude from the origin downwards if that's easier.
# Let's attach to the bottom face (Z=0) and extrude down.
# Note: Since the first extrude went from Z=0 to Z=main_length, the "bottom" face is at Z=0.
# However, CadQuery's direction can be tricky.
# Let's try explicit positioning for clarity.

# Alternative approach: Build two cylinders and union them.
# Cylinder 1: Main body
part1 = cq.Workplane("XY").circle(main_diameter / 2).extrude(main_length)

# Cylinder 2: Pin
# We want this to be at the bottom. Since part1 starts at Z=0 and goes up to Z=100,
# part2 should start at Z=0 and go down to Z=-10.
part2 = cq.Workplane("XY").circle(pin_diameter / 2).extrude(-pin_length)

# Combine the parts
result = part1.union(part2)

# Export or visualization
if __name__ == "__main__":
    try:
        from cadquery import exporters
        # Exporters/visualizers might be used here in a real environment
        pass
    except ImportError:
        pass