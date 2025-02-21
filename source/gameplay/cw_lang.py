from source.gameplay.game_logic import Ability, Effect
# Ability(Trigger(), [DealDamage(self, Choice(TargetTag.Foe_Creatures), 1)])

def split_codes(codes, symbol):
    continues = 0
    while continues != len(codes):
        continues = 0
        for item in codes:
            if symbol not in item:
                continues += 1
                continue
            for part in str(item).split(symbol):
                codes.append(part)
            codes.remove(item)
            break

# def get_effect_from_code(code, entity) -> Effect | None:
#     match code.split('(')[0]:
#         case "deal_dmg":
#             print('found deal damage effect')
#         case _:
#             print('\033[93m' + f'Entity {entity}: invalid effect code ({code})' + '\033[0m')
#             return None

# DEAL_DMG(SELECT(FOE_CREATURES, 1), 1)
# {DEAL_DMG: [{SELECT: [FOE_CREATURES, 1]}, 1]}
# {deal_dmg: [{select: [[foe_creatures, 1]]}]}

def get_scope_params(code):
    inner_scope_starts = 0
    inner_scope_ends = 0
    params = []

    index = 0
    run = True

    while run:
        run = False
        for character in code:
            if character == '(':
                inner_scope_starts += 1
            elif character == ')':
                inner_scope_ends += 1
            elif inner_scope_starts - inner_scope_ends == 0 and character == ',':
                params.append(code[:index])
                code = code[index + 1:]

                index = 0
                run = True
                break

            index += 1

    params.append(code[:-1])
    return params

def tokenize_code(code):
    for character in code:
        if character == '(':
            split = code.split('(', 1)
            function = split[0]
            params = get_scope_params(split[1])

            if len(params) == 1:
                return {function : tokenize_code(params[0])}
            else:
                values = list()
                for param in params:
                    values.append(tokenize_code(param))
                return {function : values}
    return code

def parse(cw_code, entity):
    import json

    if cw_code == '':
        return list()

    cw_code = cw_code.replace(" ", "")
    cw_code = cw_code.lower()
    trigger_code = cw_code.split(':')[0]
    effect_codes = [cw_code.split(':')[1]]

    split_codes(effect_codes, ';')

    effects = list()
    for item in effect_codes:
        tokens = tokenize_code(item)
        # print(tokens)
        # print(json.dumps(tokens, sort_keys=False, indent=4))

        # effect = get_effect_from_code(item, entity)
        # if effect is None:
        #     return list()
        # effects.append(effect)

    # return Ability()