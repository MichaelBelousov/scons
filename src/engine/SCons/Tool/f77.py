"""engine.SCons.Tool.f77

Tool-specific initialization for the generic Posix f77 Fortran compiler.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""

#
# __COPYRIGHT__
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__revision__ = "__FILE__ __REVISION__ __DATE__ __DEVELOPER__"

import SCons.Defaults
import SCons.Scanner.Fortran
import SCons.Tool
import SCons.Util
import fortran

compilers = ['f77']

#
F77Action = SCons.Action.Action("$F77COM")
ShF77Action = SCons.Action.Action("$SHF77COM")
F77PPAction = SCons.Action.Action("$F77PPCOM")
ShF77PPAction = SCons.Action.Action("$SHF77PPCOM")

#
F77Suffixes = ['.f77']
F77PPSuffixes = []
if SCons.Util.case_sensitive_suffixes('.f77', '.F77'):
    F77PPSuffixes.append('.F77')
else:
    F77Suffixes.append('.F77')

#
F77Scan = SCons.Scanner.Fortran.FortranScan("F77PATH")

for suffix in F77Suffixes + F77PPSuffixes:
    SCons.Defaults.ObjSourceScan.add_scanner(suffix, F77Scan)

#
F77Generator = fortran.VariableListGenerator('F77', 'FORTRAN', '_FORTRAND')
F77FlagsGenerator = fortran.VariableListGenerator('F77FLAGS', 'FORTRANFLAGS')
ShF77Generator = fortran.VariableListGenerator('SHF77', 'SHFORTRAN', 'F77', 'FORTRAN', '_FORTRAND')
ShF77FlagsGenerator = fortran.VariableListGenerator('SHF77FLAGS', 'SHFORTRANFLAGS')

def add_to_env(env):
    """Add Builders and construction variables for f77 to an Environment."""
    env.AppendUnique(FORTRANSUFFIXES = F77Suffixes + F77PPSuffixes)

    static_obj, shared_obj = SCons.Tool.createObjBuilders(env)

    for suffix in F77Suffixes:
        static_obj.add_action(suffix, F77Action)
        shared_obj.add_action(suffix, ShF77Action)
        static_obj.add_emitter(suffix, SCons.Defaults.StaticObjectEmitter)
        shared_obj.add_emitter(suffix, SCons.Defaults.SharedObjectEmitter)

    for suffix in F77PPSuffixes:
        static_obj.add_action(suffix, F77PPAction)
        shared_obj.add_action(suffix, ShF77PPAction)
        static_obj.add_emitter(suffix, SCons.Defaults.StaticObjectEmitter)
        shared_obj.add_emitter(suffix, SCons.Defaults.SharedObjectEmitter)

    env['_F77G']      = F77Generator
    env['_F77FLAGSG'] = F77FlagsGenerator
    env['F77COM']     = '$_F77G $_F77FLAGSG $_F77INCFLAGS -c -o $TARGET $SOURCES'
    env['F77PPCOM']   = '$_F77G $_F77FLAGSG $CPPFLAGS $_CPPDEFFLAGS $_F77INCFLAGS -c -o $TARGET $SOURCES'

    env['_SHF77G']      = ShF77Generator
    env['_SHF77FLAGSG'] = ShF77FlagsGenerator
    env['SHF77COM']   = '$_SHF77G $_SHF77FLAGSG $_F77INCFLAGS -c -o $TARGET $SOURCES'
    env['SHF77PPCOM'] = '$_SHF77G $_SHF77FLAGSG $CPPFLAGS $_CPPDEFFLAGS $_F77INCFLAGS -c -o $TARGET $SOURCES'

    env['_F77INCFLAGS'] = '$( ${_concat(INCPREFIX, F77PATH, INCSUFFIX, __env__, RDirs)} $)'

def generate(env):
    fortran.add_to_env(env)

    import f90
    import f95
    f90.add_to_env(env)
    f95.add_to_env(env)

    add_to_env(env)

    env['_FORTRAND']        = env.Detect(compilers) or 'f77'

def exists(env):
    return env.Detect(compilers)
