from dataclasses import dataclass
import json

@dataclass
class SubTest:
    a: int
    b: list


@dataclass
class Test:
    a: int
    b: SubTest

def class2dict(instance, built_dict={}):
    if not hasattr(instance, "__dict__"):
        return instance
    new_subdic = vars(instance)
    for key, value in new_subdic.items():
        new_subdic[key] = class2dict(value)
    return new_subdic


test = Test(1, SubTest(1, []))
print(json.dumps(class2dict(test)))