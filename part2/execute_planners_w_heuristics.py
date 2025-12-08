# Tested in py3.10.18
# pip install unified-planning[engines]
# https://unified-planning.readthedocs.io/en/latest/examples.html
# --> Basic Example
# https://unified-planning.readthedocs.io/en/latest/operation_modes.html#oneshotplanner 

from unified_planning.io import PDDLReader
from unified_planning.shortcuts import *
import unified_planning as up
import time

# ----------------------------------------------------------------------
# LOAD PDDL DOMAIN & PROBLEM
# ----------------------------------------------------------------------

reader = PDDLReader()
problem_files = [
    ("blocksworld_domain.pddl", "blocksworld_task.pddl"),
    ("blocksworld_domain2.pddl", "blocksworld_task2.pddl"),
    ("blocksworld_domain3.pddl", "blocksworld_task3.pddl")
]

for (domain_file, problem_file) in problem_files:
    problem = reader.parse_problem(domain_file, problem_file)
    print(f"Loaded domain: {domain_file}")
    print(f"Loaded problem: {problem_file}")

    print("Available planners: ", up.shortcuts.get_environment().factory.engines)
    planner_names = ["fast-downward-opt"] # , 'pyperplan', 'tamer', "fast-downward-opt"
    heuristics = ["hadd", "hlandmarks", "blind", "hmax"] # "hmax", "hadd", "hlandmarks", "hff", "blind"
    for planner_name in planner_names:
        if planner_name == "fast-downward-opt":
            with OneShotPlanner(name=planner_name) as planner:
                print(planner.get_configuration_space())
                print(f"Choosing algo {planner_name}")
                start_time = time.process_time() #CPU Time is more valuable
                result = planner.solve(problem)
                end_time = time.process_time()
                elapsed_time = end_time - start_time
                print(f"Time to solve: {elapsed_time:.4f} seconds")
                if result.status == up.engines.PlanGenerationResultStatus.SOLVED_SATISFICING:
                    print(f"{planner_name} planner returned: {result.plan}")
                else:
                    print("No plan found.")
        for h in heuristics:
            with OneshotPlanner(name=planner_name, params={"heuristic": h}) as planner:
                print(planner.get_configuration_space())
                print(f"Choosing algo {planner_name} and heuristic {h}")
                start_time = time.process_time() #CPU Time is more valuable
                result = planner.solve(problem)
                end_time = time.process_time()
                elapsed_time = end_time - start_time
                print(f"Time to solve: {elapsed_time:.4f} seconds")
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
    