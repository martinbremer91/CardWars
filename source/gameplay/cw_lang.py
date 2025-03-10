﻿from source.gameplay.ability import Ability
from source.gameplay.effect import DealDamage, ModAttack
from source.gameplay.choice import Choice
from source.gameplay.game_enums import TargetTag
from source.system.console_colors import *

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

def get_function_from_tokens(tokens, game_object):
    if isinstance(tokens, dict):
        for key in tokens.keys():
            params = get_function_from_tokens(tokens[key], game_object)

            match key:
                case 'deal_dmg':
                    return DealDamage(game_object, params[0], params[1])
                case 'choice':
                    return Choice(params[0], params[1])
                case 'mod_atk':
                    return ModAttack(game_object, params[0], params[1], params[2])
                case _:
                    return None

    elif isinstance(tokens, list):
        params = list()
        for item in tokens:
            params.append(get_function_from_tokens(item, game_object))
        return params

    else:
        if not isinstance(tokens, str):
            return None
        try:
            if int(tokens).is_integer():
                return int(tokens)
        except ValueError:
            pass
        match tokens:
            case 'foe_creatures':
                return TargetTag.Foe_Creatures
            case 'self':
                return game_object
            case 'eot':
                return game_object.end_of_turn
            case _:
                return None

def get_triggers_from_code(code, game_object):
    activation_trigger, deactivation_trigger = None, None

    match code:
        case 'sot':
            activation_trigger = game_object.self_enters_play
            deactivation_trigger = game_object.self_exits_play
            trigger = game_object.start_of_turn
        case 'sep':
            trigger = game_object.self_enters_play
        case _:
            return None, None, None

    return trigger, activation_trigger, deactivation_trigger

def parse(cw_code, game_object):
    if cw_code == '':
        return None

    cw_code = cw_code.replace(" ", "")
    cw_code = cw_code.lower()
    trigger_code = cw_code.split(':')[0]

    triggers = get_triggers_from_code(trigger_code, game_object)
    trigger = triggers[0]
    activation_trigger = triggers[1]
    deactivation_trigger = triggers[2]

    if trigger is None:
        print_w(f'{game_object}: invalid trigger code ({trigger_code})')
        return None

    effect_codes = [cw_code.split(':')[1]]
    split_codes(effect_codes, ';')

    effects = list()
    for code in effect_codes:
        tokens = tokenize_code(code)
        effect = get_function_from_tokens(tokens, game_object)

        if effect is None:
            print_w(f'{game_object}: invalid effect code ({code})')
            return None

        effects.append(effect)

    return Ability(trigger, effects, activation_trigger, deactivation_trigger)