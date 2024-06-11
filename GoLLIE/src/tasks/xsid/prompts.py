from typing import List

from ..utils_typing import Entity, dataclass


@dataclass
class Location(Entity):
    """{location}"""
    span: str # {location_examples}

@dataclass
class Datetime(Entity):
    """{datetime}"""
    span: str # {datetime_examples}

@dataclass
class WeatherAttribute(Entity):
    """{weather/attribute}"""
    span: str # {weather/attribute_examples}

@dataclass
class Reference(Entity):
    """{reference}"""
    span: str # {reference_examples}

@dataclass
class ReminderTodo(Entity):
    """{reminder/todo}"""
    span: str # {reminder/todo_examples}

@dataclass
class AlarmModifier(Entity):
    """{alarm/alarm_modifier}"""
    span: str # {alarm/alarm_modifier_examples}

@dataclass
class RecurringDatetime(Entity):
    """{recurring_datetime}"""
    span: str # {recurring_datetime_examples}

@dataclass
class ReminderModifier(Entity):
    """{reminder/reminder_modifier}"""
    span: str # {reminder/reminder_modifier_examples}

@dataclass
class Negation(Entity):
    """{negation}"""
    span: str # {negation_examples}

@dataclass
class TimerAttributes(Entity):
    """{timer/attributes}"""
    span: str # {timer/attributes_examples}

@dataclass
class NewsType(Entity):
    """{news/type}"""
    span: str # {news/type_examples}

@dataclass
class WeatherTemperatureUnit(Entity):
    """{weather/temperatureUnit}"""
    span: str # {weather/temperatureUnit_examples}

@dataclass
class EntityName(Entity):
    """{entity_name}"""
    span: str # {entity_name_examples}

@dataclass
class Playlist(Entity):
    """{playlist}"""
    span: str # {playlist_examples}

@dataclass
class MusicItem(Entity):
    """{music_item}"""
    span: str # {music_item_examples}

@dataclass
class Artist(Entity):
    """{artist}"""
    span: str # {artist_examples}

@dataclass
class PartySizeNumber(Entity):
    """{party_size_number}"""
    span: str # {party_size_number_examples}

@dataclass
class Sort(Entity):
    """{sort}"""
    span: str # {sort_examples}

@dataclass
class RestaurantType(Entity):
    """{restaurant_type}"""
    span: str # {restaurant_type_examples}

@dataclass
class RestaurantName(Entity):
    """{restaurant_name}"""
    span: str # {restaurant_name_examples}

@dataclass
class ServedDish(Entity):
    """{served_dish}"""
    span: str # {served_dish_examples}

@dataclass
class Facility(Entity):
    """{facility}"""
    span: str # {facility_examples}

@dataclass
class PartySizeDescription(Entity):
    """{party_size_description}"""
    span: str # {party_size_description_examples}

@dataclass
class Cuisine(Entity):
    """{cuisine}"""
    span: str # {cuisine_examples}

@dataclass
class ConditionTemperature(Entity):
    """{condition_temperature}"""
    span: str # {condition_temperature_examples}

@dataclass
class ConditionDescription(Entity):
    """{condition_description}"""
    span: str # {condition_description_examples}

@dataclass
class Service(Entity):
    """{service}"""
    span: str # {service_examples}

@dataclass
class Album(Entity):
    """{album}"""
    span: str # {album_examples}

@dataclass
class Genre(Entity):
    """{genre}"""
    span: str # {genre_examples}

@dataclass
class Track(Entity):
    """{track}"""
    span: str # {track_examples}

@dataclass
class RatingValue(Entity):
    """{rating_value}"""
    span: str # {rating_value_examples}

@dataclass
class BestRating(Entity):
    """{best_rating}"""
    span: str # {best_rating_examples}

@dataclass
class RatingUnit(Entity):
    """{rating_unit}"""
    span: str # {rating_unit_examples}

@dataclass
class ObjectName(Entity):
    """{object_name}"""
    span: str # {object_name_examples}

@dataclass
class ObjectPartOfSeriesType(Entity):
    """{object_part_of_series_type}"""
    span: str # {object_part_of_series_type_examples}

@dataclass
class ObjectSelect(Entity):
    """{object_select}"""
    span: str # {object_select_examples}

@dataclass
class ObjectType(Entity):
    """{object_type}"""
    span: str # {object_type_examples}

@dataclass
class MovieName(Entity):
    """{movie_name}"""
    span: str # {movie_name_examples}

@dataclass
class ObjectLocationType(Entity):
    """{object_location_type}"""
    span: str # {object_location_type_examples}

@dataclass
class MovieType(Entity):
    """{movie_type}"""
    span: str # {movie_type_examples}


ENTITY_DEFINITIONS: List[Entity] = [Location, 
Datetime, 
WeatherAttribute, 
Reference, 
ReminderTodo, 
AlarmModifier, 
RecurringDatetime,
ReminderModifier, 
Negation, 
TimerAttributes,
NewsType, 
WeatherTemperatureUnit, 
EntityName, 
Playlist, 
MusicItem, 
Artist, 
PartySizeNumber, 
Sort, 
RestaurantType, 
RestaurantName, 
ServedDish, 
Facility, 
PartySizeDescription, 
Cuisine, 
ConditionTemperature, 
ConditionDescription, 
Service, 
Album, 
Genre, 
Track, 
RatingValue, 
BestRating, 
RatingUnit, 
ObjectName, 
ObjectPartOfSeriesType, 
ObjectSelect,
ObjectType, 
MovieName, 
ObjectLocationType, 
MovieType]

# __all__ = list(map(str, [*ENTITY_DEFINITIONS]))
