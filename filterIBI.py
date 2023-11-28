'''
Returns a list of indices of values that are out of range and should be removed.
'''
def invalidIbiIndices(ibi):
    invalidIndices = []
    for i, sample in enumerate(ibi):
        if sample > 1500 or sample < 100:
            invalidIndices.append(i)
    return invalidIndices