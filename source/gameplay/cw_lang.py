from source.gameplay.game_logic import Ability, Effect, DealDamage, Choice
from source.gameplay.gameplay_enums import TargetTag


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

def get_function_from_tokens(tokens, entity):
    if isinstance(tokens, dict):
        for key in tokens.keys():
            params = get_function_from_tokens(tokens[key], entity)

            match key:
                case 'deal_dmg':
                    return DealDamage(entity, params[0], params[1])
                case 'choice':
                    return Choice(params[0], params[1])
                case _:
                    return None

    elif isinstance(tokens, list):
        params = list()
        for item in tokens:
            params.append(get_function_from_tokens(item, entity))
        return params

    else:
        if not isinstance(tokens, str):
            return None
        if tokens.isdigit():
            return int(tokens)
        match tokens:
            case 'foe_creatures':
                return TargetTag.Foe_Creatures
            case _:
                return None

def parse(cw_code, entity):
    if cw_code == '':
        return list()

    cw_code = cw_code.replace(" ", "")
    cw_code = cw_code.lower()
    trigger_code = cw_code.split(':')[0]
    effect_codes = [cw_code.split(':')[1]]

    split_codes(effect_codes, ';')

    effects = list()
    for code in effect_codes:
        tokens = tokenize_code(code)

        import json
        print(tokens)
        #print(json.dumps(tokens, sort_keys=False, indent=4))
        print('')

        effect = get_function_from_tokens(tokens, entity)

        if effect is None:
            print('\033[93m' + f'Entity {entity}: invalid effect code ({code})' + '\033[0m')
            return list()

        effects.append(effect)

    # return Ability()