from datapack import Datapack, mcfunction

myDatapack = Datapack(
    title = 'My_Datapack',
    author = 'Vianpyro',
    pack_meta = {
        'minecraft_version': '1.16',
        'description': 'Have fun using my first datapack!'
    },
    content = {
        'functions': {
            'test': [
                'say test ok',
                'say test ko'
            ],
            'test2': mcfunction('test')
        },
        'predicates': None
    },
)

myDatapack.content['functions']['test3'] = 'execute at @s run summon pig'

myDatapack.compile()
