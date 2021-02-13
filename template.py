from datapack import Datapack, import_from_file

my_datapack_title = 'My_Datapack'

myDatapack = Datapack(
    title = my_datapack_title,
    author = 'Vianpyro',
    pack_meta = {
        'minecraft_version': '1.16.4',
        'description': 'Have fun using my first datapack!'
    },
    content = {
        'functions': {
            'main': [
                'title Vianpyro actionbar {"text":"YAY", "color":"dark_red"}'
            ],
            'load': [
                f'tellraw @a ["", {{"text": "{my_datapack_title} > Successfuly reloaded the datapack!", "color": "green"}}]'
            ],
            'test': [
                'say test ok',
                'say test ko'
            ],
            'test2': import_from_file('test')
        },
        'predicates': {
            'my_predict': {
                "condition": "minecraft:entity_properties",
                "entity": "this",
                "predicate": {
                    "type": "minecraft:player",
                    "flags": {
                        "is_sprinting": True
                    }
                }
            }
        }
    },
    auto_replace=True
)

myDatapack.content['functions']['test3'] = 'execute at @s run summon pig'

myDatapack.compile()
