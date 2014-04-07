"""Restore System Python's ability to compile extensions,
which has been broken on OS X 10.9 with Xcode 5.1.

System Python has a compile flag `-mno-fused-madd`,
which is unrecognized by clang.
Xcode 5.1 updates clang to a version that promotes this warning to an error,
making it impossible to compile any extensions on System Python after installing Xcode 5.1.

This patches /System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/_sysconfigdata.py
to remove any instances of `-mno-fused-madd`.

Since it modifies system files, this is probably a horrible thing to do, and nobody should use it.
But here it is anyway, use at your own risk.
"""

# Copyright (C) 2013 Min RK
# Distributed under the terms of the 2-clause BSD License

import sys
import platform

from distutils.core import setup, Command
from distutils.command.install import install
from nonofusedmadd import __version__, patch

# actually run the patch at install time
class PatchSysConfig(Command):
    """Patch _sysconfigdata.py"""
    
    description = "Patch _sysconfigdata.py"
    
    user_options = []
    
    def initialize_options(self):
        pass
    
    def finalize_options(self):
        pass
    
    def run(self):
        patch()

class PatchThenInstall(install):
    def run(self):
        self.distribution.run_command("patch")
        install.run(self)

cmdclass = dict(
    patch=PatchSysConfig,
    install=PatchThenInstall,
)

name = "nonofusedmadd"

setup_args = dict(
    name = "nonofusedmadd",
    version = __version__,
    py_modules = [name],
    author = "Min Ragan-Kelley",
    author_email = "benjaminrk@gmail.com",
    url = 'http://github.com/minrk/%s' % name,
    download_url = 'http://github.com/minrk/%s/releases' % name,
    description = "Remove `-mno-fused-madd` from /System/.../_sysconfigdata.py",
    long_description = __doc__,
    license = "BSD",
    cmdclass = cmdclass,
    classifiers = [
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 2.7',
    ],
)

setup(**setup_args)

