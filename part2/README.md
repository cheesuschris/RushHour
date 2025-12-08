This contains part 2 of the makeup assignment for CMSC421 midterm #2 at the University of Maryland. The task was to analyze my previously created .pddl files within part 1 against many algorithms and heuristics from the unified-planning library, and create a .csv file that displayed/explained those results.

I imported and renamed the .pddl files from part 1 as the email suggested; all of the .pddl files are now 6x6 rush hour problems:
- blocksworld_domain.pddl and blocksworld_task.pddl are a pair of .pddl files
- Initial domain and Initial problem are a pair of .pddl files
- Postprocessed multistep domain and Multistep problem are a pair of .pddl files
- Actionsetprocessed multistep domain and Multistep problem are a pair of .pddl files

These pairs of files, along with logic for calculating the metrics can be found when exploring execute_planners_w_heuristics.py. The output of running Python file (which took a REALLY long time) are contained within FINAL_OUTPUT.txt. The analyzation of these metrics are contained within analysis.csv.

Notes:
- TOTAL memory expanded (without garbage collection) was not calculated; only memory differences from before and after running the problem solver were calculated. However, there are still some insights to be pulled from this.
- For the POSTPROCESSED multistep domain rows, since in part1 I focused on joining together the multi-step actions in the Python file AFTER the planner ran instead of within the domain, this means that the postprocessed multistep domain rows basically only contain optimzations for the 6x6 grid implementation and NOT for the multistep actions. Multistep actions actually within the .pddl actionset contain both the 6x6 grid implementation and the multistep actions.
- Somewhy, even though fast-downward-opt says that hadd, hmax, hsa, hff, blind, lmcut, landmark are available heuristics, it didn't let me modify these heuristics at all and I couldn't pass in anything to it. This was sad.
- Also, somewhy for me the Tamer planner did not work. Dependency issues swamped me when I tried to use the Tamer planner (which is lame of me I recognize).
- Significant runtime improvements were found: up to 155,000x maximum efficiency improvement from the better .pddl implementaions. Significant space improvements/fluctuations/garbage collections were also unneeded: fluctuations in the 100s of MegaBytes decreased to around 0. Read more specifically in the analysis.csv file or the FINAL_OUTPUT.txt (analysis.csv is probably better).