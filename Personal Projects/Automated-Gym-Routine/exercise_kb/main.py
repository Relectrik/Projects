# from exercise_clause import ExerciseClause as EC
# from exercise_knowledge_base import ExerciseKnowledgeBase as EKB
# from soreness_aggregator import SorenessAggregator as SA

# sore_chest = EC([("ch", False)])
# sore_tricep = EC([("t", False)])
# unsore_frontdelt = EC([("fd", True)])
# sore_sidedelt = EC([("sd", False)])

# unsore_reardelt = EC([("rd", True)])
# unsore_back = EC([("ba", True)])
# unsore_bicep = EC([("bi", True)])

# unsore_quad = EC([("q", True)])
# unsore_ham = EC([("h", True)])
# unsore_calf = EC([("ca", True)])

# test_base = EKB()

# test_base.tell(sore_chest)
# test_base.tell(sore_tricep)
# test_base.tell(unsore_frontdelt)
# test_base.tell(sore_sidedelt)

# test_base.tell(unsore_reardelt)
# test_base.tell(unsore_back)
# test_base.tell(unsore_bicep)

# test_base.tell(unsore_quad)
# test_base.tell(unsore_ham)
# test_base.tell(unsore_calf)

# muscle_groups = {"ch", "t", "fd", "sd", "rd", "ba", "bi", "q", "h", "ca"}

# example_routines = [
#     {"ch", "t", "fd"},
#     {"ch", "t", "sd"},
#     {"rd", "ba", "bi"},
#     {"ch", "ba", "bi"},
#     {"ch", "ba", "t"},
#     {"q", "h", "ca"},
# ]

# for routine in example_routines:
#     print(routine)
#     for muscle in routine:
#         if not test_base.ask(EC([(muscle, True)])):
#             print(test_base.ask(EC([(muscle, True)])))
#             break
#         else:
#             print("True")

from routine_automator import RoutineAutomator

x = RoutineAutomator("data/workout_record.csv", "data/soreness_record.csv")
x.give_workout()
