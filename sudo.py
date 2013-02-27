import re
import shutil


def __virtual__():
    '''
    Only work on posix-like systems
    '''
    # Disable on these platorms, specific service modules exist:
    disable = ['Windows']
    if __grains__['os'] in disable:
        return False
    return 'sudo'


def _sudoers_list():
    #make sure file exists
    f = open('/etc/sudoerssalt', 'r')
    rlist = [line for line in f.read().splitlines()]
    f.close()
    return rlist


def _sudoers_string():
    #make sure file exists
    f = open('/etc/sudoerssalt', 'r')
    rstring = f.read()
    f.close()
    return rstring


def _write_sudoers(wlist, name='sudoerssalt', path='/etc/'):
    #os.path test if it exsists .join
    f = open('/tmp/sudoers', 'w+')
    for line in wlist:
        f.write("%s\n" % line)
    f.close()
    cmd = 'visudo -c -f /tmp/sudoers'
    check = __salt__['cmd.run_all'](cmd)
    if check['retcode']:
        return check['stderr']
    shutil.copy('/etc/sudoerssalt', '/etc/sudoerssalt.bak')
    shutil.move('/tmp/sudoers', '/etc/sudoerssalt')
    return True


def _flatten(wdict):
    wlist = []
    aliases = ['Host_Alias',
               'User_Alias',
               'Cmnd_Alias',
               ]
    for alias in aliases:
        if alias in wdict and wdict[alias]:
            for key, val in wdict[alias].iteritems():
                line = '%s %s = %s ' % (alias, key, ', '.join(val))
                wlist.append(line)
    if 'Defaults' in wdict and wdict['Defaults']:
        for line in wdict['Defaults']:
            wlist.append('Defaults ' + line)
    if 'Access' in wdict and wdict['Access']:
        for line in wdict['Access']:
            wlist.append(line)
    msg = _write_sudoers(wlist)
    return msg


def alias_append(alias_type, alias_name, data):
    pattern = '\s*(%s)\s*(%s)(?=\s*?\=)' % (alias_type, alias_name)
    aliasRE = re.compile(pattern)
    wlist = []
    for line in _sudoers_list():
        if re.search(aliasRE, line):
            line += ',' + data
            wlist.append(line)
        else:
            wlist.append(line)
    wsudoers = _write_sudoers(wlist)
    return wsudoers


def alias_delete(alias_type, alias_name):
    pattern = '\s*(%s)\s*(%s)(?=\s*?\=)' % (alias_type, alias_name)
    aliasRE = re.compile(pattern)
    wlist = []
    for line in _sudoers_list():
        if re.search(aliasRE, line):
            continue
        else:
            wlist.append(line)
    wsudoers = _write_sudoers(wlist)
    return wsudoers


def alias_set(alias_type, alias_name, data):
    pattern = '\s*(%s)\s*(%s)(?=\s*?\=)' % (alias_type, alias_name)
    aliasRE = re.compile(pattern)
    newalias = "%s %s = %s" % (alias_type, alias_name, data)
    rlist = _sudoers_list()
    rstring = _sudoers_string()
    written = False
    wlist = []
    if re.search(aliasRE, rstring):
        for line in rlist:
            if re.search(aliasRE, line):
                wlist.append(newalias)
            else:
                wlist.append(line)
    else:
        wlist = []
        for line in rlist:
            if not line:
                wlist.append(line)
                continue
            if line.startswith('#'):
                wlist.append(line)
                continue
            if not written:
                if '# Added by Salt' in rlist:
                    wlist.append(newalias)
                    written = True
                else:
                    wlist.append('# Added by Salt')
                    wlist.append(newalias)
                    written = True
            wlist.append(line)
    wsudoers = _write_sudoers(wlist)
    return wsudoers


def ls(*args):
    aliasRE = re.compile('(\w+)(?=\s*?\=)')
    defaults = []
    access = []
    ret = {'Host_Alias': {},
           'User_Alias': {},
           'Cmnd_Alias': {},
           }
    for line in _sudoers_list():
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
                members = [m.strip() for m in members]
                alias = aliasRE.search(line).group(1)
                if alias in val:
                    val[alias] += members
                    break
                else:
                    val[alias] = members
                    break
        else:
            access.append(line)
    ret = dict([(k, ret[k]) for k, v in ret.iteritems() if v])
    if defaults:
        ret['Defaults'] = defaults
    if access:
        ret['Access'] = access
    if args:
        ret = dict([(k, ret[k]) for k in args if k in ret])
        return ret
    else:
        return ret
