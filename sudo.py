import re


def _read_sudoers():
    #make sure file exists
    f = open('/home/ej321278/salt/_modules/sudoers', 'r')
    sudolist = [line for line in f.read().splitlines()]
    f.close()
    return sudolist


def append_user(alias_name, data):
    aliasRE = re.compile("(\w+)(?=\s*?\=)")
    new_sudoers = []
    for line in _read_sudoers():
        if line.startswith('User_Alias'):
            alias = aliasRE.search(line).group(1)
            if alias_name == alias:
                line += ',' + data
                new_sudoers.append(line)
            else:
                new_sudoers.append(line)
        else:
            new_sudoers.append(line)
    return new_sudoers


def _move_sudoers():
    return True


def _write_sudoers(wlist):
    f = open('/home/ej321278/salt/_modules/wsudoers', 'w')
    for line in wlist:
        f.write("%s\n" % line)
    f.close()


def _flatten(wdict):
    wlist = []
    aliases = ['Host_Alias', 'User_Alias', 'Cmnd_Alias']
    for alias in aliases:
        if alias in wdict and wdict[alias]:
            for key, val in wdict[alias].iteritems():
                line = "%s %s = %s " % (alias, key, ', '.join(val))
                wlist.append(line)
    if 'Default' in wdict and wdict['Default']:
        for line in wdict['Default']:
            wlist.append(line)
    if 'Access' in wdict and wdict['Access']:
        for line in wdict['Access']:
            wlist.append(line)
    _write_sudoers(wlist)


def ls():
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
    _flatten(ret)
    return ret
