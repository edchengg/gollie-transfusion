from typing import List

from ..utils_typing import Entity, dataclass


@dataclass
class Time(Entity):
    """{time}"""
    span: str # {time_example}

@dataclass
class Date(Entity):
    """{date}"""
    span: str # {date_example}

@dataclass
class ColorType(Entity):
    """{color_type}"""
    span: str # {color_type_example}

@dataclass
class HousePlace(Entity):
    """{house_place}"""
    span: str # {house_place_example}

@dataclass
class ChangeAmount(Entity):
    """{change_amount}"""
    span: str # {change_amount_example}

@dataclass
class ArtistName(Entity):
    """{artist_name}"""
    span: str # {artist_name_example}

@dataclass
class MediaType(Entity):
    """{media_type}"""
    span: str # {media_type_example}

@dataclass
class PlaceName(Entity):
    """{place_name}"""
    span: str # {place_name_example}

@dataclass
class TimeZone(Entity):
    """{time_zone}"""
    span: str # {time_zone_example}

@dataclass
class OrderType(Entity):
    """{order_type}"""
    span: str # {order_type_example}

@dataclass
class FoodType(Entity):
    """{food_type}"""
    span: str # {food_type_example}

@dataclass
class NewsTopic(Entity):
    """{news_topic}"""
    span: str # {news_topic_example}

@dataclass
class SongName(Entity):
    """{song_name}"""
    span: str # {song_name_example}

@dataclass
class MusicGenre(Entity):
    """{music_genre}"""
    span: str # {music_genre_example}

@dataclass
class DeviceType(Entity):
    """{device_type}"""
    span: str # {device_type_example}

@dataclass
class MealType(Entity):
    """{meal_type}"""
    span: str # {meal_type_example}

@dataclass
class BusinessName(Entity):
    """{business_name}"""
    span: str # {business_name_example}

@dataclass
class GeneralFrequency(Entity):
    """{general_frequency}"""
    span: str # {general_frequency_example}

@dataclass
class WeatherDescriptor(Entity):
    """{weather_descriptor}"""
    span: str # {weather_descriptor_example}

@dataclass
class PlayerSetting(Entity):
    """{player_setting}"""
    span: str # {player_setting_example}

@dataclass
class JokeType(Entity):
    """{joke_type}"""
    span: str # {joke_type_example}

@dataclass
class TimeOfDay(Entity):
    """{timeofday}"""
    span: str # {timeofday_example}

@dataclass
class EventName(Entity):
    """{event_name}"""
    span: str # {event_name_example}

@dataclass
class BusinessType(Entity):
    """{business_type}"""
    span: str # {business_type_example}

@dataclass
class PlaylistName(Entity):
    """{playlist_name}"""
    span: str # {playlist_name_example}

@dataclass
class MusicDescriptor(Entity):
    """{music_descriptor}"""
    span: str # {music_descriptor_example}

@dataclass
class Person(Entity):
    """{person}"""
    span: str # {person_example}

@dataclass
class AlarmType(Entity):
    """{alarm_type}"""
    span: str # {alarm_type_example}

@dataclass
class AppName(Entity):
    """{app_name}"""
    span: str # {app_name_example}

@dataclass
class CoffeeType(Entity):
    """{coffee_type}"""
    span: str # {coffee_type_example}

@dataclass
class Relation(Entity):
    """{relation}"""
    span: str # {relation_example}

@dataclass
class MovieName(Entity):
    """{movie_name}"""
    span: str # {movie_name_example}

@dataclass
class DrinkType(Entity):
    """{drink_type}"""
    span: str # {drink_type_example}

@dataclass
class TransportType(Entity):
    """{transport_type}"""
    span: str # {transport_type_example}

@dataclass
class MusicAlbum(Entity):
    """{music_album}"""
    span: str # {music_album_example}

@dataclass
class PersonalInfo(Entity):
    """{personal_info}"""
    span: str # {personal_info_example}

@dataclass
class ListName(Entity):
    """{list_name}"""
    span: str # {list_name_example}

@dataclass
class SportType(Entity):
    """{sport_type}"""
    span: str # {sport_type_example}

@dataclass
class RadioName(Entity):
    """{radio_name}"""
    span: str # {radio_name_example}

@dataclass
class PodcastName(Entity):
    """{podcast_name}"""
    span: str # {podcast_name_example}

@dataclass
class AudiobookName(Entity):
    """{audiobook_name}"""
    span: str # {audiobook_name_example}

@dataclass
class AudiobookAuthor(Entity):
    """{audiobook_author}"""
    span: str # {audiobook_author_example}

@dataclass
class CookingType(Entity):
    """{cooking_type}"""
    span: str # {cooking_type_example}

@dataclass
class Ingredient(Entity):
    """{ingredient}"""
    span: str # {ingredient_example}

@dataclass
class GameName(Entity):
    """{game_name}"""
    span: str # {game_name_example}

@dataclass
class PodcastDescriptor(Entity):
    """{podcast_descriptor}"""
    span: str # {podcast_descriptor_example}

@dataclass
class MovieType(Entity):
    """{movie_type}"""
    span: str # {movie_type_example}

@dataclass
class TransportAgency(Entity):
    """{transport_agency}"""
    span: str # {transport_agency_example}

@dataclass
class TransportDescriptor(Entity):
    """{transport_descriptor}"""
    span: str # {transport_descriptor_example}

@dataclass
class TransportName(Entity):
    """{transport_name}"""
    span: str # {transport_name_example}

@dataclass
class CurrencyName(Entity):
    """{currency_name}"""
    span: str # {currency_name_example}

@dataclass
class DefinitionWord(Entity):
    """{definition_word}"""
    span: str # {definition_word_example}

@dataclass
class EmailFolder(Entity):
    """{email_folder}"""
    span: str # {email_folder_example}

@dataclass
class GameType(Entity):
    """{game_type}"""
    span: str # {game_type_example}

@dataclass
class EmailAddress(Entity):
    """{email_address}"""
    span: str # {email_address_example}

# filter to top 30 class
ENTITY_DEFINITIONS: List[Entity] = [ 
# [Date, PlaceName, EventName, Person, Time, MediaType, BusinessName, WeatherDescriptor, FoodType, TransportType, ArtistName, TimeOfDay, ListName, Relation, HousePlace, DeviceType, DefinitionWord, MusicGenre, CurrencyName, NewsTopic, PlayerSetting, SongName, RadioName, BusinessType, ColorType, GameName, PodcastDescriptor, AudiobookName, GeneralFrequency, OrderType]
    Time,
    Date,
    ColorType,
    HousePlace,
    ChangeAmount,
    ArtistName,
    MediaType,
    PlaceName,
    TimeZone,
    OrderType,
    FoodType,
    NewsTopic,
    SongName,
    MusicGenre,
    DeviceType,
    MealType,
    BusinessName,
    GeneralFrequency,
    WeatherDescriptor,
    PlayerSetting,
    JokeType,
    TimeOfDay,
    EventName,
    BusinessType,
    PlaylistName,
    MusicDescriptor,
    Person,
    AlarmType,
    AppName,
    CoffeeType,
    Relation,
    MovieName,
    DrinkType,
    TransportType,
    MusicAlbum,
    PersonalInfo,
    ListName,
    SportType,
    RadioName,
    PodcastName,
    AudiobookName,
    AudiobookAuthor,
    CookingType,
    Ingredient,
    GameName,
    PodcastDescriptor,
    MovieType,
    TransportAgency,
    TransportDescriptor,
    TransportName,
    CurrencyName,
    DefinitionWord,
    EmailFolder,
    GameType,
    EmailAddress]
