import copy
import five_oh_six as utl


# Constants
CACHE_FILEPATH = './CACHE.json'
NONE_VALUES = ('', 'n/a', 'none', 'unknown')
SWAPI_ENDPOINT = 'https://swapi.py4e.com/api'
SWAPI_CATEGORES = f"{SWAPI_ENDPOINT}/"
SWAPI_PEOPLE = f"{SWAPI_ENDPOINT}/people/"
SWAPI_PLANETS = f"{SWAPI_ENDPOINT}/planets/"
SWAPI_SPECIES = f"{SWAPI_ENDPOINT}/species/"
SWAPI_STARSHIPS = f"{SWAPI_ENDPOINT}/starships/"

# Create/retrieve cache
cache = utl.create_cache(CACHE_FILEPATH)


def assign_crew_members(crew_size, crew_positions, personnel):
    """Returns a dictionary of crew members mapped (i.e., assigned) by position and limited in
    size by the < crew_size > value.

    The < crew_positions > and < personnel > lists must contain the same number of elements. The
    individual < crew_positions > and < personnel > elements are then paired by index position and
    stored in a dictionary structured as follows:

    {< crew_position[0] >: < personnel[0] >, < crew_position[1] >: < personnel[1] >, ...}

    WARN: The number of crew positions/members is limited by the < crew size > value. No additional
    crew positions/members are permitted to be assigned to the crew members dictionary even if
    passed to the function. Crew positions/members are assigned to the dictionary as key-value pairs
    by index position (0, 1, ...).

    A single line dictionary comprehension is employed to create the new crew members dictionary.

    Parameters:
        crew_size (int): max crew members permitted
        crew_positions (list): crew positions (e.g., 'pilot', 'copilot', etc.)
        personnel (list): flight crew to be assigned to the crew positions

    Returns:
        dict: crew members by position
    """

    return {crew_positions[i]: personnel[i] for i in range(crew_size)}


def board_passengers(max_passengers, passengers):
    """Returns a list of passengers that are permitted to board a starship or other vehicle. The
    size of the list is governed by the < max_passengers > value.

    WARN: The number of passengers permitted to board a starship or other vehicle is limited by the
    provided < max_passengers > value. If the number of passengers attempting to board exceeds
    < max_passengers > only the first < n > passengers (where `n` = "max_passengers") are permitted
    to board the vessel.

    Parameters:
        max_passengers (int): max number of passengers permitted to board a vessel
        passengers (list): passengers seeking permission to board

    Returns:
        list: passengers to board
    """

    max_passengers["passengers_on_board"] = passengers[: max_passengers["max_passengers"]]
    return max_passengers


def calculate_articles_mean_word_count(articles):
    """Calculates the mean (e.g., average) "word_count" of the passed in list of < articles >.
    Excludes from the calculation any article with a word count of zero (0) or < None >. Word counts
    are summed and then divided by the number of non-zero/non-< None > "word_count" articles. The
    resulting mean value is rounded to the second (2nd) decimal place and returned to the caller.

    The function maintains a count of the number of articles evaluated and a count of the total
    words accumulated from each article's "word_count" key-value pair.

    The function checks the truth value of each article's "word_count" before attempting to
    increment the count. If the truth vallue of the "word_count" is < False > the article is
    excluded from the count.

    Parameters:
        articles (list): nested dictionary representations of New York Times articles

    Returns:
        float: mean word count rounded to the second (2nd) decimal place
    """
    word_count = 0
    for article in articles:
        if article['word_count'] == 0 or None:
           articles.remove(article)
    for article in articles:
        word_count += article['word_count']
    avg_word_count = word_count / len(articles)
    return round(avg_word_count,2)

def convert_episode_values(episodes, none_values):
    """Converts select string values to either < int >, < float >, < list >, or < None >
    in the passed in list of nested dictionaries. The function delegates to the
    < utl.to_*() > functions the task of converting the specified strings to either
    an integer, float, list, or None.

    If a value is a member of < none_values > the value is replaced by < None >. Otherwise,
    various < utl.to_*() > functions are called as necessary in an attempt to convert
    certain episode values to more appropriate types per the "Type conversions" listed below.

    Type conversions:
        series_season_num (str) -> series_season_num (int | None)
        series_episode_num (str) -> series_episode_num (int | None)
        season_episode_num (str) -> season_episode_num (int | None)
        episode_prod_code (str) -> episode_prod_code (float | None)
        episode_us_viewers_mm (str) -> episode_us_viewers_mm (float | None)
        episode_writers (str) -> episode_writers (list | None)

    Parameters:
        episodes (list): nested episode dictionaries
        none_values (tuple): strings to convert to None

    Returns:
        list: nested episode dictionaries containing mutated key-value pairs
    """

    for episode in episodes:
        for key, value in episode.items():
            if key == 'series_season_num':
                episode[key] = utl.to_none(utl.to_int(value), none_values)
            elif key == 'series_episode_num':
                episode[key] = utl.to_none(utl.to_int(value), none_values)
            elif key == 'season_episode_num':
                episode[key] = utl.to_none(utl.to_int(value), none_values)
            elif key == 'episode_prod_code':
                episode[key] = utl.to_none(utl.to_float(value), none_values)
            elif key == 'episode_us_viewers_mm':
                episode[key] = utl.to_none(utl.to_float(value), none_values)
            elif key == 'episode_writers':
                episode[key] = utl.to_none(utl.to_list(value,', '), none_values)
            else:
                episode[key] = utl.to_none(value, none_values)

    return episodes


