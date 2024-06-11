# The following lines describe the task definition
@dataclass
class Location(Entity):
    """Roads (streets, motorways) trajectories regions (villages, towns, cities, provinces, countries, continents,
    dioceses, parishes) structures (bridges, ports, dams) natural locations (mountains, mountain ranges, woods, rivers,
    wells, fields, valleys, gardens, nature reserves, allotments, beaches, national parks) public places (squares, opera
    houses, museums, schools, markets, airports, stations, swimming pools, hospitals, sports facilities, youth centers,
    parks, town halls, theaters, cinemas, galleries, camping grounds, NASA launch pads, club houses, universities,
    libraries, churches, medical centers, parking lots, playgrounds, cemeteries) commercial places (chemists, pubs,
    restaurants, depots, hostels, hotels, industrial parks, nightclubs, music venues) assorted buildings (houses, monasteries,
    creches, mills, army barracks, castles, retirement homes, towers, halls, rooms, vicarages, courtyards) abstract
    ``places'' (e.g. {\it the free world})"""

    span: str  # Such as: "U.S.", "Germany", "Britain", "Australia", "England"


@dataclass
class Organization(Entity):
    """Companies (press agencies, studios, banks, stock markets, manufacturers, cooperatives) subdivisions of
    companies (newsrooms) brands political movements (political parties, terrorist organisations) government bodies
    (ministries, councils, courts, political unions of countries (e.g. the {\it U.N.})) publications (magazines, newspapers,
    journals) musical companies (bands, choirs, opera companies, orchestras public organisations (schools, universities,
    charities other collections of people (sports clubs, sports teams, associations, theaters companies, religious orders,
    youth organisations."""

    span: str  # Such as: "Reuters", "U.N.", "NEW YORK", "CHICAGO", "PUK"


@dataclass
class Person(Entity):
    """first, middle and last names of people, animals and fictional characters aliases."""

    span: str  # Such as: "Clinton", "Dole", "Arafat", "Yeltsin", "Lebed"


# This is the text to analyze
text = "O janko - Ala - la fɔli tun bɛ kun bɔ ka Umaru Gajaga jɔyɔrɔ ye cɛmannin Nuhumu Sidibe saya la ."

# This is the English translation of the text
eng_text = "The main focus was on the role of Umaru Gajaga in the death of commander Nuhumu Sidibe."

# Using translation and fusion
# (1) generate annotation for eng_text
# (2) generate annotation for text

# The annotation instances that take place in the eng_text above are listed here
result = [
    Person(span="Umaru Gajaga"),
    Person(span="Nuhumu Sidibe"),
]

# The annotation instances that take place in the text above are listed here
final_result = [
    Person(span="Umaru Gajaga"),
    Person(span="Nuhumu Sidibe"),
]
