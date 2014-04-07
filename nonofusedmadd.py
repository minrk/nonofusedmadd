"""
Patch stdlib _sysconfigdata.py to remove `-mno-fused-madd`,

which makes Python unable to compile anything.

Affects System Python on OS X 10.9 with Xcode 5.1
"""

# Copyright (C) 2013 Min RK
# Distributed under the terms of the 2-clause BSD License

__version__ = '0.0.1'

import shutil
import sys
import os
from os.path import (splitext, join as pjoin)
from subprocess import check_call, Popen, PIPE

import _sysconfigdata

sysconfig_base = splitext(_sysconfigdata.__file__)[0]
sysconfig_py = sysconfig_base + '.py'
sysconfig_pyc = sysconfig_base + '.pyc'
sysconfig_pyo = sysconfig_base + '.pyo'
sysconfig_backup = sysconfig_base + '_backup.py'

def backup():
    """backup _sysconfigdata.py"""
    if not os.path.exists(sysconfig_backup):
        print("backing up %s to %s" % (sysconfig_py, sysconfig_backup))
        shutil.copy2(sysconfig_py, sysconfig_backup)

def patch():
    """remove `-mno-fused-madd` from _sysconfigdata.py"""
    with open(sysconfig_py) as f:
        before = f.read()
    after = before.replace(' -mno-fused-madd', '')
    print("removing '-mno-fused-madd' from %s" % sysconfig_py)
    if after == before:
        print("nothing to patch")
        return
    backup()
    with open(sysconfig_py, 'w') as f:
        f.write(after)
    compile()
    diff()
    print("restore the original with `%s -m nonofusedmadd restore`" % sys.executable)

def diff():
    """show the diff"""
    if os.path.exists(sysconfig_backup):
        try:
            check_call(['git', '--version'], stdout=PIPE)
        except OSError:
            diff = ['diff']
        else:
            diff = ['git', 'diff', '--no-index', '--color-words', '-U0']
        cmd = diff + [sysconfig_backup, sysconfig_py]
        print(' '.join(cmd))
        p = Popen(cmd, stdout=PIPE)
        out, err = p.communicate()
        print(out.decode('utf8', 'replace'))
    else:
        print("nothing to diff")

def restore():
    """restore _sysconfigdata from backup and remove the backup"""
    if os.path.exists(sysconfig_backup):
        print("restoring %s from %s" % (sysconfig_py, sysconfig_backup))
        shutil.copy2(sysconfig_backup, sysconfig_py)
        compile()
        print("removing backup %s" % sysconfig_backup)
        os.unlink(sysconfig_backup)
    else:
        print("no backup to restore from")

def compile():
    """bytecompile _sysconfigdata.pyc, .pyo"""
    print("bytecompiling %s" % sysconfig_pyc)
    check_call([sys.executable, '-m', 'py_compile', sysconfig_py])
    print("bytecompiling %s" % sysconfig_pyo)
    check_call([sys.executable, '-O', '-m', 'py_compile', sysconfig_py])

if __name__ == '__main__':
    cmd = patch
    if len(sys.argv) > 1:
        cmd = globals()[sys.argv[1]]
    cmd()

