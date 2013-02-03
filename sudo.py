import re


#def _write_sudoers(elist):
    #write list to file in /var/lock?
    # __salt_call__ cmd visudo check for errors
    # move file and set permissions


def _read_sudoers():
    #make sure file exists
    f = open('/home/ej321278/salt/_modules/sudoers', 'r')
    sudolist = [line for line in f.read().splitlines()]
    f.close()
    return sudolist


#def append():
#    f = [line.rstrip() for line in open('sudoers')]
#    new = open('tsudoers', 'w')
#    for item in f:
#        new.write("%s\n" % item)
#    new.close()


def ls():
    #f = open('/home/ej321278/salt/_modules/sudoers', 'r')
    aliasRE = re.compile("(\w+)(?=\s*?\=)")
    defaults = []
    access = []
    ret = {'Host_Alias': {},
           'User_Alias': {},
           'Cmnd_Alias': {},
           }
    for line in _read_sudoers():
        if not line:
            continue
        if line.startswith('#'):
            continue
        if line.startswith('Defaults'):
            def_value = line.split('Defaults')[1].lstrip()
            defaults.append(def_value)
            continue
        for key, val in ret.iteritems():
            if line.startswith(key):
                members = line.split('=')[1].split(",")
                members = [m.lstrip().rstrip() for m in members]
                alias = aliasRE.search(line).group(1)
                if alias in val:
                    val[alias] += members
                    break
                else:
                    val[alias] = members
                    break
        else:
            access.append(line)
    ret['Defaults'] = defaults
    ret['Access'] = access
    return ret
