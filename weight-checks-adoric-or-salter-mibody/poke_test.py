import requests
import webbrowser

def display_pokemon_image_in_browser(pokedex_number):
    """
    Fetches a Pokémon's image URL and opens it in the default web browser.
    """
    try:
        # 1. Construct the API URL
        pokemon_url = f'https://pokeapi.co/api/v2/pokemon/{pokedex_number}/'
        
        # 2. Make the API request
        response = requests.get(pokemon_url)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # 3. Find the Image URL
        pokemon_data = response.json()
        image_url = pokemon_data['sprites']['other']['official-artwork']['front_default']
        
        if not image_url:
            print(f"No official artwork found for Pokedex number {pokedex_number}.")
            return

        # 4. Open the image URL in the default web browser
        print(f"Opening image for Pokedex #{pokedex_number} in your browser...")
        webbrowser.open(image_url)

    except requests.exceptions.RequestException as e:
        print(f"Error: Could not retrieve Pokémon data for Pokedex number {pokedex_number}. Please check the number and your internet connection.")
        print(e)
    except KeyError:
        print(f"Error: The image URL for Pokedex number {pokedex_number} could not be found in the API response.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# --- Example Usage ---

pokedex_num = int(input('Numer pokemona: '))
' https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/26.png
for i in range(pokedex_num, pokedex_num+10):
    display_pokemon_image_in_browser(i)

