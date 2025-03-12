from source.gameplay.game_enums import ConditionType, StatType, TargetTag
from source.gameplay.target import get_targets_from_tag

class Condition:
    def __init__(self, game_object, target, param_a, condition_type, param_b):
        self.game_object = game_object
        self.target = target
        self.param_a = param_a
        self.param_b = param_b
        self.condition_type = condition_type

    def resolve(self):
        current_target = self.target if not isinstance(self.target, TargetTag) \
            else get_targets_from_tag(self.target, self.game_object)
        lhs_param = self.param_a if not isinstance(self.param_a, StatType) \
            else self.get_stat_from_enum(current_target, self.param_a)
        rhs_param = self.param_b if not isinstance(self.param_b, StatType) \
            else self.get_stat_from_enum(current_target, self.param_b)

        match self.condition_type:
            case ConditionType.Equals:
                return lhs_param == rhs_param
            case ConditionType.NotEquals:
                return lhs_param != rhs_param
            case ConditionType.Less_Than:
                return lhs_param < rhs_param
            case ConditionType.Less_Equal:
                return lhs_param <= rhs_param
            case ConditionType.Greater_Than:
                return lhs_param > rhs_param
            case ConditionType.Greater_Equal:
                return lhs_param >= rhs_param
            case ConditionType.Is:
                return lhs_param is rhs_param
            case ConditionType.Is_Not:
                return lhs_param is not rhs_param
            case _:
                raise Exception('Invalid condition type:', self.condition_type)

    @staticmethod
    def get_stat_from_enum(target, stat_enum):
        match stat_enum:
            case StatType.Attack:
                return target.attack
            case StatType.Defense:
                return target.defense
            case StatType.Damage:
                return target.damage
            case _:
                raise Exception(f'Invalid condition type ({stat_enum}): could not get stat')