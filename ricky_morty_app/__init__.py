from . import models
import requests
import pandas as pd
from odoo import api, SUPERUSER_ID


def create_characters(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    url = "https://rickandmortyapi.com/api/character/"
    characters = ['Rick Sanchez', 'Morty Smith', 'Summer Smith', 'Beth Smith',
                  'Jerry Smith', 'Squanchy', 'Mr. Poopybutthole', 'Birdperson']
    for character in characters:
        response = requests.get(url+'?name='+str(character)).json()
        info = response['results']
        df = pd.DataFrame(info)
        for index, row in df.iterrows():
            env['rick.morty.characters'].create({
                'characters_id': row['id'],
                'characters_name': row['name'],
                'characters_species': row['species'],
                'characters_type': row['type'],
                'characters_status': row['status'],
                'characters_gender': row['gender'],
                'image_url': row['image'],
                'characters_origin': row['origin']['name'],
                'characters_location': row['location']['name'],
            })
