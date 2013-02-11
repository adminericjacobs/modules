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


def _read_sudoers():
    #make sure file exists
    f = open('/home/ej321278/salt/_modules/sudoers', 'r')
    sudolist = [line for line in f.read().splitlines()]
    f.close()
    return sudolist


def append_user(alias_name, data):
    aliasRE = re.compile('(\w+)(?=\s*?\=)')
    wlist = []
    for line in _read_sudoers():
        if line.startswith('User_Alias'):
            alias = aliasRE.search(line).group(1)
            if alias_name == alias:
                line += ',' + data
                wlist.append(line)
            else:
                wlist.append(line)
        else:
            wlist.append(line)
    return wlist


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


def ls(*args):
    aliasRE = re.compile('(\w+)(?=\s*?\=)')
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
        msg = _flatten(ret)
        return msg
    else:
        msg = _flatten(ret)
        return msg