def count_episodes_by_director(episodes): #week_11_solution
    """Constructs and returns a dictionary of key-value pairs that associate each director with
    a count of the episodes that they directed. The director's name comprises the key and the
    associated value a count of the number of episodes they directed. Duplicate keys are NOT
    permitted.

    Format:
        {
            < director_name_01 >: < episode_count >,
            < director_name_02 >: < episode_count >,
            ...
        }

    Each director's episode count is incremented by < 1.0 > if, and only if, the director is
    the only person credited with directing the episode. Otherwise, if more than one person
    is credited with directing the episode each director is allocated a fraction of < 1.0 >.
    This value is calculated by dividing < 1.0 > by the number of directors credited with
    directing the episode.

    Parameters:
        episodes (list): nested episode dictionaries

    Returns:
        dict: a dictionary that store counts of the number of episodes directed
              by each director
    """

    director_count = {}  
    for episode in episodes:
        episode['episode_director'] = utl.to_list(episode["episode_director"],", ")
        for director in episode['episode_director']:
            if director not in director_count:
                director_count[director] = 1.0/len(episode["episode_director"])
            else:
                director_count[director] += 1.0/len(episode["episode_director"])   
    return director_count  


def create_droid(keys, swapi_data, wookiee_data=None, none_values=NONE_VALUES):
    """Returns a new "thinned" dictionary representation of a droid based on the passed in
    < swapi_data > dictionary. If an optional < wookiee_data > dictionary is provided by the
    caller, the < swapi_data > dictionary is updated with the < wookiee_data > key-value
    pairs prior to creating the new dictionary representation of the droid.

    The new dictionary is constructed by mapping a subset of the < swapi_data > dictionary's
    key-value pairs to the new dictionary based on the provided < keys > dictionary. The
    < keys > dictionary includes a nested "droid" dictionary that specifies the following
    new dictionary attributes:

    * the < swapi_data > key-value pairs to be mapped to the new dictionary.
    * the order in which the < swapi_data > key-value pairs are mapped to the new dictionary.
    * the key names to be used in the new dictionary. Each key in < keys > corresponds to
      a key in < swapi_data >. Each value in < keys > represents the (new) key name to be used
      in the new dictionary.

    < swapi_data > values are converted to more appropriate types as outlined below under "Mappings".
    Strings found in < none_values > are converted to < None > irrespective of case. Type
    conversions are delegated to the various < utl.to_*() > functions.

    The targeted < swapi_data > value is then mapped to the new key when assigning the new key-value
    pair to the "droid" dictionary.

    Mappings (old key -> new key):
        url (str) -> url (str)
        name (str) -> name (str | None)
        model (str) -> model (str | None)
        manufacturer (str) -> manufacturer (str | None)
        create_year (str) -> create_date (dict | None)
        height (str) -> height_cm (float | None)
        mass (str) -> mass_kg (float | None)
        equipment (str) -> equipment (list | None)
        instructions (str) -> instructions (list | None)

    Parameters:
        keys (dict): Old key to new key mappings
        swapi_data (dict): source data
        wookiee_data (dict): additional data to be combined with < swapi_data >
        none_values (tuple): strings to convert to None

    Returns:
        dict: new dictionary representation of a droid
    """
    droid_dict = {}
    if wookiee_data: 
        swapi_data.update(wookiee_data)
    for key, value in keys["droid"].items(): 
        if key == 'url':
            droid_dict[value] = swapi_data[key]
        elif key in ['name', 'model', 'manufacturer']:
            droid_dict[value] = utl.to_none(swapi_data.get(key), none_values) 
        elif key == 'create_year':
            droid_dict[value] = utl.to_none(utl.to_year_era(swapi_data.get(key)), none_values) 
        elif key in ['height', 'mass']:
           droid_dict[value] = utl.to_none(utl.to_float(swapi_data.get(key)), none_values) 
        elif key in ['equipment', 'instructions']:
            droid_dict[value] = utl.to_none(utl.to_list(swapi_data.get(key), "｜"), none_values) 
        else:
            raise ValueError(f"Invalid key: {key}")
    return droid_dict



