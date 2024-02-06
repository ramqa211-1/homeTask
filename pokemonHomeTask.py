import requests
import pytest

def test_get_pokemon_types():
    url = 'https://pokeapi.co/api/v2/type'
    response = requests.get(url)
    assert response.status_code == 200, f"Failed to fetch Pokémon types: {response.status_code}"
    types_data = response.json()
    assert len(types_data['results']) == 20, "Unexpected number of Pokémon types."
    fire_type_id = next(
        (type_entry['url'].split('/')[-2] for type_entry in types_data['results'] if type_entry['name'] == 'fire'),
        None)
    assert fire_type_id is not None, "Fire type not found."
    print(f"The ID of the 'Fire' type is {fire_type_id}.")

    fire_type_url = f'https://pokeapi.co/api/v2/type/{fire_type_id}'
    fire_type_response = requests.get(fire_type_url)
    assert fire_type_response.status_code == 200, f"Failed to fetch Fire type Pokémon: {fire_type_response.status_code}"

    fire_pokemon_data = fire_type_response.json()
    does_charmander_found = any(pokemon['pokemon']['name'] == 'charmander' for pokemon in fire_pokemon_data['pokemon'])
    assert does_charmander_found, "Charmander is not in the JSON of Fire Pokémon list."
    does_bulbasaur_found = any(pokemon['pokemon']['name'] == 'bulbasaur' for pokemon in fire_pokemon_data['pokemon'])
    assert not does_bulbasaur_found, "Bulbasaur is in the JSON of Fire Pokémon list."

def test_validate_heaviest_pokemon():
    expected_weights = {
        'charizard-gmax': 10000,
        'cinderace-gmax': 10000,
        'coalossal-gmax': 10000,
        'centiskorch-gmax': 10000,
        'groudon-primal': 9997
    }
    fire_pokemon = get_fire_pokemon()
    assert fire_pokemon is not None, "Validation failed due to missing Fire Pokémon data."
    heaviest_pokemon = sorted(fire_pokemon, key=lambda x: get_pokemon_details(x['pokemon']['name'])['weight'], reverse=True)[:5]

    for pokemon in heaviest_pokemon:
        pokemon_name = pokemon['pokemon']['name']
        actual_weight = get_pokemon_details(pokemon_name)['weight']
        expected_weight = expected_weights.get(pokemon_name, None)
        assert actual_weight == expected_weight, f"Validation failed for {pokemon_name}: Expected {expected_weight}, got {actual_weight}"
    print("All validations passed successfully.")

def get_fire_pokemon():
    fire_type_id = get_fire_type_id()
    if fire_type_id:
        fire_type_url = f'https://pokeapi.co/api/v2/type/{fire_type_id}'
        fire_type_response = requests.get(fire_type_url)
        assert fire_type_response.status_code == 200, f"Failed to fetch Fire type Pokémon: {fire_type_response.status_code}"
        return fire_type_response.json()['pokemon']
    else:
        print("Fire type not found.")
        return None

def get_fire_type_id():
    url = 'https://pokeapi.co/api/v2/type'
    response = requests.get(url)
    assert response.status_code == 200, f"Failed to fetch Pokémon types: {response.status_code}"
    types_data = response.json()
    fire_type_entry = next((type_entry for type_entry in types_data['results'] if type_entry['name'] == 'fire'), None)
    if fire_type_entry:
        return fire_type_entry['url'].split('/')[-2]
    else:
        print("Fire type not found.")
        return None

def get_pokemon_details(pokemon_name):
    pokemon_url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
    response = requests.get(pokemon_url)
    assert response.status_code == 200, f"Failed to fetch Pokémon details: {response.status_code}"
    return response.json()

if __name__ == '__main__':
    pytest.main()