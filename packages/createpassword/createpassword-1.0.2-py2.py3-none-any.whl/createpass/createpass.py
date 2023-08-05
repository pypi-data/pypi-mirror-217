import genepass


def createpassword(suggest_num=10, security_level='strong',length=8, character_sets=None):
    return genepass.suggest_passwords(suggest_num, security_level, length, character_sets)
