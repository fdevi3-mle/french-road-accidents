from src.franums import FileTypeEnum, CategoryBaseEnum


class Old_Road_Accident_Enum(FileTypeEnum):
    '''Collection of all the categories for file type 'vehicle.csv' '''

    class Num_Acc(CategoryBaseEnum):
        '''The Index/Number of the Crash follows the pattern yyyyxxxxx and is the index column'''

    class id_vehicule(CategoryBaseEnum):
        '''The vehicle id  in terms of xxx-xxx'''

    class catv(CategoryBaseEnum):  # catv Vehicle Category
        '''The Category of Vehicle involved in the crash'''
        UNDETERMINED = 0
        BICYCLE = 1
        MOPED_LESS_EQUAL_50CC = 2
        MICROCAR = 3
        TOURISM_VEHICLE = 7
        UTILITY_VEHICLE_PTAC_1_5T_3_5T = 10  # 1.5<PTAC<3.5
        HEAVY_TRUCK_PTAC_3_5T_7_5T = 13
        HEAVY_TRUCK_PTAC_OVER_7_5T = 14
        HEAVY_TRUCK_OVER_3_5T_WITH_TRAILER = 15
        TRACTOR_ONLY = 16
        TRACTOR_WITH_SEMI_TRAILER = 17
        SPECIAL_VEHICLE = 20
        AGRICULTURAL_TRACTOR = 21
        SCOOTER_LESS_EQUAL_50CC = 30
        MOTORCYCLE_50CC_125CC = 31
        SCOOTER_50CC_125CC = 32
        MOTORCYCLE_OVER_125CC = 33
        SCOOTER_OVER_125CC = 34
        LIGHT_QUAD_LESS_EQUAL_50CC = 35
        HEAVY_QUAD_OVER_50CC = 36
        BUS = 37
        COACH = 38
        TRAIN = 39
        TRAMWAY = 40
        THREE_WHEELED_VEHICLE_LESS_EQUAL_50CC = 41
        THREE_WHEELED_VEHICLE_50CC_125CC = 42
        THREE_WHEELED_VEHICLE_OVER_125CC = 43
        MOTORIZED_PERSONAL_TRANSPORT = 50
        NON_MOTORIZED_PERSONAL_TRANSPORT = 60
        OTHER_VEHICLE = 99

    class obs(CategoryBaseEnum):  # obs Static ObstacleHit
        ''' The Static/Stationary Obstacle Hit'''
        UNKNOWN = 0
        PARKED_VEHICLE = 1
        TREE_ON_ROADSIDE = 2
        METAL_BARRIER = 3
        CONCRETE_BARRIER = 4
        OTHER_BARRIER = 5
        BUILDING_WALL_BRIDGE_PIER = 6  # BUILDING, WALL OR BRIDGE PIER
        VERTICAL_SIGNPOST_OR_EMERGENCY_CALLBOX = 7
        POLE = 8
        URBAN_FURNITURE = 9
        PARAPET = 10
        REFUGE_ISLAND_BOLLARD = 11  # THE ROAD ISLAND / BOLLARD
        SIDEWALK = 12  # SIDEWALK OR CURB
        DITCH = 13  # DITCH OR EMBANKMENT
        OTHER_OBS_ON_ROADWAY = 14
        OTHER_OBS_ON_SIDEWALK = 15
        ROADWAY_EXIT_WITOUT_OBSTACLES = 16
        AQUEDUCT_HEAD = 17

    class obsm(CategoryBaseEnum):  # obsm #Mobile obstacle hit
        '''The Dynamic Obstacle Hit'''
        UNKNOWN = 0
        PEDESTRIAN = 1
        VEHICLE = 2
        RAIL_VEHICLE = 3
        ANIMAL_DOMESTIC = 4
        ANIMAL_WILD = 5
        OTHER = 9

    class choc(CategoryBaseEnum):  # choc Initial Point of Impact
        '''The Initial Point of Impact of the crash'''
        UNKNOWN = 0
        FRONT = 1
        FRONT_LEFT = 2
        FRONT_RIGHT = 3
        REAR = 4
        REAR_RIGHT = 5
        REAR_LEFT = 6
        SIDE_LEFT = 7
        SIDE_RIGHT = 8
        MULTIPLE = 9

    class manv(CategoryBaseEnum):  # manv , Main action before crash
        '''The Main Action performed by the user before the crash'''
        UNKNOWN = 0
        CIRCULATING_NO_DIRECTION_CHANGE = 1
        CIRCULATING_SAME_DIRECTION = 2  # SAME DIRECTION SAME LANE
        CIRCULATION_BETWEEN_2_LANES = 3
        CIRCULATING_REVERSING = 4
        CIRCULATING_AGAINTS_FLOW_TRAFFIC = 5
        CIRCULATING_CROSSING_MEDIAN_STRIP = 6
        CIRCULATING_IN_BUSLANE_SAME_DIRECTION = 7
        CIRCULATING_IN_BUSLANE_OPP_DIRECTION = 8
        CIRCULATING_INSERTION = 9
        CIRCULATING_TURNING_AROUND_CARRIAGE_WAY = 10
        CHANGING_LANE_LEFT = 11
        CHANGING_LANE_RIGHT = 12
        DEPORT_LEFT = 13
        DEPORT_RIGHT = 14
        TURNING_LEFT = 15
        TURNING_RIGHT = 16
        OVERTAKING_LEFT = 17
        OVERTAKING_RIGHT = 18
        # VARIOUS S
        CROSSING_ROAD = 19
        PARKING_ACTION = 20
        AVOIDANCE_ACTION = 21
        DOOR_OPENED = 22
        STOP_NO_PARKING = 23
        PARKED_WITH_PASS = 24  # PARKED WITH PASSANGERS
        DRIVING_SIDEWALK = 25
        OTHER_ACTIONS = 26

    class motor(CategoryBaseEnum):  # motor
        '''The Type of Motor(In terms of fuel type) involved in the crash'''
        UNKNOWN = 0
        CONVENTIONAL_FUEL = 1  # PETROL, DIESEL ,ETC
        HYBRID_ELECTRIC = 2
        ELECTRIC = 3
        HYDROGEN = 4
        HUMAN_POWERED = 5
        OTHER = 6

    class catr(CategoryBaseEnum):
        '''Category of the road'''
        MOTORWAY = 1
        NATIONAL_ROAD = 2
        DEPARTMENTAL_ROAD = 3
        MUNICIPAL_ROAD = 4
        OFF_NETWORK = 5
        PARKING_AREA = 6
        URBAN_METROPOLE_ROAD = 7
        OTHER = 9

    class circ(CategoryBaseEnum):
        '''Traffic regime:'''
        NOT_PROVIDED = -1
        ONE_WAY = 1
        BIDIRECTIONAL = 2
        SEPARATE_LANES = 3
        VARIABLE_LANE = 4

    class surf(CategoryBaseEnum):
        '''Surface condition'''
        NOT_PROVIDED = -1
        NORMAL = 1
        WET = 2
        PUDDLES = 3
        FLOODED = 4
        SNOWY = 5
        MUDDY = 6
        ICY = 7
        GREASE = 8
        OTHER = 9

    class infra(CategoryBaseEnum):
        '''Development - Infrastructure:'''
        NOT_PROVIDED = -1
        NONE = 0
        UNDERGROUND = 1
        BRIDGE = 2
        INTERCHANGE_RAMP = 3
        RAILROAD = 4
        AMENAGED_CROSSROAD = 5
        PEDESTRIAN_ZONE = 6
        TOLL_ZONE = 7
        WORKZONE = 8
        OTHERS = 9

    class situ(CategoryBaseEnum):
        '''Situation of the accident'''
        NOT_PROVIDED = -1
        NONE = 0
        ON_ROADWAY = 1
        ON_EMERGENCY_LANE = 2
        ON_SHOULDER = 3
        ON_SIDEWALK = 4
        ON_CYCLE_PATH = 5
        ON_OTHER_SPECIAL_LANE = 6
        OTHERS = 8

    class vma(CategoryBaseEnum):
        '''Maximum speed permitted at the location and time of the accident.'''

    class catu(CategoryBaseEnum):  #
        '''User category'''
        UNDETERMINED = 0
        DRIVER = 1
        PASSENGER = 2
        PEDESTRIAN = 3

    class grav(CategoryBaseEnum):
        ''' Severity of the accident: The injured users are classified into three categories of victims plus the uninjured'''
        UNKNOWN = 0
        NO_INJURY = 1
        KILLED = 2
        INJURED_HOSPITALIZED = 3
        MINOR_INJURY = 4

    class sexe(CategoryBaseEnum):
        '''User's gender'''
        UNKNOWN = 0
        MALE = 1
        FEMALE = 2

    class an_nais(CategoryBaseEnum):
        '''Year of birth of the user'''

    class secu1(CategoryBaseEnum):
        '''The existence of a safety equipment'''
        NOT_PROVIDED = -1
        NO_EQUIPMENT = 0
        SEATBELT = 1
        HELMET = 2
        CHILD_DEVICE = 3
        REFLECTIVE_VEST = 4
        AIRBAG_2W_3W = 5
        GLOVES_2W_3W = 6
        GLOVES_AIRBAG_2W_3W = 7
        NOT_DETERMINABLE = 8
        OTHER = 9

    class jour(CategoryBaseEnum):
        '''Day of the accident'''

    class mois(CategoryBaseEnum):
        '''Month of the accident'''

    class an(CategoryBaseEnum):
        '''Year of the accident'''

    class hrmn(CategoryBaseEnum):
        '''Hour and minute of the accident'''

    class lum(CategoryBaseEnum):
        '''Lighting conditions during the accident'''
        DAYLIGHT = 1
        DUSK_OR_DAWN = 2
        NIGHT_WITHOUT_PUBLIC_LIGHT = 3
        NIGHT_WITH_PUBLIC_LIGHT_OFF = 4
        NIGHT_WITH_PUBLIC_LIGHT_ON = 5

    class dep(CategoryBaseEnum):
        '''Department code (INSEE code for French departments)'''

    class agg(CategoryBaseEnum):
        '''Location of the accident: inside or outside the urban area'''
        OUTSIDE_URBAN_AREA = 1
        INSIDE_URBAN_AREA = 2

    class int(CategoryBaseEnum):
        '''Type of intersection where the accident occurred'''
        NO_INTERSECTION = 1
        X_INTERSECTION = 2
        T_INTERSECTION = 3
        Y_INTERSECTION = 4
        INTERSECTION_WITH_MORE_THAN_4_BRANCHES = 5
        ROUNDABOUT = 6
        SQUARE = 7
        RAILWAY_CROSSING = 8
        OTHER_INTERSECTION = 9

    class atm(CategoryBaseEnum):
        '''Atmospheric conditions during the accident'''
        NOT_PROVIDED = -1
        NORMAL = 1
        LIGHT_RAIN = 2
        HEAVY_RAIN = 3
        SNOW_HAIL = 4
        FOG_SMOKE = 5
        STRONG_WIND_STORM = 6
        BLINDING_WEATHER = 7
        CLOUDY_WEATHER = 8
        OTHER = 9

    class col(CategoryBaseEnum):
        '''Type of collision'''
        NOT_PROVIDED = -1
        TWO_VEHICLES_FRONT = 1
        TWO_VEHICLES_REAR = 2
        TWO_VEHICLES_SIDE = 3
        THREE_VEHICLES_CHAIN = 4
        THREE_VEHICLES_MULTIPLE_COLLISIONS = 5
        OTHER_COLLISION = 6
        NO_COLLISION = 7

    class lat(CategoryBaseEnum):
        '''Latitude of the accident location'''

    class long(CategoryBaseEnum):
        '''Longitude of the accident location'''



