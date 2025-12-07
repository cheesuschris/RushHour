### Project 2 for CMSC421 at UMD

#Contains both the actual work for Project 2 as well as the makeup work for midterm #2

##The original submission is in submission_rush_hour.py.
#Additional .py and .txt files that are merely dependencies include agents.py, csp.py, logic.py, planning.py, requirements.txt, search.py, and utils.py. You may have to pip install -r requirements.txt if things are not working.
#The midterm makeup submission contains the following files:

- check_6x6.py
- check_multistep_actions.py
- example_EC_1.py
- example_EC_2.py
- expanded_rush_hour_driver.py
- expanded_rush_hour_feat[any version].py
- expanded_rush_hour_featsmerged[any version].py

#Within check_6x6, I compare results from expanded_rush_hour_feat1ver1 and example_EC_1. Within check_multistep_actions, I compare results from expanded_rush_hour_feat2ver1 and example_EC_1. These mainly check for correctness. The driver allows you to select these.
#example_EC_1 and example_EC_2 are the given extra credit solutions for the ORIGINAL assignment that I used both as a benchmark against other problem representations, as well as for inspiration in my own version of the problem representation.
#The expanded_rush_hour.py files contain the bulk of the work done for the makeup assignment:

- Within each version of the file contains both the problem description and iteratively the changes since the previous version of the same feature (or merged feature). They also contain steps to take for the next change. They also contain how long it took to ran, as well as compared against the baseline given example_EC_1.py.
- expanded_rush_hour_driver.py allows you to select ANY problem configuration and ANY version of my problem representations and try to solve it w/GraphPlan (be careful, though, as some versions of the problem representation only allow 4x4 grids and not 6x6 grids). The wall and CPU runtime, as well as solution path will be printed. Also, this may take a long time depending on the version of representation you select - check the individual feature files beforehand to know how long the problem should take to solve.
- expanded_rush_hour_feat1ver1.py is my first attempt at the 6x6 grid. I combined parts I liked from example_EC_1 and example_EC_2, and merged them in there. This was VERY SLOW and unoptimized.
- expanded_rush_hour_feat1ver2.py is my second attempt at the 6x6 grid. I expanded upon ONLY example_EC_1 in this version of feature 1 because I thought that Occupies() was a worse represenation than AtHead() and AtTail(), which I later realized was wrong. This performed about the same, still correct but being very slow. This was essentially a dead-end version of feature 1, but I still kept it around and recorded my doing this.
- expanded_rush_hour_feat2ver1.py is my first attempt at the multi-step representation over the single-step representation in a 4x4 grid. I took feat1ver1 (still has occupies) and trimmed it down to a 4x4, then manually created the multi-step moves (yes, lots of actions) for the cars. This performed a great bit better than the 6x6 grid feature, but still was any times slower than the 4x4 grid with the original actionset.
- expanded_rush_hour_featsmergedver1.py contains my first attempt at merging the features within expanded_rush_hour_feat1ver1 and expanded_rush_hour_feat2ver1. Even though they were unoptimized and ran VERY slowly, I still wanted to merge the features first and then see what I could do from there. This performed the worst, and simply printed out "Killed" from the Out-Of-Memory kernel.
- expanded_rush_hour_featsmerged_domainver1.pddl and expanded_rush_hour_featsmerged_problemver1.pddl contain the PDDL REPRESENTATIONS of expanded_rush_hour_featsmergedver1.py (and the sample input I've been using all along). This part of the process helped me debug, merge, get rid of, and brainstorm what I could do to optimize the problem representation.
- expanded_rush_hour_featsmerged_domainver2.pddl and expanded_rush_hour_featsmerged_problemver2.pddl contain the PDDL IMPROVEMENTS over the first version of these .pddl files. Improvements include rows/cols instead of cells, nextrow and nextcol instead of adjacencies (and removing left/up checks), combining at and dir checks, and relying on post-processing (VERY HARD, I'VE FOUND) to chain together into multi-step actions.
- expanded_rush_hour_featsmerged_domainver3.pddl and expanded_rush_hour_featsmerged_problemver2.pddl contain the PDDL IMPROVEMENTS over the first version of these .pddl files. domainver3 is similar to domainver2, except instead of post-processing it instead relies on actually putting multi-step actions into the actionset.
- expanded_rush_hour_featsmergedver2.py contains the domainver2.pddl and problemver2.pddl, translated back into Python. This performed SIGNIFICANTLY BETTER than anything I had previously, albeit still some multiples slower than the same example input problem representation on a 4x4 grid. My post-processing algorithm is O(n^2) since I realized I couldn't be greedy, and linearization deals with time-series. Altering linearized moves is NOT EASY.
- expanded_rush_hour_featsmergedver3.py contains the domainver3.pddl and problemver2.pddl, translated back into Python. This was NOT able to find a solution without OOM kicking in, similar to featsmerged_domainver1. ===THIS WAS SAD, AND GIVEN MORE TIME I WOULD'VE LIKED TO EXPERIMENT MORE WITH THE EXPANDED ACTIONSET (even though it makes the search tree very computationally expensive, are there ways to dynamically generate different sets actions for each node?)===

#Notes:

- The order of these above bullet points is ROUGHLY the order in which I developed these problem representations.
- I went through both post-processing and multi-step actions in the merged features ver2 and ver3 since I could see arguments for why both of them would be desired.
- Given more time, I would've wanted to implement things like the predefined 40-challenges challenge set as defined in the Official Rush Hour. \_I would've also liked to experiment with more representations, such as a dynamically adjusted actionset (is this possible?) in PDDL and maybe even converted back to Python (representing this would probably be easier in Python) --> ===HEAVY EMPHASIS ON THIS, AS I WAS DISAPPOINTED THAT featsmergedver3.py DID NOT WORK OUT.=== I would NOT have wanted to implement bounds, though, like row 3 only containing the exit, since that was clearly defined not to be a part of the rules in this makeup assignment.
- I learned how to describe domains and problems in PDDL using https://fareskalaboud.github.io/LearnPDDL/ &https://editor.planning.domains/# during this assignment.
- The problem representation from featsmergedver2 is slow, but might be reasonable? I think a qualitative look at the code/representation, as well as the algorithm for post-processing would explain better as to how good it is.
