from typing import List

from ..utils_typing import Entity, dataclass


"""Entity definitions

The entity definitions are derived from the official ConLL2003 guidelines:
https://www.clips.uantwerpen.be/conll2003/ner/
Based on: Nancy Chinchor, Erica Brown, Lisa Ferro, Patty Robinson,
           "1999 Named Entity Task Definition". MITRE and SAIC, 1999.
"""


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
class WeatherNoun(Entity):
    """{weather/noun}"""
    span: str # {weather/noun_examples}

@dataclass
class AlarmModifier(Entity):
    """{alarm/alarm_modifier}"""
    span: str # {alarm/alarm_modifier_examples}

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
class TimerNoun(Entity):
    """{timer/noun}"""
    span: str # {timer/noun_examples}

@dataclass
class RecurringPeriod(Entity):
    """{reminder/recurring_period}"""
    span: str # {reminder/recurring_period_examples}

@dataclass
class ReminderNoun(Entity):
    """{reminder/noun}"""
    span: str # {reminder/noun_examples}

@dataclass
class ReminderTodo(Entity):
    """{reminder/todo}"""
    span: str # {reminder/todo_examples}

@dataclass
class Reference(Entity):
    """{reminder/reference}"""
    span: str # {reminder/reference_examples}

ENTITY_DEFINITIONS: List[Entity] = [
    WeatherNoun,
    Location, 
    Datetime, 
    WeatherAttribute, 
    ReminderTodo,
    AlarmModifier, 
    ReminderNoun,
    RecurringPeriod,
    Reference,
    ReminderModifier, 
    TimerNoun,
    Negation,
    TimerAttributes,
    NewsType,
    WeatherTemperatureUnit
]

# __all__ = list(map(str, [*ENTITY_DEFINITIONS]))
