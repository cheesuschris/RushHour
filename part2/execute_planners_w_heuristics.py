# Tested in py3.10.18
# pip install unified-planning[engines]
# https://unified-planning.readthedocs.io/en/latest/examples.html
# --> Basic Example
# https://unified-planning.readthedocs.io/en/latest/operation_modes.html#oneshotplanner 

from unified_planning.io import PDDLReader
from unified_planning.shortcuts import *
import unified_planning as up
import time
import psutil
import os

# ----------------------------------------------------------------------
# LOAD PDDL DOMAIN & PROBLEM
# ----------------------------------------------------------------------

up.shortcuts.get_environment().credits_stream = None

reader = PDDLReader()
problem_files = [
    ("6x6_rush_hour_initial_domain.pddl", "6x6_rush_hour_initial_problem.pddl"),
    ("6x6_rush_hour_postprocessed_multistep_domain.pddl", "6x6_rush_hour_multistep_problem.pddl"),
    ("6x6_rush_hour_actionsetprocessed_multistep_domain.pddl", "6x6_rush_hour_multistep_problem.pddl")
]

for (domain_file, problem_file) in problem_files:
    problem = reader.parse_problem(domain_file, problem_file)
    print(f"Loaded domain: {domain_file}")
    print(f"Loaded problem: {problem_file}")
    #INITIALLY TAMER WAS IN HERE BUT THERE ARE DEPENDENCY ISSUES FOR IT: I TRIED LOOKING FOR WAYS TO INSTALL TAMER FOR SO LONG BUT WASN'T SUCCESSFUL
    planner_names = ["pyperplan", "pyperplan-opt", "fast-downward", "fast-downward-opt"] 
    for planner_name in planner_names:
        if planner_name == "fast-downward-opt" or planner_name == "fast-downward":
            with OneshotPlanner(name=planner_name) as planner:
                print(planner.get_configuration_space())
                print(f"Choosing algo {planner_name}")
                start_time = time.process_time() #CPU Time is more valuable
                process = psutil.Process(os.getpid())
                mem_before = process.memory_info().rss / 1024 / 1024
                result = planner.solve(problem)
                mem_after = process.memory_info().rss / 1024 / 1024
                end_time = time.process_time()
                elapsed_time = end_time - start_time
                print(f"Time to solve: {elapsed_time:.4f} seconds")
                print(f"Memory used: {mem_after - mem_before:.2f} MB")
                if result.status == up.engines.PlanGenerationResultStatus.SOLVED_SATISFICING:
                    print(f"{planner_name} planner returned: {result.plan}")
                else:
                    print("No plan found.")
        elif planner_name == "pyperplan":
            heuristics = ["hadd", "hmax", "hsa", "hff", "blind", "lmcut", "landmark"]
            for h in heuristics:
                with OneshotPlanner(name=planner_name, params={"heuristic": h}) as planner:
                    print(planner.get_configuration_space())
                    print(f"Choosing algo {planner_name}")
                    start_time = time.process_time() #CPU Time is more valuable
                    process = psutil.Process(os.getpid())
                    mem_before = process.memory_info().rss / 1024 / 1024
                    result = planner.solve(problem)
                    mem_after = process.memory_info().rss / 1024 / 1024
                    end_time = time.process_time()
                    elapsed_time = end_time - start_time
                    print(f"Time to solve: {elapsed_time:.4f} seconds")
                    print(f"Memory used: {mem_after - mem_before:.2f} MB")
                    if result.status == up.engines.PlanGenerationResultStatus.SOLVED_SATISFICING:
                        print(f"{planner_name} planner returned: {result.plan}")
                    else:
                        print("No plan found.")
        elif planner_name == "pyperplan-opt":
            heuristics = ["blind", "hmax", "lmcut"]
            for h in heuristics:
                with OneshotPlanner(name=planner_name, params={"heuristic": h}) as planner:
                    print(planner.get_configuration_space())
                    print(f"Choosing algo {planner_name}")
                    start_time = time.process_time() #CPU Time is more valuable
                    process = psutil.Process(os.getpid())
                    mem_before = process.memory_info().rss / 1024 / 1024
                    result = planner.solve(problem)
                    mem_after = process.memory_info().rss / 1024 / 1024
                    end_time = time.process_time()
                    elapsed_time = end_time - start_time
                    print(f"Time to solve: {elapsed_time:.4f} seconds")
                    print(f"Memory used: {mem_after - mem_before:.2f} MB")
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
    