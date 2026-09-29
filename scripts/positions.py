"""Answer position for new questions: balanced (each block of 4 consecutive ids uses every position once) but not
predictable (the permutation of each block is picked by a hash), so position patterns can't be exploited."""
import hashlib, itertools
PERMS = list(itertools.permutations(range(4)))

def pos(subject, i):
    k = int(hashlib.sha1(f's{subject}-block{i // 4}'.encode()).hexdigest(), 16) % 24
    return PERMS[k][i % 4]