def create_person(keys, swapi_data, wookiee_data=None, planets=None, planet_key="name", species=None, species_key="name", none_values=NONE_VALUES):
    """Returns a new "thinned" dictionary representation of a person based on the passed in
    < swapi_data > dictionary. If an optional < wookiee_data > dictionary is provided by the caller,
    the < swapi_data > dictionary is updated with the < wookiee_data > key-value pairs prior to creating
    the new dictionary representation of the person.

    The new dictionary is constructed by mapping a subset of the < swapi_data > dictionary's
    key-value pairs to the new dictionary based on the provided < keys > dictionary. The
    < keys > dictionary includes a nested "person" dictionary that specifies the following
    new dictionary attributes:

    * the < swapi_data > key-value pairs to be mapped to the new dictionary.
    * the order in which the < swapi_data > key-value pairs are mapped to the new dictionary.
    * the key names to be used in the new dictionary. Each key in < keys > corresponds to
      a key in < swapi_data >. Each value in < keys > represents the (new) key name to be used
      in the new dictionary.

    < swapi_data > values are converted to more appropriate types as outlined below under "Mappings".
    Strings found in < none_values > are converted to < None > irrespective of case. Type
    conversions are delegated to the various < utl.to_*() > functions.

    Retrieving a dictionary representation of the person's home planet is delegated to the
    function `get_homeworld()`. Retrieving a dictionary representation of the person's species
    is delegated to the function `get_species()`. The < planets > and < planet_key > values
    are passed directly to < get_homeworld() > while the < species > and < species_key >
    values are passed directly to < get_species() >.

    The targeted < swapi_data > value is then mapped to the new key when assigning the new key-value
    pair to the "person" dictionary.

    Mappings (old key -> new key):
        url (str) -> url (str)
        name (str) -> name (str | None)
        birth_year (str) -> birth_date (dict | None)
        height (str) -> height_cm (float | None)
        mass (str) -> mass_kg (float | None)
        homeworld (str) -> homeworld (dict | None)
        species (list) -> species (dict | None)
        force_sensitive (str) -> force_sensitive (str | None)

    Parameters:
        keys (dict): Old key to new key mappings
        swapi_data (dict): source data
        wookiee_data (dict): additional data to be combined with < swapi_data >
        planets (tuple): Supplementary planet data
        planets_key (str): key name used in supplemental species data search
        species (tuple): Supplemenatry species data
        species_key (str): key name used in supplemental species data search
        none_values (tuple): strings to convert to None

    Returns:
        dict: new dictionary representation of a person
    """
    person_dict = {}
    if wookiee_data: swapi_data.update(wookiee_data)
    for key, value in keys["person"].items(): 
        if key == 'url':
            person_dict[value] = swapi_data[key] 
        elif key == 'name':
            person_dict[value] = utl.to_none(swapi_data.get(key), none_values) 
        elif key == 'birth_year':
            person_dict[value] = utl.to_none(utl.to_year_era(swapi_data.get(key)), none_values) 
        elif key in ['height', 'mass']:
            person_dict[value] = utl.to_none(utl.to_float(swapi_data.get(key)), none_values) 
        elif key == 'homeworld':
            person_dict[value] = utl.to_none(get_homeworld(keys, swapi_data.get(key), planets, planet_key, none_values), none_values)
        elif key == 'species':
            person_dict[value] = utl.to_none(get_species(keys, swapi_data.get(key)[0], species, species_key, none_values), none_values)
        elif key == 'force_sensitive':
            person_dict[value] = utl.to_none(swapi_data.get(key), none_values) 
        else:
            raise ValueError(f"Invalid key: {key}") 
    return person_dict

    

def create_planet(keys, swapi_data, wookiee_data=None, none_values=NONE_VALUES):
    """Returns a new "thinned" dictionary representation of a planet based on the passed in
    < swapi_data > dictionary. If an optional < wookiee_data > dictionary is provided by the caller,
    the < swapi_data > dictionary is updated with the < wookiee_data > key-value pairs prior to creating
    the new dictionary representation of the droid.

    The new dictionary is constructed by mapping a subset of the < swapi_data > dictionary's
    key-value pairs to the new dictionary based on the provided < keys > dictionary. The
    < keys > dictionary includes a nested "planet" dictionary that specifies the following
    new dictionary attributes:

    * the < swapi_data > key-value pairs to be mapped to the new dictionary.
    * the order in which the < swapi_data > key-value pairs are mapped to the new dictionary.
    * the key names to be used in the new dictionary. Each key in < keys > corresponds to
      a key in < swapi_data >. Each value in < keys > represents the (new) key name to be used
      in the new dictionary.

    < swapi_data > values are converted to more appropriate types as outlined below under "Mappings".
    Strings found in < none_values > are converted to < None > irrespective of case. Type
    conversions are delegated to the various < utl.to_*() > functions.

    The targeted < swapi_data > value is then mapped to the new key when assigning the new key-value
    pair to the "planet" dictionary.

    Mappings (old key -> new key):
        url (str) -> url (str)
        name (str) -> name (str | None)
        region (str) -> region (str | None)
        sector (str) -> sector (str | None)
        suns (str) -> suns (int | None)
        moons (str) -> moons (int | None)
        orbital_period (str) -> orbital_period_days (float | None)
        diameter (str) -> diameter_km (int | None)
        gravity (str) -> gravity_std (float | None)
        climate (str) -> climate (list | None)
        terrain (str) -> terrain (list | None)
        population (str) -> population (int | None)

    Parameters:
        keys (dict): Old key to new key mappings
        swapi_data (dict): source data
        wookiee_data (dict): additional data to be combined with < swapi_data >
        none_values (tuple): strings to convert to None

    Returns:
        dict: new dictionary representation of a planet
    """
    planet_dict = {}
    if wookiee_data:
        swapi_data.update(wookiee_data)
    for key, value in keys['planet'].items():
            if key == "url" :
                planet_dict[value] = swapi_data.get(key)
            elif key in ["name","region","sector"]:
                planet_dict[value] = utl.to_none(swapi_data.get(key),none_values)
            elif key in ["suns","moons","diameter","population"]:
                planet_dict[value] = utl.to_none(utl.to_int(swapi_data.get(key)),none_values)
            elif key == "orbital_period":
                planet_dict[value] = utl.to_none(utl.to_float(swapi_data.get(key)),none_values)   
            elif key == "gravity":
                planet_dict[value] = utl.to_none(utl.to_gravity_value(swapi_data.get(key)),none_values)   
            elif key in ["climate","terrain"]:
                planet_dict[value] = utl.to_none((utl.to_list(swapi_data.get(key),", ")),none_values)  
            else:
                raise ValueError(f"Unexpected key:{key}")
    return planet_dict 




