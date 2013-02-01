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
    hostAliasRE = re.compile("^\s*Host_Alias")
    userAliasRE = re.compile("^\s*User_Alias")
    cmndAliasRE = re.compile("^\s*Cmnd_Alias")
    aliasRE = re.compile("(\w+)(?=\s*?\=)")
    cmndAlias = {}
    userAlias = {}
    hostAlias = {}
    #aliaslist = [defaultsRE, hostAliasRE, userAliasRE, cmndAliasRE]
    for line in f.read().splitlines():
        if(hostAliasRE.search(line)):
            members = line.split('=')[1].split(",")
            members = [m.lstrip().rstrip() for m in members]
            alias = aliasRE.search(line).group(1)
            if alias in hostAlias:
                hostAlias[alias] += members
            else:
                hostAlias[alias] = members
        if(userAliasRE.search(line)):
            members = line.split('=')[1].split(",")
            members = [m.lstrip().rstrip() for m in members]
            alias = aliasRE.search(line).group(1)
            if alias in userAlias:
                userAlias[alias] += members
            else:
                userAlias[alias] = members
        if(cmndAliasRE.search(line)):
            members = line.split('=')[1].split(",")
            members = [m.lstrip().rstrip() for m in members]
            alias = aliasRE.search(line).group(1)
            if alias in cmndAlias:
                cmndAlias[alias] += members
            else:
                cmndAlias[alias] = members
    f.close()
    ret = {'hostAlias': hostAlias, 'userAlias': userAlias, 'cmndAlias': cmndAlias}
    return ret
