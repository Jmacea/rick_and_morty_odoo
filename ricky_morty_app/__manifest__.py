{
    'name': "RickyMortyApp",
    'summary': """
        Modulo de Ricky and Morty""",
    'author': "Jmacea",
    'category': 'Tools',
    'sequence': -100,
    'version': '16.0.0.0',
    'depends': ['base'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/ir.cron.xml',
        'views/rick_morty_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': "LGPL-3",
    'post_init_hook': 'create_characters'
}
