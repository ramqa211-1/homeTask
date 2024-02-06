import requests
import unittest

class TestPokemon(unittest.TestCase):
    def test_get_pokemon_types(self):
        url = 'https://pokeapi.co/api/v2/type'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200, f"Failed to fetch Pokémon types: {response.status_code}")
        # Parse the JSON data
        types_data = response.json()
        self.assertEqual(len(types_data['results']), 20, "Unexpected number of Pokémon types.")
        fire_type_id = None
        for type_entry in types_data['results']:
            if type_entry['name'] == 'fire':
                fire_type_id = type_entry['url'].split('/')[-2]
                break
        self.assertIsNotNone(fire_type_id, "Fire type not found.")
        print(f"The ID of the 'Fire' type is {fire_type_id}.")
        # Fetch the list of Fire Pokemon
        fire_type_url = f'https://pokeapi.co/api/v2/type/{fire_type_id}'
        fire_type_response = requests.get(fire_type_url)
        self.assertEqual(fire_type_response.status_code, 200, f"Failed to fetch Fire type Pokémon: {fire_type_response.status_code}")
        fire_pokemon_data = fire_type_response.json()

        does_charmander_found = any(
            pokemon['pokemon']['name'] == 'charmander' for pokemon in fire_pokemon_data['pokemon'])
        self.assertTrue(does_charmander_found, "Charmander is not in the JSON of Fire Pokémon list.")
        does_bulbasaur_found = any(
            pokemon['pokemon']['name'] == 'bulbasaur' for pokemon in fire_pokemon_data['pokemon'])
        self.assertFalse(does_bulbasaur_found, "Bulbasaur is in the JSON of Fire Pokémon list.")

    def test_validate_heaviest_pokemon(self):
        # Expected weights for the specified Pokémon
        expected_weights = {
            'charizard-gmax': 10000,
            'cinderace-gmax': 10000,
            'coalossal-gmax': 10000,
            'centiskorch-gmax': 10000,
            'groudon-primal': 9997
        }
        fire_pokemon = self.get_fire_pokemon()
        if fire_pokemon:
            # Sort Fire Pokémon by weight in descending order
            heaviest_pokemon = sorted(fire_pokemon, key=lambda x: self.get_pokemon_details(x['pokemon']['name'])['weight'], reverse=True)[:5]

            for pokemon in heaviest_pokemon:
                pokemon_name = pokemon['pokemon']['name']
                actual_weight = self.get_pokemon_details(pokemon_name)['weight']
                expected_weight = expected_weights.get(pokemon_name, None)
                self.assertEqual(actual_weight, expected_weight, f"Validation failed for {pokemon_name}: Expected {expected_weight}, got {actual_weight}")
            print("All validations passed successfully.")
        else:
            print("Validation failed due to missing Fire Pokémon data.")
    def get_fire_pokemon(self):
        fire_type_id = self.get_fire_type_id()
        if fire_type_id:
            fire_type_url = f'https://pokeapi.co/api/v2/type/{fire_type_id}'
            fire_type_response = requests.get(fire_type_url)
            self.assertEqual(fire_type_response.status_code, 200, f"Failed to fetch Fire type Pokémon: {fire_type_response.status_code}")
            return fire_type_response.json()['pokemon']
        else:
            print("Fire type not found.")
            return None
    def get_fire_type_id(self):
        url = 'https://pokeapi.co/api/v2/type'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200, f"Failed to fetch Pokémon types: {response.status_code}")
        types_data = response.json()
        for type_entry in types_data['results']:
            if type_entry['name'] == 'fire':
                return type_entry['url'].split('/')[-2]
        print("Fire type not found.")
        return None

    def get_pokemon_details(self, pokemon_name):
        # Fetch details of a specific Pokémon
        pokemon_url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
        response = requests.get(pokemon_url)
        self.assertEqual(response.status_code, 200, f"Failed to fetch Pokémon details: {response.status_code}")
        return response.json()
if __name__ == '__main__':
    unittest.main()
