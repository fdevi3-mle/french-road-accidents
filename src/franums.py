import json
from enum import Enum


class CategoryBaseEnum(Enum):
    @classmethod
    def Name(cls):
        return f"{cls.__name__}"
    @classmethod
    def IsCategory(cls):
        return True if len(cls.__members__) > 0 else False
    @classmethod
    def get_description(cls):
        return cls.__doc__ or "No description available"
    @classmethod
    def to_dict(cls):
        return {member.name:member.value for member in cls}
    @classmethod
    def to_json(cls, indent=4):
        return json.dumps(cls.to_dict(), indent=indent)
    @classmethod
    def enum_keys(cls):
        return [member.name for member in cls]


class FileTypeEnum(Enum):
    @classmethod
    def Name(cls):
        return f"{cls.__name__}"
    @classmethod
    def get_description(cls):
        return cls.__doc__ or "No description available"
    @classmethod
    def to_dict(cls):
        return {member.name:member.value.to_dict() for member in cls}
    @classmethod
    def enum_keys(cls):
        return [member.name for member in cls]


class RoadAccidentEnum(FileTypeEnum):
    '''Collection of all the categories for file type 'vehicle.csv' '''

    class accident_id(CategoryBaseEnum):
        '''The Index/Number of the Crash follows the pattern yyyyxxxxx and is the index column'''

    class vehicle_id(CategoryBaseEnum):
        '''The vehicle id  in terms of xxx-xxx'''

    class vehicle_category(CategoryBaseEnum):  # catv Vehicle Category
        '''The Category of Vehicle involved in the crash'''
        UNKNOWN = 0
        LIGHT = 1
        MEDIUM = 2
        HEAVY = 3
        MISC = 4

    class obstacle_static(CategoryBaseEnum):  # obs Static ObstacleHit
        ''' The Static/Stationary Obstacle Hit'''
        UNKNOWN = 0
        NO_OBSTACLE = 1
        LIGHT = 2
        MEDIUM = 3
        HEAVY = 4

    class obstacle_mobile(CategoryBaseEnum):  # obsm #Mobile obstacle hit
        '''The Dynamic Obstacle Hit'''
        UNKNOWN = 0
        ANIMAL_OR_OTHER = 1
        VEHICLE = 2
        PEDESTRIAN = 3

    class impact_point(CategoryBaseEnum):  # choc Initial Point of Impact
        '''The Initial Point of Impact of the crash'''
        UNKNOWN = 0
        FRONT_IMPACT = 1
        SIDE_IMPACT = 2
        REAR_IMPACT = 3
        MULTIPLE_IMPACT = 4

    class action(CategoryBaseEnum):  # manv , Main action before crash
        '''The Main Action performed by the user before the crash'''
        UNKNOWN = 0
        STATIC = 1
        NORMAL_RISK = 2
        MEDIUM_RISK = 3
        HIGH_RISK = 4

    class motor(CategoryBaseEnum):  # motor
        '''The Type of Motor(In terms of fuel type) involved in the crash'''
        UNKNOWN = 0
        OTHER = 1
        TRADITIONAL = 2
        ELECTRIC_HYBRID = 3
        NON_MOTORIZED = 4

    class road(CategoryBaseEnum):
        '''Category of the road'''
        UNKNOWN = 0
        OTHER = 1
        URBAN_ROAD = 2
        HIGHWAY = 3

    class road_surface(CategoryBaseEnum):
        '''Surface condition'''
        UNKNOWN = 0
        NORMAL = 1
        MODERATE = 2
        SEVERE = 3

    class speed_limit(CategoryBaseEnum):
        '''Maximum speed permitted at the location and time of the accident.'''

    class user_category(CategoryBaseEnum):  #
        '''User category'''
        UNKNOWN = 0
        DRIVER = 1
        PASSENGER = 2
        PEDESTRIAN = 3

    class severity(CategoryBaseEnum):
        ''' Severity of the accident: The injured users are classified into three categories of victims plus the uninjured'''
        UNKNOWN = 0
        NO_INJURY = 1
        MINOR_INJURY = 2
        MAJOR_INJURY = 3
        KILLED = 4

    class sex(CategoryBaseEnum):
        '''User's gender'''
        UNKNOWN = 0
        MALE = 1
        FEMALE = 2

    class dob(CategoryBaseEnum):
        '''Year of birth of the user'''

    class safety_equipment(CategoryBaseEnum):
        '''The existence of a safety equipment'''
        UNKNOWN = 0
        NORMAL = 1
        GOOD = 2
        BEST = 3

    class datetime(CategoryBaseEnum):
        '''Date Time of the accident'''

    class lum(CategoryBaseEnum):
        '''Lighting conditions during the accident'''
        UNKNOWN = 0
        DAYLIGHT = 1
        NIGHT_LIT = 2
        LOW_LIGHT = 3
        NIGHT_DARK = 4

    class weather(CategoryBaseEnum):
        '''Weather conditions during the accident'''
        UNKNOWN = 0
        LIGHT = 1
        MEDIUM = 2
        SEVERE = 3

    class collision_type(CategoryBaseEnum):
        '''Type of collision'''
        UNKNOWN = 0
        NO_COLLISION = 1
        SIMPLE = 2
        COMPLEX = 3

    class lat(CategoryBaseEnum):
        '''Latitude of the accident location'''

    class long(CategoryBaseEnum):
        '''Longitude of the accident location'''
