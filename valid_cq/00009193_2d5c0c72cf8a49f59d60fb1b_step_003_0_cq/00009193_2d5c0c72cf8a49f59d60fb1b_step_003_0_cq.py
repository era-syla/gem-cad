import cadquery as cq

# This script generates a simplified representation of the complex mechanical assembly shown in the image.
# The image appears to be a transmission or differential housing with various linkages.
# Due to the complexity and low resolution of the source image, this model approximates the
# main housing body and the linkage rods as separate conceptual components combined into one result.

def create_model():
    # ---------------------------------------------------------
    # Parameters
    # ---------------------------------------------------------
    housing_length = 80.0
    housing_width = 60.0
    housing_height = 70.0
    wall_thickness = 4.0
    
    # Main bore parameters
    main_bore_radius = 25.0
    
    # Linkage parameters (simulated floating parts to match image layout)
    linkage_offset_x = 150.0 # Far to the right as in image
    linkage_offset_y = 50.0
    linkage_height = 80.0
    rod_radius = 1.5

    # ---------------------------------------------------------
    # 1. Main Housing Body
    # ---------------------------------------------------------
    # Create the main block
    housing = (
        cq.Workplane("XY")
        .box(housing_length, housing_width, housing_height)
        .edges("|Z").fillet(5.0) # Soften edges
    )
    
    # Create the internal cavity (shell)
    # We subtract a smaller box from the main one, but typically complex housings are cast.
    # Here we will just drill the main bore to simulate the housing nature.
    
    # Main large bore through the Y axis (side to side)
    housing = housing.faces(">Y").workplane().hole(main_bore_radius * 2)

    # Add some complexity: Ribs/Bosses on the top
    top_feature = (
        cq.Workplane("XY")
        .workplane(offset=housing_height/2)
        .rect(housing_length * 0.8, housing_width * 0.6)
        .extrude(10)
    )
    housing = housing.union(top_feature)
    
    # Add side mounting flange/boss
    side_boss = (
        cq.Workplane("YZ")
        .workplane(offset=housing_length/2)
        .circle(15)
        .extrude(10)
    )
    housing = housing.union(side_boss)

    # Add a front feature (angled section often seen on differential housings)
    front_wedge = (
        cq.Workplane("XY")
        .workplane(offset=-housing_height/2)
        .center(0, -housing_width/2)
        .wedge(housing_length, housing_width/2, housing_height/2, 
               housing_length/2, housing_width/2, housing_length/2, housing_width/2)
    )
    # Positioning the wedge is tricky, let's use a simpler extrusion cut or add
    # Let's add a protruding block on the front face
    front_block = (
        cq.Workplane("XZ")
        .workplane(offset=-housing_width/2)
        .rect(40, 40)
        .extrude(-15)
    )
    housing = housing.union(front_block)

    # ---------------------------------------------------------
    # 2. Detail Features (approximation of the clutter)
    # ---------------------------------------------------------
    
    # Some smaller linkage arms attached to the main body
    arm_geo = (
        cq.Workplane("XY")
        .workplane(offset=housing_height/2 + 5)
        .center(-20, 0)
        .rect(10, 40)
        .extrude(5)
    )
    housing = housing.union(arm_geo)
    
    # A small cylindrical protrusion (sensor or bolt)
    sensor = (
        cq.Workplane("YZ")
        .workplane(offset=-housing_length/2)
        .center(10, 10)
        .circle(3)
        .extrude(-10)
    )
    housing = housing.union(sensor)

    # ---------------------------------------------------------
    # 3. The Distant Linkage (The "floating" rods in the image)
    # ---------------------------------------------------------
    # The image shows a group of thin rods quite far from the main body.
    
    # Rod 1
    rod1 = (
        cq.Workplane("XY")
        .center(linkage_offset_x, linkage_offset_y)
        .circle(rod_radius)
        .extrude(linkage_height)
    )
    
    # Rod 2 (slightly angled or offset)
    rod2 = (
        cq.Workplane("XY")
        .center(linkage_offset_x + 10, linkage_offset_y + 5)
        .circle(rod_radius)
        .extrude(linkage_height * 0.8)
    )
    
    # A connector at the bottom of the rods
    connector = (
        cq.Workplane("XY")
        .center(linkage_offset_x + 5, linkage_offset_y + 2.5)
        .rect(15, 10)
        .extrude(5)
    )
    
    linkage_assembly = rod1.union(rod2).union(connector)

    # ---------------------------------------------------------
    # Final Assembly
    # ---------------------------------------------------------
    result = housing.union(linkage_assembly)
    
    return result

# Generate the result
result = create_model()