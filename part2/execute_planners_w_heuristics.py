# Tested in py3.10.18
# pip install unified-planning[engines]
# https://unified-planning.readthedocs.io/en/latest/examples.html
# --> Basic Example
# https://unified-planning.readthedocs.io/en/latest/operation_modes.html#oneshotplanner 

from unified_planning.io import PDDLReader
from unified_planning.shortcuts import *
import unified_planning as up
# ----------------------------------------------------------------------
# LOAD PDDL DOMAIN & PROBLEM
# ----------------------------------------------------------------------

reader = PDDLReader()
problem = reader.parse_problem(
    "blocksworld_domain.pddl",
    "blocksworld_task.pddl"
)

print("Available planners: ", up.shortcuts.get_environment().factory.engines)
planner_names = ["tamer"] # , 'pyperplan', 'tamer', "fast-downward-opt"
heuristics = ["hadd", "hlandmarks", "blind", "hmax"] # "hmax", "hadd", "hlandmarks", "hff", "blind"
for planner_name in planner_names:
    for h in heuristics:
        with OneshotPlanner(name=planner_name, params={"heuristic": h}) as planner:
            print(planner.get_configuration_space())
            print(f"Choosing algo {planner_name} and heuristic {h}")
            result = planner.solve(problem)
            if result.status == up.engines.PlanGenerationResultStatus.SOLVED_SATISFICING:
                print(f"{planner_name} planner returned: {result.plan}")
            else:
                print("No plan found.")
                
        plan = result.plan
        with PlanValidator(problem_kind=problem.kind, plan_kind=plan.kind) as validator:
            if validator.validate(problem, plan):
                print('The plan is valid')
            else:
                print('The plan is invalid')
            
# with OneshotPlanner(
#     names=["tamer", "pyperplan"],
#     params=[{"heuristic": "hadd", "weight": 0.8}, {}],
# ) as planner:
#     result = planner.solve(problem)
#     print(result)
    