class Old_RoadAccidentEnglish(FileTypeEnum):
    '''Collection of all the categories for file type 'vehicle.csv' '''

    class accident_id(CategoryBaseEnum):
        '''The Index/Number of the Crash follows the pattern yyyyxxxxx and is the index column'''

    class vehicle_id(CategoryBaseEnum):
        '''The vehicle id  in terms of xxx-xxx'''

    class vehicle_category(CategoryBaseEnum):  # catv Vehicle Category
        '''The Category of Vehicle involved in the crash'''
        UNDETERMINED = 0
        BICYCLE = 1
        MOPED_LESS_EQUAL_50CC = 2
        MICROCAR = 3
        TOURISM_VEHICLE = 7
        UTILITY_VEHICLE_PTAC_1_5T_3_5T = 10  # 1.5<PTAC<3.5
        HEAVY_TRUCK_PTAC_3_5T_7_5T = 13
        HEAVY_TRUCK_PTAC_OVER_7_5T = 14
        HEAVY_TRUCK_OVER_3_5T_WITH_TRAILER = 15
        TRACTOR_ONLY = 16
        TRACTOR_WITH_SEMI_TRAILER = 17
        SPECIAL_VEHICLE = 20
        AGRICULTURAL_TRACTOR = 21
        SCOOTER_LESS_EQUAL_50CC = 30
        MOTORCYCLE_50CC_125CC = 31
        SCOOTER_50CC_125CC = 32
        MOTORCYCLE_OVER_125CC = 33
        SCOOTER_OVER_125CC = 34
        LIGHT_QUAD_LESS_EQUAL_50CC = 35
        HEAVY_QUAD_OVER_50CC = 36
        BUS = 37
        COACH = 38
        TRAIN = 39
        TRAMWAY = 40
        THREE_WHEELED_VEHICLE_LESS_EQUAL_50CC = 41
        THREE_WHEELED_VEHICLE_50CC_125CC = 42
        THREE_WHEELED_VEHICLE_OVER_125CC = 43
        MOTORIZED_PERSONAL_TRANSPORT = 50
        NON_MOTORIZED_PERSONAL_TRANSPORT = 60
        OTHER_VEHICLE = 99

    class obstacle_static(CategoryBaseEnum):  # obs Static ObstacleHit
        ''' The Static/Stationary Obstacle Hit'''
        UNKNOWN = 0
        PARKED_VEHICLE = 1
        TREE_ON_ROADSIDE = 2
        METAL_BARRIER = 3
        CONCRETE_BARRIER = 4
        OTHER_BARRIER = 5
        BUILDING_WALL_BRIDGE_PIER = 6  # BUILDING, WALL OR BRIDGE PIER
        VERTICAL_SIGNPOST_OR_EMERGENCY_CALLBOX = 7
        POLE = 8
        URBAN_FURNITURE = 9
        PARAPET = 10
        REFUGE_ISLAND_BOLLARD = 11  # THE ROAD ISLAND / BOLLARD
        SIDEWALK = 12  # SIDEWALK OR CURB
        DITCH = 13  # DITCH OR EMBANKMENT
        OTHER_OBS_ON_ROADWAY = 14
        OTHER_OBS_ON_SIDEWALK = 15
        ROADWAY_EXIT_WITOUT_OBSTACLES = 16
        AQUEDUCT_HEAD = 17

    class obstacle_mobile(CategoryBaseEnum):  # obsm #Mobile obstacle hit
        '''The Dynamic Obstacle Hit'''
        UNKNOWN = 0
        PEDESTRIAN = 1
        VEHICLE = 2
        RAIL_VEHICLE = 3
        ANIMAL_DOMESTIC = 4
        ANIMAL_WILD = 5
        OTHER = 9

    class impact_point(CategoryBaseEnum):  # choc Initial Point of Impact
        '''The Initial Point of Impact of the crash'''
        UNKNOWN = 0
        FRONT = 1
        FRONT_LEFT = 2
        FRONT_RIGHT = 3
        REAR = 4
        REAR_RIGHT = 5
        REAR_LEFT = 6
        SIDE_LEFT = 7
        SIDE_RIGHT = 8
        MULTIPLE = 9

    class action(CategoryBaseEnum):  # manv , Main action before crash
        '''The Main Action performed by the user before the crash'''
        UNKNOWN = 0
        CIRCULATING_NO_DIRECTION_CHANGE = 1
        CIRCULATING_SAME_DIRECTION = 2  # SAME DIRECTION SAME LANE
        CIRCULATION_BETWEEN_2_LANES = 3
        CIRCULATING_REVERSING = 4
        CIRCULATING_AGAINTS_FLOW_TRAFFIC = 5
        CIRCULATING_CROSSING_MEDIAN_STRIP = 6
        CIRCULATING_IN_BUSLANE_SAME_DIRECTION = 7
        CIRCULATING_IN_BUSLANE_OPP_DIRECTION = 8
        CIRCULATING_INSERTION = 9
        CIRCULATING_TURNING_AROUND_CARRIAGE_WAY = 10
        CHANGING_LANE_LEFT = 11
        CHANGING_LANE_RIGHT = 12
        DEPORT_LEFT = 13
        DEPORT_RIGHT = 14
        TURNING_LEFT = 15
        TURNING_RIGHT = 16
        OVERTAKING_LEFT = 17
        OVERTAKING_RIGHT = 18
        # VARIOUS S
        CROSSING_ROAD = 19
        PARKING_ACTION = 20
        AVOIDANCE_ACTION = 21
        DOOR_OPENED = 22
        STOP_NO_PARKING = 23
        PARKED_WITH_PASS = 24  # PARKED WITH PASSANGERS
        DRIVING_SIDEWALK = 25
        OTHER_ACTIONS = 26

    class motor(CategoryBaseEnum):  # motor
        '''The Type of Motor(In terms of fuel type) involved in the crash'''
        UNKNOWN = 0
        CONVENTIONAL_FUEL = 1  # PETROL, DIESEL ,ETC
        HYBRID_ELECTRIC = 2
        ELECTRIC = 3
        HYDROGEN = 4
        HUMAN_POWERED = 5
        OTHER = 6

    class road(CategoryBaseEnum):
        '''Category of the road'''
        MOTORWAY = 1
        NATIONAL_ROAD = 2
        DEPARTMENTAL_ROAD = 3
        MUNICIPAL_ROAD = 4
        OFF_NETWORK = 5
        PARKING_AREA = 6
        URBAN_METROPOLE_ROAD = 7
        OTHER = 9

    class traffic(CategoryBaseEnum):
        '''Traffic regime:'''
        NOT_PROVIDED = -1
        ONE_WAY = 1
        BIDIRECTIONAL = 2
        SEPARATE_LANES = 3
        VARIABLE_LANE = 4

    class road_surface(CategoryBaseEnum):
        '''Surface condition'''
        NOT_PROVIDED = -1
        NORMAL = 1
        WET = 2
        PUDDLES = 3
        FLOODED = 4
        SNOWY = 5
        MUDDY = 6
        ICY = 7
        GREASE = 8
        OTHER = 9

    class infra(CategoryBaseEnum):
        '''Development - Infrastructure:'''
        NOT_PROVIDED = -1
        NONE = 0
        UNDERGROUND = 1
        BRIDGE = 2
        INTERCHANGE_RAMP = 3
        RAILROAD = 4
        AMENAGED_CROSSROAD = 5
        PEDESTRIAN_ZONE = 6
        TOLL_ZONE = 7
        WORKZONE = 8
        OTHERS = 9

    class situation(CategoryBaseEnum):
        '''Situation of the accident'''
        NOT_PROVIDED = -1
        NONE = 0
        ON_ROADWAY = 1
        ON_EMERGENCY_LANE = 2
        ON_SHOULDER = 3
        ON_SIDEWALK = 4
        ON_CYCLE_PATH = 5
        ON_OTHER_SPECIAL_LANE = 6
        OTHERS = 8

    class speed_limit(CategoryBaseEnum):
        '''Maximum speed permitted at the location and time of the accident.'''

    class user_category(CategoryBaseEnum):  #
        '''User category'''
        UNDETERMINED = 0
        DRIVER = 1
        PASSENGER = 2
        PEDESTRIAN = 3

    class severity(CategoryBaseEnum):
        ''' Severity of the accident: The injured users are classified into three categories of victims plus the uninjured'''
        UNKNOWN = 0
        NO_INJURY = 1
        KILLED = 2
        INJURED_HOSPITALIZED = 3
        MINOR_INJURY = 4

    class sex(CategoryBaseEnum):
        '''User's gender'''
        UNKNOWN = 0
        MALE = 1
        FEMALE = 2

    class dob(CategoryBaseEnum):
        '''Year of birth of the user'''

    class safety_equipment(CategoryBaseEnum):
        '''The existence of a safety equipment'''
        NOT_PROVIDED = -1
        NO_EQUIPMENT = 0
        SEATBELT = 1
        HELMET = 2
        CHILD_DEVICE = 3
        REFLECTIVE_VEST = 4
        AIRBAG_2W_3W = 5
        GLOVES_2W_3W = 6
        GLOVES_AIRBAG_2W_3W = 7
        NOT_DETERMINABLE = 8
        OTHER = 9

    class datetime(CategoryBaseEnum):
        '''Date Time of the accident'''

    class lum(CategoryBaseEnum):
        '''Lighting conditions during the accident'''
        DAYLIGHT = 1
        DUSK_OR_DAWN = 2
        NIGHT_WITHOUT_PUBLIC_LIGHT = 3
        NIGHT_WITH_PUBLIC_LIGHT_OFF = 4
        NIGHT_WITH_PUBLIC_LIGHT_ON = 5

    class dep(CategoryBaseEnum):
        '''Department code (INSEE code for French departments)'''

    class is_urban_area(CategoryBaseEnum):
        '''Location of the accident: inside or outside the urban area'''
        OUTSIDE_URBAN_AREA = 1
        INSIDE_URBAN_AREA = 2

    class intersection(CategoryBaseEnum):
        '''Type of intersection where the accident occurred'''
        NO_INTERSECTION = 1
        X_INTERSECTION = 2
        T_INTERSECTION = 3
        Y_INTERSECTION = 4
        INTERSECTION_WITH_MORE_THAN_4_BRANCHES = 5
        ROUNDABOUT = 6
        SQUARE = 7
        RAILWAY_CROSSING = 8
        OTHER_INTERSECTION = 9

    class weather(CategoryBaseEnum):
        '''Weather conditions during the accident'''
        NOT_PROVIDED = -1
        NORMAL = 1
        LIGHT_RAIN = 2
        HEAVY_RAIN = 3
        SNOW_HAIL = 4
        FOG_SMOKE = 5
        STRONG_WIND_STORM = 6
        BLINDING_WEATHER = 7
        CLOUDY_WEATHER = 8
        OTHER = 9

    class collision_type(CategoryBaseEnum):
        '''Type of collision'''
        NOT_PROVIDED = -1
        TWO_VEHICLES_FRONT = 1
        TWO_VEHICLES_REAR = 2
        TWO_VEHICLES_SIDE = 3
        THREE_VEHICLES_CHAIN = 4
        THREE_VEHICLES_MULTIPLE_COLLISIONS = 5
        OTHER_COLLISION = 6
        NO_COLLISION = 7

    class lat(CategoryBaseEnum):
        '''Latitude of the accident location'''

    class long(CategoryBaseEnum):
        '''Longitude of the accident location'''
