GUIDELINES = {
    "ner_person": {
        "en": [
            "first, middle and last names of people, animals and fictional characters aliases.",
            (
                'Paraphrase: "The initial, middle, and last names of individuals, creatures, and imaginary'
                " personalities, along \nwith their pseudonyms."
            ),
            (
                'Paraphrase: "Initially, focus on the full names of individuals, animals, and imaginary personalities,'
                " as well as \ntheir pseudonyms."
            ),
            (
                'Paraphrase: "Initially, the study focused on the names of individuals, including their first, middle,'
                " and last \nnames, as well as the names of animals and imaginary characters, along with any aliases"
                " they might have."
            ),
            (
                'Original text: "first, middle and last names of people, animals and fictional characters aliases."'
                ' Paraphrased \ntext: "Initially, individuals consider the full names of humans, animals, and'
                " imaginary personalities, along with \ntheir nicknames or pseudonyms."
            ),
        ]
    },
    "ner_organization": {
        "en": [
            (
                "Companies (press agencies, studios, banks, stock markets, manufacturers, cooperatives) subdivisions"
                " of \ncompanies (newsrooms) brands political movements (political parties, terrorist organisations)"
                " government bodies \n(ministries, councils, courts, political unions of countries (e.g. the {\\it"
                " U.N.})) publications (magazines, newspapers, \njournals) musical companies (bands, choirs, opera"
                " companies, orchestras public organisations (schools, universities, \ncharities other collections of"
                " people (sports clubs, sports teams, associations, theaters companies, religious orders, \nyouth"
                " organisations."
            ),
            (
                "Organizations such as news agencies, film studios, banks, stock exchanges, manufacturers,"
                " cooperatives, as well \nas their subdivisions like newsrooms, and various entities like political"
                " movements (political parties, terrorist \ngroups), government bodies (ministries, councils, courts),"
                " political unions of countries (e.g., the United Nations), \npublications (magazines, newspapers,"
                " journals), musical companies (bands, choirs, opera companies, orchestras), public \norganizations"
                " (schools, universities, charities), and other assortments of people (sports clubs, sports teams,"
                " associations, \ntheaters, companies, religious orders, youth organizations) are examples of groups"
                " that can be analyzed using network \nanalysis."
            ),
            (
                "Organizations such as news agencies, film studios, banks, stock exchanges, manufacturers, and"
                " cooperatives, as \nwell as subdivisions of companies like newsrooms, and distinct brands encompass"
                " political movements like political \nparties and terrorist groups, government entities including"
                " ministries, councils, courts, and political unions of \ncountries like the United Nations, various"
                " publications like magazines, newspapers, and journals, musical companies like \nbands, choirs, opera"
                " companies, and orchestras, public organizations like schools, universities, and charities, and"
                " \nother assortments of people such as sports clubs, sports teams, associations, theaters, and"
                " religious orders, as well as \nyouth organizations."
            ),
            (
                "Organizations such as news agencies, film studios, banks, stock exchanges, manufacturers, and"
                " cooperatives, as \nwell as subdivisions of these companies like newsrooms, and brands associated"
                " with political movements like political \nparties and terrorist groups, government entities"
                " including ministries, councils, courts, and political unions of \ncountries like the United Nations,"
                " various publications like magazines, newspapers, and journals, musical companies \nencompassing"
                " bands, choirs, opera companies, and orchestras, public organizations such as schools, universities,"
                " and \ncharities, and finally other assortments of people like sports clubs, sports teams,"
                " associations, theaters, companies, \nreligious orders, and youth organizations."
            ),
            (
                "Organizations such as news agencies, film studios, banks, stock exchanges, manufacturers,"
                " cooperatives, as well \nas subdivisions of companies like newsrooms, brands, political movements"
                " like political parties and terrorist \norganizations, government entities like ministries, councils,"
                " courts, and political unions of countries like the United \nNations, various publications like"
                " magazines, newspapers, and journals, musical companies like bands, choirs, opera \ncompanies, and"
                " orchestras, public organizations like schools, universities, and charities, and other groups of"
                " people like \nsports clubs, sports teams, associations, theaters, companies, religious orders, and"
                " youth organizations."
            ),
        ]
    },
    "ner_location": {
        "en": [
            (
                "Roads (streets, motorways) trajectories regions (villages, towns, cities, provinces, countries,"
                " continents, \ndioceses, parishes) structures (bridges, ports, dams) natural locations (mountains,"
                " mountain ranges, woods, rivers, \nwells, fields, valleys, gardens, nature reserves, allotments,"
                " beaches, national parks) public places (squares, opera \nhouses, museums, schools, markets,"
                " airports, stations, swimming pools, hospitals, sports facilities, youth centers, \nparks, town"
                " halls, theaters, cinemas, galleries, camping grounds, NASA launch pads, club houses, universities,"
                " \nlibraries, churches, medical centers, parking lots, playgrounds, cemeteries) commercial places"
                " (chemists, pubs, \nrestaurants, depots, hostels, hotels, industrial parks, nightclubs, music venues)"
                " assorted buildings (houses, monasteries, \ncreches, mills, army barracks, castles, retirement homes,"
                " towers, halls, rooms, vicarages, courtyards) abstract \n``places'' (e.g. {\\it the free world})"
            ),
            (
                "Roads (including streets and motorways) connect various regions (such as villages, towns, cities,"
                " provinces, \ncountries, continents, dioceses, and parishes). They also provide access to structures"
                " (like bridges, ports, and dams) and \nnatural locations (like mountains, mountain ranges, woods,"
                " rivers, wells, fields, valleys, gardens, nature reserves, \nallotments, beaches, and national"
                " parks). These roads lead to public places (like squares, opera houses, museums, schools, \nmarkets,"
                " airports, stations, swimming pools, hospitals, sports facilities, youth centers, parks, town halls,"
                " theaters, \ncinemas, galleries, camping grounds, NASA launch pads, club houses, universities,"
                " libraries, churches, medical centers, \nand parking lots) and commercial places (such as chemists,"
                " pubs, restaurants, depots, hostels, hotels, industrial \nparks, nightclubs, and music venues)."
                " Additionally, they pass by various types of buildings (including houses, \nmonasteries, creches,"
                " mills, army barracks, castles, retirement homes, towers, halls, rooms, vicarages, and courtyards),"
                ' as \nwell as more abstract "places" (e.g., "the free world").'
            ),
            (
                "Roads (including streets, motorways) lead to various regions (such as villages, towns, cities,"
                " provinces, \ncountries, continents, dioceses, parishes) and are connected to different structures"
                " (like bridges, ports, dams). They also \ntraverse natural locations (like mountains, mountain"
                " ranges, woods, rivers, wells, fields, valleys, gardens, nature \nreserves, allotments, beaches, and"
                " national parks) as well as public places (encompassing squares, opera houses, museums, \nschools,"
                " markets, airports, stations, swimming pools, hospitals, sports facilities, youth centers, parks,"
                " town halls, \ntheaters, cinemas, galleries, camping grounds, NASA launch pads, club houses,"
                " universities, libraries, churches, medical \ncenters, parking lots, playgrounds, and cemeteries)."
                " Furthermore, they pass by commercial places (such as chemists, pubs, \nrestaurants, depots, hostels,"
                " hotels, industrial parks, nightclubs, and music venues) and various buildings (like houses,"
                " \nmonasteries, creches, mills, army barracks, castles, retirement homes, towers, halls, rooms,"
                ' vicarages, and courtyards). \nLastly, they can also encompass abstract "places" (e.g., "the free'
                ' world").'
            ),
            (
                "Roads (including streets, motorways) lead to various regions (encompassing villages, towns, cities,"
                " provinces, \ncountries, continents, dioceses, parishes), and they connect different structural"
                " elements (such as bridges, ports, dams). \nThey also traverse natural locations (like mountains,"
                " mountain ranges, woods, rivers, wells, fields, valleys, \ngardens, nature reserves, allotments,"
                " beaches, and national parks). Furthermore, they provide access to public places \n(like squares,"
                " opera houses, museums, schools, markets, airports, stations, swimming pools, hospitals, sports"
                " \nfacilities, youth centers, parks, town halls, theaters, cinemas, galleries, camping grounds, NASA"
                " launch pads, club houses, \nuniversities, libraries, churches, medical centers, and parking lots)"
                " and commercial establishments (like chemists, pubs, \nrestaurants, depots, hostels, hotels,"
                " industrial parks, nightclubs, and music venues). Additionally, they serve a variety of \nspecific"
                " buildings (including houses, monasteries, creches, mills, army barracks, castles, retirement homes,"
                ' towers, \nhalls, rooms, vicarages, and courtyards), as well as more abstract "places" (e.g., "the'
                ' free world").'
            ),
            (
                "Roads (including streets, motorways) lead to various regions (encompassing villages, towns, cities,"
                " provinces, \ncountries, continents, dioceses, parishes), and they connect diverse structures (such"
                " as bridges, ports, dams). They also \ntraverse natural locations (like mountains, mountain ranges,"
                " woods, rivers, wells, fields, valleys, gardens, nature \nreserves, allotments, beaches, and national"
                " parks). Furthermore, they access public places (like squares, opera houses, \nmuseums, schools,"
                " markets, airports, stations, swimming pools, hospitals, sports facilities, youth centers, parks,"
                " town \nhalls, theaters, cinemas, galleries, camping grounds, NASA launch pads, club houses,"
                " universities, libraries, \nchurches, medical centers, and parking lots), as well as commercial"
                " places (chemists, pubs, restaurants, depots, hostels, \nhotels, industrial parks, nightclubs, music"
                " venues). Additionally, they pass by a variety of buildings (such as houses, \nmonasteries, creches,"
                " mills, army barracks, castles, retirement homes, towers, halls, rooms, vicarages, and courtyards),"
                ' and \nthey even touch abstract "places" (e.g., "the free world").'
            ),
        ]
    },
    "ner_date": {
        "en": [
            (
                "all absolute and relative dates or periods, including days, months, years.\n"
                "1. Absolute date expressions are to be tagged. Absolute date expression must\n"
                "indicate a specific segment of date i.e the particular day, season, financial quarters,\n"
                "years, decade or a particular century.\n"
                "2. Relative time expressions.\n"
                "3. Special days, such as holidays, that are referenced by name.\n"
                "4. Expression indicating periods between two dates.\n"
                "5. Absolute time expressions. It must indicate a specific segment of time i.e a particular minute and hour.\n"
                "6. Time expressions including the city time zone.\n"
                "7. Expression indicating periods between two times."
            ),            
        ]
    },

}