def create_species(keys, swapi_data, wookiee_data=None, none_values=NONE_VALUES):
    """Returns a new "thinned" dictionary representation of a species based on the passed in
    < swapi_data > dictionary. If an optional < wookiee_data > dictionary is provided by the caller,
    the < swapi_data > dictionary is updated with the < wookiee_data > key-value pairs prior to creating
    the new dictionary representation of the droid.

    The new dictionary is constructed by mapping a subset of the < swapi_data > dictionary's
    key-value pairs to the new dictionary based on the provided < keys > dictionary. The
    < keys > dictionary includes a nested "species" dictionary that specifies the following
    new dictionary attributes:

    * the < swapi_data > key-value pairs to be mapped to the new dictionary.
    * the order in which the < swapi_data > key-value pairs are mapped to the new dictionary.
    * the key names to be used in the new dictionary. Each key in < keys > corresponds to
      a key in < swapi_data >. Each value in < keys > represents the (new) key name to be used
      in the new dictionary.

    < swapi_data > values are converted to more appropriate types as outlined below under "Mappings".
    Strings found in < none_values > are converted to < None > irrespective of case. Type
    conversions are delegated to the various < utl.to_*() > functions.

    The targeted < swapi_data > value is then mapped to the new key when assigning the new key-value
    pair to the "species" dictionary.

    Mappings (old key -> new key):
        url (str) -> url (str)
        name (str) -> name (str | None)
        classification (str) -> classification (str | None)
        designation (str) -> designation (str | None)
        average_lifespan (str) -> average_lifespan_yrs (int | None)
        average_height (str) -> average_height_cm (float | None)
        language (str) -> language (str | None)

    Parameters:
        keys (dict): Old key to new key mappings
        swapi_data (dict): source data
        wookiee_data (dict): additional data to be combined with < swapi_data >
        none_values (tuple): strings to convert to None

    Returns:
        dict: new dictionary representation of a planet
    """

    species_dict = {} 
    if wookiee_data:
       swapi_data.update(wookiee_data)
    for key, value in keys["species"].items():
       if key in ["url", "language"] and key in swapi_data: 
           species_dict[value] = swapi_data[key]
       elif key in ["name", "classification", "designation"]:
            species_dict[value] = utl.to_none(swapi_data.get(key), none_values)
       elif key == "average_lifespan":
            species_dict[value] = utl.to_none(utl.to_int(swapi_data.get(key)), none_values) 
       elif key == "average_height":
            species_dict[value] = utl.to_none(utl.to_float(swapi_data.get(key)), none_values) 
       else:
           raise ValueError(f"Unexpected key: {key}") 
    return species_dict



def create_starship(keys, swapi_data, wookiee_data=None, none_values=NONE_VALUES):
    """Returns a new "thinned" dictionary representation of a starship based on the passed in
    < swapi_data > dictionary. If an optional < wookiee_data > dictionary is provided by the caller,
    the < swapi_data > dictionary is updated with the < wookiee_data > key-value pairs prior to
    creating the new dictionary representation of the droid.

    The new dictionary is constructed by mapping a subset of the < swapi_data > dictionary's
    key-value pairs to the new dictionary based on the provided < keys > dictionary. The
    < keys > dictionary includes a nested "starship" dictionary that specifies the following
    new dictionary attributes:

    * the < swapi_data > key-value pairs to be mapped to the new dictionary.
    * the order in which the < swapi_data > key-value pairs are mapped to the new dictionary.
    * the key names to be used in the new dictionary. Each key in < keys > corresponds to
      a key in < swapi_data >. Each value in < keys > represents the (new) key name to be used
      in the new dictionary.

    < swapi_data > values are converted to more appropriate types as outlined below under "Mappings".
    Strings found in < none_values > are converted to < None > irrespective of case. Type
    conversions are delegated to the various < utl.to_*() > functions.

    The targeted < swapi_data > value is then mapped to the new key when assigning the new key-value
    pair to the "starship" dictionary.

    Assigning crew members and passengers consitute separate operations.

    Mappings (old key -> new key):
        url (str) -> url (str)
        name (str) -> name (str | None)
        model (str) -> model (str | None)
        starship_class (str) -> starship_class (str | None)
        manufacturer (str) -> manufacturer (str | None)
        length (str) -> length_m (float | None)
        hyperdrive_rating (str) -> hyperdrive_rating (float | None)
        MGLT (str) -> max_megalight_hr (int | None)
        max_atmosphering_speed (str) -> max_atmosphering_speed_kph (int | None)
        crew (str) -> crew_size (int | None)
        crew_members (list) -> crew_members (list | None)
        passengers (str) -> max_passengers (int | None)
        passengers_on_board (list) -> passengers_on_board (list | None)
        cargo_capacity (str) -> cargo_capacity_kg (int | None)
        consumables (str) -> consumables (str | None)
        armament (list) -> armament (list | None)

    Parameters:
        keys (dict): Old key to new key mappings
        swapi_data (dict): source data
        wookiee_data (dict): additional data to be combined with < swapi_data >
        none_values (tuple): strings to convert to None

    Returns:
        dict: new dictionary representation of a planet
    """
    starship_dict = {} 
    if wookiee_data:
       swapi_data.update(wookiee_data)

    for key, value in keys["starship"].items():
        if key in ["url", "consumables"] and key in swapi_data: 
            starship_dict[value] = swapi_data[key]
        elif key in ["name", "model", "starship_class", "manufacturer"]: 
            starship_dict[value] = utl.to_none(swapi_data.get(key), none_values)
        elif key in ["length", "hyperdrive_rating"]:
            starship_dict[value] = utl.to_none(utl.to_float(swapi_data.get(key)), none_values) 
        elif key in ["MGLT", "max_atmosphering_speed", "crew", "passengers", "cargo_capacity"]:
            starship_dict[value] = utl.to_none(utl.to_int(swapi_data.get(key)), none_values)
        elif key in ["crew_members", "passengers_on_board", "armament"]:
            starship_dict[value] = utl.to_none(utl.to_list(swapi_data.get(key), ", "), none_values)
        return starship_dict



