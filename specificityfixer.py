from snorkel.lf_helpers import *
from snorkel.models import *
from random import randint


def fix_specificity(session, BiomarkerCondition, candidates):
    needsAdding = []
    justAdded = []
    for c in candidates:

        # Create the StableLabel for the adjective candidate
        temp_arr_poses = []
        temp_arr_words = []
        cared_words = []
        for thing in get_left_tokens(c.condition, window=4, attrib="words"):
            temp_arr_words.append(thing)
        for thing in get_left_tokens(c.condition, window=4, attrib="pos_tags"):
            temp_arr_poses.append(thing)
        x = (len(temp_arr_poses) - 1)
        while (x >= 0 and (temp_arr_poses[x] == 'jj' or temp_arr_poses[x] == 'nn')):
            cared_words.append(temp_arr_words[x])
            x -= 1
        to_append_string = ""
        for word in cared_words:
            to_append_string += (word + " ")
        print to_append_string + " added to "+  str(c.condition.get_span())