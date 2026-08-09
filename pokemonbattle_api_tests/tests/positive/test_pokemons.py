import pytest
from utils.helpers import (
    knockout_all_pokemons,
    create_pokemon
)

BASE_URL = "https://api.pokemonbattle.ru/v2"

@pytest.mark.positive
def test_patch_pokemon_name(session):

    knockout_all_pokemons(session)

    pokemon_id = create_pokemon(session)

    new_name = "SuperPokemon"

    response = session.patch(
        f"{BASE_URL}/pokemons",
        json={
            "pokemon_id": pokemon_id,
            "name": new_name
        }
    )

    assert response.status_code == 200

    response = session.get(
        f"{BASE_URL}/pokemons",
        params={
            "pokemon_id": pokemon_id
        }
    )

    pokemon = response.json()["data"][0]

    assert pokemon["name"] == new_name