def get_homeworld(keys, swapi_url, planets=None, planet_key="name", none_values=NONE_VALUES):
    """Retrieves a SWAPI representation of a planet using the provided < swapi_url >.
    If an optional < planets > list is provided by the caller the function
    < utl.get_nested_dict() > is called to retrieve a second dictionary representation
    of the planet. Both the SWAPI and Wookieepedia dictionaries along with the < keys >
    and < none_values > are then passed to the function < create_planet() > in order to
    return an enhanced dictionary representation of the planet to the caller.

    Parameters:
        keys (dict): Old key to new key mappings
        swapi_url (str): SWAPI uniform resource locator
        planets (list): supplemental planet data
        planet_key (str): key name used in supplemental planet data search
        none_values (tuple): strings to convert to None

    Returns:
        dict: "thinned" dictionary representation of a planet
    """

    planet_dict = get_swapi_resource(swapi_url) 
    wookiee_dict = None
    if planets:
       wookiee_dict = utl.get_nested_dict(planets, planet_key, planet_dict.get("name"))
    return create_planet(keys, planet_dict, wookiee_dict, none_values)




def get_species(keys, swapi_url, species=None, species_key="name", none_values=NONE_VALUES):
    """Retrieves a SWAPI representation of a species using the provided < swapi_url >.
    If an optional < species > list is provided by the caller the function
    < utl.get_nested_dict() > is called to retrieve a second dictionary representation
    of the species. Both the SWAPI and Wookieepedia dictionaries along with the < keys >
    and < none_values > are then passed to the function < create_species() > in order to
    return an enhanced dictionary representation of the species to the caller.

    Parameters:
        keys (dict): Old key to new key mappings
        swapi_url (str): SWAPI uniform resource locator
        species (list): supplemental species data
        species_key (str): key name used in supplemental species data search
        none_values (tuple): strings to convert to None

    Returns:
        dict: "thinned" dictionary representation of a species
    """

    species_dict = get_swapi_resource(swapi_url)
    wookiee_dict = None
    if species:
        wookiee_dict = utl.get_nested_dict(species, species_key, species_dict.get("name")) 
    return create_species(keys, species_dict, wookiee_dict, none_values)




def get_most_viewed_episode(episodes): #ps4_solution
    """Identifies and returns a list of one or more episodes with the highest recorded
    viewership. Ignores episodes with no viewship value. Includes in the list only those
    episodes that tie for the highest recorded viewership. If no ties exist only one
    episode will be returned in the list. Delegates to the function < has_viewer_data >
    the task of determining if the episode includes viewership "episode_us_viewers_mm"
    numeric data.

    Parameters:
        episodes (list): nested episode dictionaries

    Returns:
        list: episode(s) with the highest recorded viewership.
    """

    max_viewership = 0
    most_viewed_episodes = [] 

    for episode in episodes:
        if has_viewer_data(episode):  
            viewership = episode['episode_us_viewers_mm']
            if viewership > max_viewership:  
                max_viewership = viewership
                most_viewed_episodes = [episode]
            elif viewership == max_viewership: 
                most_viewed_episodes.append(episode)
    return most_viewed_episodes


def get_news_desks(articles, none_values):
    """Returns a list of New York Times news desks sourced from the passed in
    < articles > list. Accesses the news desk name from each article's "news_desk"
    key-value pair. Filters out duplicates in order to guarantee uniqueness. The
    list sorted alphanumerically before being returned to the caller.

    Delegates to the function < utl.to_none > the task of converting "news_desk"
    values that equal "None" (a string) to None. Only news_desk values that are "truthy"
    (i.e., not None) are returned in the list.

    Parameters:
        articles (list): nested dictionary representations of New York Times articles
        none_values (tuple): strings to convert to None

    Returns:
        list: news desk strings (no duplicates) sorted alphanumerically
    """

    news_desks = []  
    for article in articles:
        news_desk = article.get("news_desk")
        news_desk = utl.to_none(news_desk, none_values)  
        if news_desk and news_desk not in news_desks: 
            news_desks.append(news_desk)
        news_desks.sort()
    return news_desks


