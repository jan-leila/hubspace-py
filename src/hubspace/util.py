
def getExpansions(expansions):
    if expansions == None or len(expansions) == 0:
        return ""
    return "?expansions=" + ",".join(expansions)
