#
# Copyright 2016 by Shaheed Haque (srhaque@theiet.org)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301  USA.
#
"""
SIP binding customisation for PyKF5.KCoreAddons. This modules describes:

    * The SIP file generator rules.
"""

import os, sys

import rules_engine
sys.path.append(os.path.dirname(os.path.dirname(rules_engine.__file__)))
import Qt5Ruleset

from clang.cindex import AccessSpecifier

def discard_base(container, sip, matcher):
    sip["base_specifiers"] = ""

def local_container_rules():
    return [
        [".*", "K_EXPORT_PLUGIN_is_deprecated_see_KDE5PORTING", ".*", ".*", ".*", rules_engine.container_discard],
        [".*", "KUserId", ".*", ".*", ".*", discard_base],
        [".*", "KGroupId", ".*", ".*", ".*", discard_base]
    ]

def qualify_kshell_enum(container, function, parameter, sip, matcher):
    sip["decl"] = "KShell::" + sip["decl"]

def local_parameter_rules():
    return [
        ["KShell", "splitArgs", ".*", "Options.*flags.*", ".*", qualify_kshell_enum],
    ]

def local_function_rules():
    return [
        #
        # Strip protected functions which require private stuff to work.
        #
        ["KPluginFactory", "KPluginFactory", ".*", ".*", ".*KPluginFactoryPrivate", rules_engine.function_discard],
        ["KJob", "KJob", ".*", ".*", "KJobPrivate.*", rules_engine.function_discard],
        ["KCompositeJob", "KCompositeJob", ".*", ".*", "KCompositeJobPrivate.*", rules_engine.function_discard],

        ["KUser", "KUser", ".*", ".*", ".*passwd.*", rules_engine.function_discard],
        ["KUserGroup", "KUserGroup", ".*", ".*", ".*group.*", rules_engine.function_discard],

        # Use forward declared types
        ["KPluginFactory", "createPartObject", ".*", ".*", ".*", rules_engine.function_discard],
        ["KPluginFactory", "create", ".*", ".*", ".*", rules_engine.function_discard],

        # Something is broken in our initializer detection
        ["KShell", "splitArgs", ".*", ".*", ".*", rules_engine.function_discard],

        ["KMacroExpanderBase", "expandMacrosShellQuote", ".*", ".*", ".*, int ", rules_engine.function_discard],

        # Multiple overloads with same python signature
        ["KRandomSequence", "setSeed", ".*", ".*", "int.*", rules_engine.function_discard],

        #
        # This class has inline implementations in the header file.
        #
        ["KPluginName", ".*", ".*", ".*", ".*", rules_engine.function_discard_impl],
        ["KCrash", "defaultCrashHandler", ".*", ".*", ".*", rules_engine.function_discard_impl],

        [".*", "qobject_cast", ".*", ".*", ".*", rules_engine.function_discard],
        [".*", "qobject_interface_iid", ".*", ".*", ".*", rules_engine.function_discard],
        ["KPluginLoader", "instantiatePlugins", ".*", ".*", ".*", rules_engine.function_discard],
        ["KPluginLoader", "findPlugins.*", ".*", ".*", ".*", rules_engine.function_discard],
        ["KPluginLoader", "forEachPlugin", ".*", ".*", ".*", rules_engine.function_discard],
        #
        # kuser.h has inline operators.
        #
        [".*", "operator!=", ".*", ".*", "const KUser(Group){0,1} &other", rules_engine.function_discard],
    ]

class RuleSet(Qt5Ruleset.RuleSet):
    """
    SIP file generator rules. This is a set of (short, non-public) functions
    and regular expression-based matching rules.
    """
    def __init__(self, includes):
        Qt5Ruleset.RuleSet.__init__(self, includes)
        self._param_db = rules_engine.ParameterRuleDb(lambda: local_parameter_rules() + Qt5Ruleset.parameter_rules())
        self._fn_db = rules_engine.FunctionRuleDb(lambda: local_function_rules() + Qt5Ruleset.function_rules())
        self._container_db = rules_engine.ContainerRuleDb(lambda: local_container_rules() + Qt5Ruleset.container_rules())