def get_swapi_resource(url, params=None, timeout=10):
    """Retrieves a deep copy of a SWAPI resource from either the local < cache >
    dictionary or from a remote API if no local copy exists. Delegates to the function
    < utl.create_cache_key > the task of minting a key that is used to identify a cached
    resource. If the desired resource is not located in the cache, delegates to the
    function < get_resource > the task of retrieving the resource from SWAPI.
    A deep copy of the resource retrieved remotely is then added to the local < cache > by
    mapping it to a new < cache[key] >. The mutated cache is written to the file
    system before a deep copy of the resource is returned to the caller.

    WARN: Deep copying is required to guard against possible mutatation of the cached
    objects when dictionaries representing SWAPI entities (e.g., films, people, planets,
    species, starships, and vehicles) are modified by other processes.

    Parameters:
        url (str): a uniform resource locator that specifies the resource.
        params (dict): optional dictionary of querystring arguments.
        timeout (int): timeout value in seconds

    Returns:
        dict|list: requested resource sourced from either the local cache or a remote API
      """

    key = utl.create_cache_key(url, params)
    if key in cache.keys():
        return copy.deepcopy(cache[key]) # recursive copy of objects
    else:
        resource = utl.get_resource(url, params, timeout)
        cache[key] = copy.deepcopy(resource) # recursive copy of objects
        utl.write_json(CACHE_FILEPATH, cache) # persist mutated cache
        return resource


def group_articles_by_news_desk(news_desks, articles): #week 14 + ps 11 solution
    """Returns a dictionary of "news desk" key-value pairs that group the passed in
    < articles > by their parent news desk. The passed in < news_desks > list provides
    the keys while each news desk's < articles > are stored in a list and assigned to
    the appropriate "news desk" key. Each key-value pair is structured as follows:

    {
        < news_desk_name_01 >: [{< article_01 >}, {< article_05 >}, ...],
        < news_desk_name_02 >: [{< article_20 >}, {< article_31 >}, ...],
        ...
    }

    Each dictionary that represents an article is a "thinned" version of the New York Times
    original and consists of the following key-value pairs ordered as follows:

    Key order:
        web_url
        headline_main (new name)
        news_desk
        byline_original (new name)
        document_type
        material_type (new name)
        abstract
        word_count
        pub_date

    Parameters:
        news_desks (list): list of news_desk names
        articles (list): nested dictionary representations of New York Times articles

    Returns
        dict: key-value pairs that group articles by their parent news desk
    """
    articles_news_desk = {}
    for news_desk in news_desks:
        articles_news_desk[news_desk] = []
        for article in articles:
            if article["news_desk"] == news_desk:
                articles_news_desk[news_desk].append({
                    "web_url":article["web_url"],
                    "headline_main":article["headline"]['main'],
                    "news_desk":article["news_desk"],
                    "byline_original":article["byline"]["original"],
                    "document_type":article["document_type"],
                    "material_type":article["type_of_material"],
                    "abstract":article["abstract"],
                    "word_count":article["word_count"],
                    "pub_date":article["pub_date"]
                })
    return articles_news_desk



def has_viewer_data(episode): #week_11 solution
    """Checks the truth value of an episode's "episode_us_viewers_mm" key-value pair. Returns
    True if the truth value is "truthy" (e.g., numeric values that are not 0, non-empty sequences
    or dictionaries, boolean True); otherwise returns False if a "falsy" value is detected (e.g.,
    empty sequences (including empty or blank strings), 0, 0.0, None, boolean False)).

    Parameters:
        episode (dict): represents an episode

    Returns:
        bool: True if "episode_us_viewers_mm" value is truthy; otherwise False
    """

    try:
        if 'episode_us_viewers_mm' in episode:
            value = episode['episode_us_viewers_mm']
            if value: 
                return True
            else:  
                return False
        else:
            return False
    except:
        # Return False in case of any exception
        return False


