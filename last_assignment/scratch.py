def main():
    """TODO"""

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

    darth_vader = {
        "name": "Darth Vader",
        "height": "202",
        "mass": "136",
        "hair_color": "none",
        "skin_color": "white",
        "eye_color": "yellow",
        "birth_year": "41.9BBY",
        "gender": "male",
        "homeworld": "https://swapi.py4e.com/api/planets/1/", 
        "films": [
            "https://swapi.py4e.com/api/films/1/",
            "https://swapi.py4e.com/api/films/2/",
            "https://swapi.py4e.com/api/films/3/",
            "https://swapi.py4e.com/api/films/6/"
        ],
        "species": [
            "https://swapi.py4e.com/api/species/1/"
        ],
        "vehicles": [],
        "starships": [
            "https://swapi.py4e.com/api/starships/13/"
        ],
        "created": "2014-12-10T15:18:20.704000Z",
        "edited": "2014-12-20T21:17:50.313000Z",
        "url": "https://swapi.py4e.com/api/people/4/"
    }


    vader = {}

    # TODO Implement loop

    print(f"\n vader = {vader}")


if __name__ == "__main__":
    main()
