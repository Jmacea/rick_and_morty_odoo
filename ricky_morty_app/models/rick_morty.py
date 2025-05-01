import requests
import pandas as pd
import random as ran
import logging
import base64

from odoo import api, fields, models
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)


class RickAndMortyCharacters(models.Model):
    _name = 'rick.morty.characters'
    _description = 'Rick Morty Characters'
    _rec_name = 'characters_name'

    characters_id = fields.Integer(string='Id')
    characters_name = fields.Char(string='Name')
    characters_species = fields.Char(string='Species')
    characters_status = fields.Selection([
        ('Alive', 'Alive'),
        ('Dead', 'Dead'),
        ('unknown', 'unknown'),
    ], string='Status')
    characters_type = fields.Char(string="Type")
    characters_gender = fields.Selection([
        ('Female', 'Female'),
        ('Male', 'Male',),
        ('Genderless', 'Genderless'),
        ('unknown', 'unknown')
    ], string='Gender')
    characters_location = fields.Char(string='Location')
    characters_origin = fields.Char(string='Origin')
    image_url = fields.Char(string="Image URL")
    characters_image = fields.Binary(string='Image', store=True,
                                     compute="_compute_image",
                                     attachment=False)

    def get_image_from_url(self, url):
        data = ""
        try:
            data = base64.b64encode(requests.get(url.strip()).content).replace(b"\n", b"")
        except Exception as e:
            _logger.warning("Can’t load the image from URL %s" % url)
            logging.exception(e)
        return data

    @api.depends("image_url")
    def _compute_image(self):
        for record in self:
            characters_image = None
            if record.image_url:
                characters_image = self.get_image_from_url(record.image_url)
            record.update({"characters_image": characters_image})

    def random_characters(self):
        num = ran.randint(1, 42)
        url = "https://rickandmortyapi.com/api/character/"
        response = requests.get(url+'?page='+str(num)).json()
        info = response['results'][:10]
        df = pd.DataFrame(info)
        for index, row in df.iterrows():
            self.env['rick.morty.characters'].create({
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
        return True