def main():
    """Entry point for program.

    Parameters:
        None

    Returns:
        None
    """

    keys = {
        "droid": {
            "url": "url",
            "name": "name",
            "model": "model",
            "manufacturer": "manufacturer",
            "create_year": "create_date",
            "height": "height_cm",
            "mass": "mass_kg",
            "equipment": "equipment",
            "instructions": "instructions"
            },
        "person": {
            "url": "url",
            "name": "name",
            "birth_year": "birth_date",
            "height": "height_cm",
            "mass": "mass_kg",
            "homeworld": "homeworld",
            "species": "species",
            "force_sensitive": "force_sensitive"
            },
        "planet": {
            "url": "url",
            "name": "name",
            "region": "region",
            "sector": "sector",
            "suns": "suns",
            "moons": "moons",
            "orbital_period": "orbital_period_days",
            "diameter": "diameter_km",
            "gravity": "gravity_std",
            "climate": "climate",
            "terrain": "terrain",
            "population": "population"
        },
        "species": {
            "url": "url",
            "name": "name",
            "classification": "classification",
            "designation": "designation",
            "average_lifespan": "average_lifespan_yrs",
            "average_height": "average_height_cm",
            "language": "language"
        },
        "starship": {
            "url": "url",
            "name": "name",
            "model": "model",
            "starship_class": "starship_class",
            "manufacturer": "manufacturer",
            "length": "length_m",
            "hyperdrive_rating": "hyperdrive_rating",
            "MGLT": "max_megalight_hr",
            "max_atmosphering_speed": "max_atmosphering_speed_kph",
            "crew": "crew_size",
            "crew_members": "crew_members",
            "passengers": "max_passengers",
            "passengers_on_board": "passengers_on_board",
            "cargo_capacity": "cargo_capacity_kg",
            "consumables": "consumables",
            "armament": "armament"
        }
    }

    # 10.1 CHALLENGE 01

    # 10.1.2
    assert utl.to_none('', NONE_VALUES) == None
    assert utl.to_none('N/A ', NONE_VALUES) == None
    assert utl.to_none(' unknown', NONE_VALUES) == None
    assert utl.to_none('Yoda', NONE_VALUES) == 'Yoda'
    assert utl.to_none(('41BBY', '19BBY'), NONE_VALUES) == ('41BBY', '19BBY')

    # 10.1.4
    assert utl.to_float('4') == 4.0
    assert utl.to_float('506,000,000.9999') == 506000000.9999
    assert utl.to_float('Darth Vader') == 'Darth Vader'

    # 10.1.6
    assert utl.to_int('506') == 506
    assert utl.to_int('506,000,000.9999') == 506000000
    assert utl.to_int('Ahsoka Tano') == 'Ahsoka Tano'

    # 10.1.8
    assert utl.to_list('Use the Force') == ['Use', 'the', 'Force']
    assert utl.to_list('X-wing|Y-wing', '|') == ['X-wing', 'Y-wing']
    assert utl.to_list([506, 507], ', ') == [506, 507]


    # 10.2 CHALLENGE 02

    # 10.2.2
    clone_wars_episodes = utl.read_csv_to_dicts("data-clone_wars_episodes.csv")

    # 10.2.4
    # TODO Implement loop; increment count
    count = 0
    for episode in clone_wars_episodes:
       if has_viewer_data(episode):
        count += 1
    print(f"\n10.2.4 Episodes w/viewership data (n={len(clone_wars_episodes)}) = {count}")


    # 10.3 Challenge 03 #ps11_solution

    # 10.3.2
    # TODO Call function; assign return value; write to file
    clone_wars_episodes = convert_episode_values(clone_wars_episodes,NONE_VALUES)
    utl.write_json("episodes_converted.json", clone_wars_episodes)


    # 10.4 Challenge 04

    # 10.4.2
    most_viewed_episode= get_most_viewed_episode(clone_wars_episodes)
    print(f"\n10.4.2 Most viewed episode = {most_viewed_episode}")


    # 10.5 Challenge 05

    # 10.5.2
    # TODO Call function; assign return value
    director_episode_counts = count_episodes_by_director(clone_wars_episodes)

    # TODO Uncomment and sort
    # Sort by count (descending), last name (ascending)
    director_episode_counts = {
        director: count
        for director, count
        in sorted(director_episode_counts.items(), key=lambda x: (-x[1], x[0].split()[-1]))
        }

    # TODO write to file
    utl.write_json("stu-clone_wars-director_episode_counts.json",director_episode_counts)


    # 10.6 CHALLENGE 06

    # 10.6.2
    # TODO Call functions; assign return values; write to file
    articles = utl.read_json("./data-nyt_star_wars_articles.json")
    news_desks = get_news_desks(articles, NONE_VALUES)
    utl.write_json("stu-nyt_news_desks.json",news_desks)


    # 10.7 CHALLENGE 07

    # 10.7.2
    # TODO Call function; assign return value; write to file
    news_desk_articles = group_articles_by_news_desk(news_desks,articles)
    utl.write_json("stu-nyt_news_desk_articles.json",news_desk_articles)


    # 10.8 CHALLENGE 08

    mean_word_counts = {}
    
    # 10.8.2
    ignore = ('Business Day', 'Movies')
    # TODO Implement loop; accumulate key-value pairs; write to file
    for key, value in news_desk_articles.items():
        if key not in ignore:
            mean_word_count = calculate_articles_mean_word_count(value)
            mean_word_counts[key] = mean_word_count

    utl.write_json("stu-nyt_news_desk_mean_word_counts.json",mean_word_counts)


    # 10.9 CHALLENGE 09

    # 10.9.2
    # TODO Read file; call functions; write to files
    wookiee_planets = utl.read_csv_to_dicts("data-wookieepedia_planets.csv")
    wookiee_dagobah = utl.get_nested_dict(wookiee_planets,'name','dagobah')
    utl.write_json("wookiee_dagobah.json",wookiee_dagobah)

    wookiee_haruun_kal = utl.get_nested_dict(wookiee_planets,'system',"AI'Har system")
    utl.write_json("wookiee_haruun_kal.json",wookiee_haruun_kal)
    # 10.10 CHALLENGE 10

    # 10.10.2
    assert utl.to_gravity_value('1 standard') == 1.0
    # assert utl.to_gravity_value('5STANDARD') == 5.0
    assert utl.to_gravity_value('0.98') == 0.98
    assert utl.to_gravity_value('N/A') == 'N/A'

    # 10.10.4
    # TODO Call functions; write to files
    swapi_tatooine = get_swapi_resource(SWAPI_PLANETS,{"search":"tatooine"})
    tatooine = create_planet(keys,swapi_tatooine)
    utl.write_json('stu-tatooine-v1p0.json',tatooine)

    wookiee_tatooine = utl.get_nested_dict(wookiee_planets,"name",swapi_tatooine['name'])
    tatooine = create_planet(keys, swapi_tatooine, wookiee_tatooine)
    utl.write_json('fxt-tatooine-v1p1.json',tatooine)


    # 10.11 CHALLENGE 11

    # 10.11.2
    assert utl.to_year_era('1032BBY') == {'year': 1032, 'era': 'BBY'}
    assert utl.to_year_era('19BBY') == {'year': 19, 'era': 'BBY'}
    assert utl.to_year_era('0ABY') == {'year': 0, 'era': 'ABY'}
    assert utl.to_year_era('Chewbacca') == 'Chewbacca'

    # 10.11.4
    swapi_r2_d2 = get_swapi_resource(SWAPI_ENDPOINT[0], {"search": "R2-D2"}, ", ") 
    wookiee_droids = utl.read_json('data-wookieepedia_droids.json')
    wookiee_r2_d2 = utl.get_nested_dict(wookiee_droids, 'name', swapi_r2_d2['name']) 
    r2_d2 = create_droid(keys, swapi_r2_d2, wookiee_r2_d2)
    utl.write_json('stu-r2_d2.json', r2_d2) 



    # 10.12 Challenge 12

    # 10.12.2
    # TODO Call functions; write to file
    swapi_human_species = get_swapi_resource(SWAPI_SPECIES, {"search", "human"})
    human_species = create_species(keys, swapi_human_species) 
    utl.write_json('human_species.json', human_species)


    # 10.13 Challenge 13

    # 10.13.2
    # TODO Call functions; write to file
    swapi_anakin = get_swapi_resource(SWAPI_PEOPLE, {"search": "Anakin Skywalker"}) 
    swapi_anakin_homeworld = get_homeworld(keys, swapi_anakin['homeworld'], wookiee_planets) 
    utl.write_json('stu-anakin_homeworld.json', swapi_anakin_homeworld)


    # 10.14 Challenge 14

    # 10.14.2
    # TODO Call function; write to file
    swapi_anakin_species = get_species(keys, swapi_anakin['species'][0]) 
    utl.write_json('stu-anakin_species.json', swapi_anakin_species)


    # 10.15 CHALLENGE 15

    # 10.15.2
    # TODO Read file; call functions; write to files
    wookiee_people = utl.read_json('data-wookieepedia_people.json')
    wookiee_anakin = utl.get_nested_dict(wookiee_people, 'name', 'Anakin SkyWalker') 
    anakin = create_person(keys, swapi_anakin, wookiee_anakin, wookiee_planets) 
    utl.write_json('stu-anakin_skywalker.json', anakin)

    swapi_obi_wan = get_swapi_resource(SWAPI_PEOPLE[0], {"search”: ”obi-wan kenobi"}) 
    wookiee_obi_wan = utl.get_nested_dict(wookiee_people, 'name', 'Obi-Wan Kenobi') 
    obi_wan = create_person(keys, swapi_obi_wan, wookiee_obi_wan, wookiee_planets) 
    utl.write_json('stu-obi_wan_kenobi.json', obi_wan)


    # 10.16 CHALLENGE 16

    # 10.16.2
    # TODO Read file; call functions; write to file
    wookiee_starships = utl.read_csv_to_dicts('data-wookieepedia_starships.csv') 
    wookiee_twilight = utl.get_nested_dict(wookiee_starships, 'name', 'Twilight') 
    twilight = create_starship(keys, SWAPI_STARSHIPS, wookiee_twilight, NONE_VALUES) 
    utl.Write_json('stu-twilight.json', twilight)


    # 10.17 CHALLENGE 17

    # 10.17.2
    # TODO Call functions; write to files
    swapi_padme = get_swapi_resource(SWAPI_PEOPLE, {"search": "padme amidala"}) 
    wookiee_padme = utl.get_nested_dict(wookiee_people, 'name', 'PadmAo Amidala')
    padme = create_person(keys, swapi_padme, wookiee_padme, wookiee_planets) 
    utl.write_json('stu-padme_amidala.json', padme)

    swapi_c_3po = get_swapi_resource(SWAPI_ENDPOINT[0], {"search": "C-3PO"}, ", ") 
    wookiee_c_3po = utl.get_nested_dict(wookiee_droids, 'name', swapi_c_3po['name']) 
    c_3po = create_droid(keys, swapi_c_3po, wookiee_c_3po)
    utl.write_json('stu-c_3po.json', c_3po)


    # 10.17.2.5-6
    # TODO Board passengers
    twilight['passengers_on_board'] = board_passengers(twilight['max_passengers'], [padme, c_3po,r2_d2] )


    # 10.18 CHALLENGE 18

    # 10.18.2
    # TODO Assign crew members
    twilight['crew_members'] = assign_crew_members(twilight['crew_size'], ['pilot', 'copilot'], [anakin, obi_wan])

    # 10.18.3
    # TODO Add instructions
    r2_d2['instructions'] = map(lambda x: x, ['Power up the engines']) 


    # 10.19 CHALLENGE 19

    # 10.19.1
    # TODO List comprehension; sort with lambda; write to file
    planets = [create_planet(keys, planet, wookiee_planets) for planet in wookiee_planets] 
    planets.sort(key=lambda x: x['name'], reverse=True)
    utl.write_json('stu-planets_sorted_name.json', planets)


    # 10.19.2.1
    # TODO Call function
    naboo = utl.get_nested_dict(planets, 'diameter_km', 12120)

    # 10.19.2.3
    # TODO Add instructions
    r2_d2['instructions'].append(f'Plot course for Naboo, {naboo["region"]}, {naboo["sector"]}')

    # 10.19.3
    # TODO Sort list with lambda; write to file
    planets_diameter_km = planets.sort(key=lambda x: (x['diameter_km'] if x['diameter_km'] is not None else float('-inf'), x['name']), reverse=True)
    utl.write_json('stu-planets_sorted_diameter.json'. planets_diameter_km)

    # 10.20 CHALLENGE 20

    # 10.20.1
    # TODO Add instruction; write to file
    r2_d2['instructions'].append('Release the docking clamp')
    utl.write_json('stu-twilight_departs.json', twilight)


if __name__ == '__main__':
    main()
