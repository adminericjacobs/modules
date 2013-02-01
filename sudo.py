import re


def _parseAlias(line, marker):
    res = {}

    aliasRE = re.compile("\s*%s\s*(\S+)\s*=\s*((\S+,?\s*)+)" % marker)
    m = aliasRE.search(line)
    if(m):
        alias = str(m.group(1))
        nodes = str(m.group(2)).split(",")
        nodes = [node.strip() for node in nodes]
        res[alias] = nodes
    return res


def ls():
    ret = {}
    f = open('/home/ej321278/salt/_modules/sudoers', 'r')
    #defaultsRE = re.compile("^\s*Defaults")
    #hostAliasRE = re.compile("^\s*Host_Alias")
    #userAliasRE = re.compile("^\s*User_Alias")
    #cmndAliasRE = re.compile("^\s*Cmnd_Alias")
    aliasRE = re.compile("(\w+)(?=\s*?\=)")
    cmndAlias = {}
    userAlias = {}
    hostAlias = {}
    for line in f.read().splitlines():
        ret = {'Host_Alias': hostAlias,
               'User_Alias': userAlias,
               'Cmnd_Alias': cmndAlias}
        if not line:
            continue
        if line.startswith('#'):
            continue
        for key, val in ret.iteritems():
            if line.startswith(key):
                members = line.split('=')[1].split(",")
                members = [m.lstrip().rstrip() for m in members]
                alias_name = aliasRE.search(line).group(1)
                if alias_name in val:
                    val[alias_name] += members
                else:
                    val[alias_name] = members
    f.close()
    return ret
