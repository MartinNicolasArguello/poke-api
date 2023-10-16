
# simple validation for the creation and edit forms, name and type must be alphabetical,
#  height and weight must be numberical and none can have empty spaces

def validate_pokemon(new_pokemon, origin):

    if (origin == "CREATE"):
        if ((new_pokemon.name).isalpha()
                and len(new_pokemon.name.split(' ')) == 1):
            if ((new_pokemon.type).isalpha()
                    and len(new_pokemon.type.split(' ')) == 1):
                if ((new_pokemon.height).isnumeric()
                        and len(new_pokemon.name.split(' ')) == 1):
                    if ((new_pokemon.weight).isnumeric()
                            and len(new_pokemon.name.split(' ')) == 1):
                        return True
        return False
    else:

        if ((new_pokemon.type).isalpha()
                and len(new_pokemon.type.split(' ')) == 1):
            if ((new_pokemon.height).isnumeric()
                    and len(new_pokemon.name.split(' ')) == 1):
                if ((new_pokemon.weight).isnumeric()
                        and len(new_pokemon.name.split(' ')) == 1):
                    return True
        return False
