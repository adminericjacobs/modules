import re


def ls():
    f = open('/home/ej321278/salt/_modules/sudoers', 'r')
    aliasRE = re.compile("(\w+)(?=\s*?\=)")
    defaultsRE = re.compile("^\s*Defaults")
    defaults = {}
    ret = {'Host_Alias': {},
           'User_Alias': {},
           'Cmnd_Alias': {}
           }
    for line in f.read().splitlines():
        if not line:
            continue
        if line.startswith('#'):
            continue
        for key, val in ret.iteritems():
            if line.startswith(key):
                members = line.split('=')[1].split(",")
                members = [m.lstrip().rstrip() for m in members]
                alias = aliasRE.search(line).group(1)
                if alias in val:
                    val[alias] += members
                else:
                    val[alias] = members
       # if(defaultsRE.search(line)):
       #     value = line.split(' ')[1].lstrip()
       #     ret['Defaults'] += [value]
    f.close()
    return ret
