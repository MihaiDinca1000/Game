import argparse
import sys
from . import netloop
from collections import OrderedDict
import logging
import platform
from . import session
import os
from .aspic import Aspic, BiAtex
from .blackbox import BlackBox
from .alto_component import AltoCliComponent
from .alto_component import AltoGuiComponent
from .dss_actor import CommunityMgr, LocalCtrl, Maestro, ExternApp, Tsar, Vmac, Realtime, Synoptic, Cats
from .configuration import Conf, PathMapperPath
from . import configuration
from .application import Application
from . import windows_shares
from .. import version
from . import versions
import subprocess
from .convert_xml import run_convertor
import platform as _platform


class AltoCli(object):

    def add_choices(self, parser):
        g = parser.add_mutually_exclusive_group(required=False)
        g.add_argument('-i', '--interactive', action='store_true', help='Choose options interactively in the terminal')
        g.add_argument(
            '-s',
            '--set',
            action='append',
            nargs="?",
            help='Set an option (syntax: OPTION_NAME=option_value). This argument may be repeated as much as needed')
        g.add_argument('-f', '--file', help='Set options as saved in the FILE')
        g.add_argument('-g', '--gui', action='store_true', help='Choose options interactively in a window')

    def __build_session_parser(self, newparsers):

        def add_cmd(root_parser, subcommand, help):
            parser = root_parser.add_parser(subcommand, help=help)
            parser.set_defaults(func=getattr(self, "session_" + subcommand))
            return parser

        p = add_cmd(newparsers, 'new', help='Create a new session')
        p.add_argument('-d', '--dir', type=str, help='Force the name of the directory of the session')

        p = add_cmd(newparsers, 'get', help='Get the path a session')

        p = add_cmd(newparsers, 'list', help='List the history of a session id')

        p = add_cmd(newparsers, 'setup', help='Set up alto directory structure')

    def __build_conf_parser(self, newparsers):

        def add_cmd(root_parser, subcommand, help):
            parser = root_parser.add_parser(subcommand, help=help)
            parser.set_defaults(func=getattr(self, "conf_" + subcommand))
            return parser

        p = add_cmd(newparsers, 'load', help="Load a configuration file")
        p.add_argument('filename', type=str, help='The configuration file name')
        p.add_argument('platforms', type=str, help='The platforms file name')
        p.add_argument('-n', '--new', action='store_true', help='Create a new session at the same time')
        self.add_choices(p)

        p = add_cmd(newparsers, 'show', help='Show the configuration')
        p.add_argument('-r', '--resolved', action='store_true', default=False, help='Resolve {{tags}} to their values')

    def __build_options_parser(self, newparsers):

        def add_cmd(root_parser, subcommand, help):
            parser = root_parser.add_parser(subcommand, help=help)
            parser.set_defaults(func=getattr(self, "options_" + subcommand))
            return parser

        p = add_cmd(newparsers, 'choose', help="Choose options values")
        self.add_choices(p)

        p = add_cmd(newparsers, 'show', help='Show options values')

        p = add_cmd(newparsers, 'save', help='Save options values to a file')
        p.add_argument('filename', help='Save option choices to a file')

        p = add_cmd(newparsers, 'change', help="Change options at run time")
        self.add_choices(p)

    def __build_srv_parser(self, newparsers):

        def add_cmd(root_parser, subcommand, help):
            parser = root_parser.add_parser(subcommand, help=help)
            parser.set_defaults(func=getattr(self, "srv_" + subcommand))
            return parser

        p = add_cmd(newparsers, 'ping', help='Ping a Bow server')
        p.add_argument('hostname', help='One or several (comma separated) host names or IP address')

        p = add_cmd(newparsers, 'run', help='Run a command in foreground on a Bow server')
        p.add_argument('hostname', help='One or several (comma separated) host names or IP address')
        p.add_argument('cmd', help='Command to execute')

        p = add_cmd(newparsers, 'runbg', help='Run a command in background on a Bow server')
        p.add_argument('hostname', help='One or several (comma separated) host names or IP address')
        p.add_argument('cmd', help='Command to execute')

        p = add_cmd(newparsers, 'cp', help='Copy a file to a remote server via a remote Bow server')
        p.add_argument('hostname', help='One or several (comma separated) host names or IP address')
        p.add_argument('fr', help='The file to cpy')
        p.add_argument('to', help='The remote path')

        p = add_cmd(newparsers, 'kill', help='Kill commands launched on a Bow server')
        p.add_argument('--hostname', help='One or several (comma separated) host names or IP address')

    def __build_drive_parser(self, newparsers):

        def add_cmd(root_parser, subcommand, help):
            parser = root_parser.add_parser(subcommand, help=help)
            parser.set_defaults(func=getattr(self, "drive_" + subcommand))
            return parser

        p = add_cmd(newparsers, 'list', help='List mapped network share')

        p = add_cmd(newparsers, 'map', help='Map a network share to a drive')
        p.add_argument('-d', '--drive', help='The drive letter to be mapped')
        p.add_argument('-u', '--unmap', action='store_true', help='Unmap (cf. unmap subcommand)')
        p.add_argument('share', help='The network share')

        p = add_cmd(newparsers, 'batchmap', help='Map a set of new shares to a set of drives')
        p.add_argument('share', nargs="+", help='The network shares')

        p = add_cmd(newparsers, 'batchunmap', help='Unmap a set of drives')
        p.add_argument('share', nargs="+", help='The network shares')

        p = add_cmd(newparsers, 'unmap', help='Unmap a drive')
        p.add_argument('drive', help='The drive letter')

    def __build_appli_parser(self, newparsers):

        def add_cmd(root_parser, subcommand, help):
            parser = root_parser.add_parser(subcommand, help=help)
            parser.set_defaults(func=getattr(self, "appli_" + subcommand))
            return parser

        p = add_cmd(newparsers, 'start', help='Start an application')
        p.add_argument('-c', '--configuration', type=str, help='Load a configuration file')
        self.add_choices(p)
        p.add_argument('-d', '--dryrun', action='store_true', help='Do not really launch the application')
        p.add_argument('-n', '--new', action='store_true', help='Create a new session')
        p.add_argument('-p', '--platforms', action='store',
                       help='Perform the remote command on all the machines of the platform')
        p.add_argument('component', nargs="*", default=[], help='If specified, only those components will be launched')

        p = add_cmd(newparsers, 'stop', help='Stop an application')
        p.add_argument('-d', '--dryrun', action='store_true', help='Do not really launch the application')
        p.add_argument('component', nargs="*", default=[], help='If specified, only those components will be stopped')

        p = add_cmd(newparsers, 'reset', help='Reset Platform')
        self.add_choices(p)

    def __build_local_command_parser(self, newparsers):

        def add_cmd(root_parser, subcommand, help):
            parser = root_parser.add_parser(subcommand, help=help)
            parser.set_defaults(func=getattr(self, "local_" + subcommand))
            return parser

        p = add_cmd(newparsers, 'launch', help='Launch a component on localhost')
        p.add_argument("config_file", help="Path to the local configuration file")
        p.add_argument("component_name", help="The name of the component to launch")
        p.add_argument("--display", help="Set the DISPLAY environment variable")

        p = add_cmd(newparsers, 'stop', help='Stop a component on localhost')
        p.add_argument("config_file", help="Path to local configuration file")
        p.add_argument("component_name", help="Name of component to stop")

        p = add_cmd(newparsers, 'reset', help='Reset host')
        p.add_argument("host_name", help="Name of the host to reset")
        p.add_argument("linux_script", help="Path to linux user reset script")
        p.add_argument("windows_script", help="Path to windows user reset script")

        p = add_cmd(newparsers, 'diagnostic',
                    help='Perform a diagnostic on a component running on localhost [NOT IMPLEMENTED]')
        p.add_argument("config_file", help="Path to the configuration file [NOT IMPLEMENTED]")
        p.add_argument("component_name", help="Name of the component to diagnose [NOT IMPLEMENTED]")


    def __init__(self, sysargs):

        os.umask(0)

        if len(sysargs) > 0 and sysargs[0] == 'test':
            import pytest
            sys.exit(pytest.main(sysargs[1:]))

        def add_cmd(root_parser, subcommand, help):
            parser = root_parser.add_parser(subcommand, help=help)
            parser.set_defaults(func=getattr(self, subcommand))
            return parser

        parser = argparse.ArgumentParser(description='Application Launcher TOol')
        parser.add_argument('--sid', help='The session ID')
        parser.add_argument('--pref', help='Alto Launcher preferences file')
        parser.add_argument('--noshared', action='store_true',
                            help='Do not look up for the network share Alto-Launcher is running on')
        parser.add_argument('-v', '--version', action='version', version=version.get_version())
        parser.add_argument('-l', '--local', action='store_true', help='Launch ALTO in local mode')
        subparsers = parser.add_subparsers(help='Subcommands')

        p = subparsers.add_parser("drive", help='Manage network shares and its mappings')
        self.__build_drive_parser(p.add_subparsers())

        p = subparsers.add_parser("local_command", help='Operate a component on localhost')
        self.__build_local_command_parser(p.add_subparsers())

        p = subparsers.add_parser("options", help='Manage options specified in the configuration')
        self.__build_options_parser(p.add_subparsers())

        p = add_cmd(subparsers, 'ping', help='Ping a remote host')
        p.add_argument('hostname', help='One or several (comma separated) host names or IP address')

        p = add_cmd(subparsers, 'remote', help='Perform an Alto command on a remote host')
        g = p.add_mutually_exclusive_group(required=False)
        g.add_argument('-m', '--host', action='append',
                       help='One or several (comma separated) host names or IP address')
        g.add_argument('-p', '--platform', action='store_true',
                       help='Perform the remote command on all the machines of the platform')
        g.add_argument('-w', '--windows', action='store_true',
                       help='Perform the remote command on all Windows machines of the platform')
        p.add_argument("command", nargs=argparse.REMAINDER, help='The Alto-Launcher command to be executed')

        p = add_cmd(subparsers, 'resolve', help='Resolve a network name to IP address')
        p.add_argument('hostname', help='One or several (comma separated) host names or IP address')

        p = subparsers.add_parser("session", help='Manage sessions')
        self.__build_session_parser(p.add_subparsers())

        p = subparsers.add_parser("srv", help='Perform actions on a remote Bow server')
        self.__build_srv_parser(p.add_subparsers())

        p = add_cmd(subparsers, 'test', help='Run the automatic test suite')
        p.add_argument('args', nargs=argparse.REMAINDER, help="Arguments passed to PyTest framework")

        # no need for platform file if local mode
        if '--local' in sysargs:
            if platform.system() == "Windows":
                suffix = "_WIN"
            else:
                suffix = "_LINUX"
            if hasattr(sys, "frozen"):
                platforms_file = os.path.join(
                    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(sys.executable)))),
                    'local_mode', 'LOCAL_PLATFORM' + suffix + '.xml')
            else:
                platforms_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'local_mode',
                                              'LOCAL_PLATFORM' + suffix + '.xml')
            if platforms_file not in sysargs:
                if len(set(['appli', 'start']).intersection(set(sysargs))) == 2:
                    sysargs.append('-p')
                    sysargs.append(platforms_file)
                if len(set(['conf', 'load']).intersection(set(sysargs))) == 2:
                    sysargs.append(platforms_file)

        p = subparsers.add_parser("conf", help='Manage Alto configuration')
        self.__build_conf_parser(p.add_subparsers())

        p = subparsers.add_parser("appli", help='Launch/Stop a simulation application')
        self.__build_appli_parser(p.add_subparsers())

        p = add_cmd(subparsers, 'convert', help='Convert the ALTO configuration file')
        p.add_argument('versions', type=str, nargs='+', help='The ALTO version of the file to convert')
        p.add_argument('filename', type=str, help='The configuration file')

        p = add_cmd(subparsers, 'version', help='Get a version information from ALTO configuration file')
        p.add_argument('conf_file', type=str, help='The configuration file')
        p.add_argument('version_type', type=str, help='The name of the component version to retreive (to access a tool, write tools and add --tool_name option)')
        p.add_argument('--pathmapper', type=str, help='The name of the pathmapper to use to compute path for this version')
        p.add_argument("--group", help="The name of the specific_versions of the component to retreive")
        p.add_argument('--platform', type=str, help='The name of the pathmapper to use to compute path for this version')
        p.add_argument('--tool_name', type=str, help='The name of the tool you want info on')
        info_to_get = p.add_mutually_exclusive_group()
        info_to_get.add_argument("--version", action='store_true', help="The output will be the the version number")
        info_to_get.add_argument("--path", action='store_true', help="The output will be the the version path on the actual machine")
        info_to_get.add_argument("--path_linux", action='store_true', help="The output will be the the version linux path")
        info_to_get.add_argument("--path_windows", action='store_true', help="The output will be the the version windows path")


        args = parser.parse_args(sysargs)

        if hasattr(args, 'filename') and args.filename is not None:
            args.filename = args.filename if os.path.isabs(args.filename) else os.path.join(os.getcwd(), args.filename)
        if hasattr(args, 'platforms') and args.platforms is not None:
            args.platforms = args.platforms if os.path.isabs(
                args.platforms) else os.path.join(os.getcwd(), args.platforms)
        if hasattr(args, 'pref') and args.pref is not None:
            args.pref = args.pref if os.path.isabs(args.pref) else os.path.join(os.getcwd(), args.pref)

        if 'func' not in args:
            parser.print_help()
            sys.exit(0)
        if args.func != self.session_list and args.func != self.session_setup and args.func != self.convert and args.func != self.version:
            if "ALTO_SESSION_ID" in os.environ and args.sid is None:
                args.sid = os.environ["ALTO_SESSION_ID"]
            if args.sid is None:
                print("Error: you must specify a session id (by argument or ALTO_SESSION_ID env var)")
                sys.exit(255)
        if args.func == self.appli_reset:
            try:
                self.session = session.Session.get(args.sid)
                # self.session.activate()
                Conf()
                Conf().pickle_load(self.session.path_pickle_configuration)
            except:
                logging.info("Error: " + args.sid + " is an inexistant session name")
                print("Error: " + args.sid + " is an inexistant session name")
                sys.exit(255)
        if (args.func == self.conf_load or args.func == self.appli_start) and args.new is True:
            self.session = session.Session.new(args.sid)
            self.session.activate()
            Conf()
            if args.noshared:
                Conf().shared_folders_full_check = False
            if hasattr(args, 'local'):
                Conf().local = args.local
        elif not args.func.__name__.startswith("session_") and args.func != self.convert and args.func != self.version:
            self.session = session.Session.get(args.sid)

            if self.session is None:
                logging.info("Error: " + args.sid + " is an inexistant session name")
                print("Error: " + args.sid + " is an inexistant session name")
                sys.exit(255)

            self.session.activate()
            Conf()
            if args.noshared:
                Conf().shared_folders_full_check = False
            if os.path.exists(self.session.path_pickle_configuration):
                Conf().pickle_load(self.session.path_pickle_configuration)
            if hasattr(args, 'local'):
                Conf().local = args.local

        ret = args.func(args)

        if ret is None:
            ret = 0

        sys.exit(ret)

    def __make_host_list(self, host_list_string):
        return host_list_string.split(",")

    def version(self, args):
        if not os.path.exists(args.conf_file):
            print("Error: conf file "+str(args.conf_file)+" not found")
        if args.platform is not None and not os.path.exists(args.platform):
            print("Error: conf file "+str(args.conf_file)+" not found")
        version_type = args.version_type
        if args.version_type == "tools":
            if args.tool_name is None:
                print("Error: tool_name not defined")
                sys.exit(1)
            else:
                version_type = args.tool_name


        if args.path:
            if platform.system() == "Linux":
                os_type = "Linux"
            else:
                os_type = "Windows"
        elif args.path_linux:
            os_type = "Linux"
        elif args.path_windows:
            os_type = "Windows"
        else:
            version_number = None
            Conf().load_xml_retreive_info(args.conf_file, None, None, "version_num")
            if args.group is not None:
                if args.group in Conf().parser.data.versions:
                    version_number = Conf().parser.data.versions[args.group][version_type].version
                    if version_number is None:
                        version_number = Conf().parser.data.versions["default"][version_type].version
                else:
                    print("Error: " + args.group + " not found")
                    sys.exit(1)
            else:
                version_number = Conf().parser.data.versions["default"][version_type].version
            if version_number is not None:
                print(version_number)
            else:
                print("None")
            return

        if args.pathmapper is None:
            print("Error: no pathmapper specified to retreive a path")
            sys.exit(1)
        if args.platform is None:
            print("Error: no platform specified to retreive a path")
            sys.exit(1)
        Conf().load_xml_retreive_info(args.conf_file, args.platform, args.pathmapper, "version_path")

        version = None
        if args.group is not None:
            if args.group in Conf().parser.data.versions:
                if os_type == "Windows":
                    version = Conf().parser.data.versions[args.group][version_type].path_windows
                else:
                    version = Conf().parser.data.versions[args.group][version_type].path_linux
            else:
                print("Error: " + args.group + " not found")
                sys.exit(1)
        else:
            if os_type == "Windows":
                version = Conf().parser.data.versions["default"][version_type].path_windows
            else:
                version = Conf().parser.data.versions["default"][version_type].path_linux
        if version is not None:
            version = Conf().parser.compute_value_for_path(version, os_type, None, None)
            if "{{property[" in version:
                print("Error: a property wasn't resolved in <"+version+">, this may be because this property is defined in the platform file")
                sys.exit(1)
            print(version)
        else:
            print("None")

    def test(self, args):
        raise Exception("This cannot happen")

    def ping(self, args):
        hosts = self.__make_host_list(args.hostname)
        resolved_named = netloop.loop().resolve(hosts)
        dict_hostname_ip = OrderedDict(resolved_named)
        ips = [ip for (h, ip) in resolved_named if ip is not None]
        dict_ip_ping = OrderedDict(netloop.loop().ping(ips))
        for (h, ip) in dict_hostname_ip.items():
            if ip is None:
                print(h + ": Unresolved")
            else:
                if h == ip:
                    print(ip + ": " + str(dict_ip_ping[ip]))
                else:
                    print(h + ": " + ip + ": " + str(dict_ip_ping[ip]))

    def resolve(self, args):
        hosts = self.__make_host_list(args.hostname)
        res = netloop.loop().resolve(hosts)
        for (name, ip) in res:
            print(name + ": " + str(ip))

    def remote(self, args):

        if args.platform is True:
            hosts = [h.name for h in Conf().data.current_plf.generichosts.values() if h.enabled_resolved]
        elif args.windows is True:
            hosts = [h.name for h in Conf().data.current_plf.generichosts.values() if h.type ==
                     configuration.HostType.Windows and h.enabled_resolved]
        else:
            hosts = args.host

        cmd = args.command
        res = netloop.loop().remote(hosts, cmd)
        for host, result in res:
            if result['stdout'] is not None:
                for l in str(result['stdout']).splitlines():
                    print(host + ":stdout:" + str(l))
            if result['stderr'] is not None:
                for l in str(result['stderr']).splitlines():
                    print(host + ":stderr:" + str(l))
            print(host + ": return code = " + str(result['returncode']))

    def session_new(self, args):
        s = session.Session.new(args.sid, args.dir)
        s.activate()
        print("New session created. Path: " + s.path_session)
        return 0

    def session_list(self, args):
        for id in session.Session.list():
            print(id)

    def session_get(self, args):
        s = session.Session.get(args.sid)
        if s is None:
            sys.exit(1)
        print("Path: " + s.path_session)

    def session_setup(self, args):
        session.Session.setup_alto()

    def options_choose(self, args):

        if args.interactive:
            res = Conf().do_choices('console')
        elif args.gui:
            res = Conf().do_choices('gui')
        else:
            argument = None
            if args.set is not None:
                argument = [a for a in args.set if a is not None]
            elif args.file:
                argument = os.path.join(self.session.path_startup, args.file)
            res = Conf().do_choices('non_interactive', argument)

        if res == 2:
            print("Options choice aborted by user.")
            sys.exit(2)
        elif res != 0:
            print("Error during options choice. Not saving.")
            sys.exit(1)

    def finish_options_choose(self):
        Application().compute_groups()
        Application().compute_hosts_names()
        if not Conf().local:
            Application().testing_bow_server()
        if Conf().data.login is not None and Conf().data.user_script is not None:
            ret = Application().testing_user_script()
            if ret != 0:
                sys.exit(ret)
        Conf().pickle_dump(self.session.path_pickle_configuration)

    def options_show(self, args):
        print("Options logic => " + str(Conf().data.logic))
        for obj in Conf().data.options.values():
            obj.print()

    def options_change(self, args):

        Conf().backup_options()

        if args.interactive:
            res = Conf().do_choices('console', at_runtime=True)
        elif args.gui:
            res = Conf().do_choices('gui', at_runtime=True)
        else:
            argument = None
            if args.set:
                argument = args.set
            elif args.file:
                argument = os.path.join(self.session.path_startup, args.file)
            res = Conf().do_choices('non_interactive', argument, at_runtime=True)

        if res == 1:
            print("Error during options choice. Not saving.")
            sys.exit(1)
        elif res == 2:
            print("Choice aborted by user.")
            sys.exit(2)

        optchanged = Conf().changes_since_backup()

        compo = set()
        for o in optchanged:
            compo |= o.used_by_components
        compo_to_stop = []
        for c in compo:
            if Conf().data.components[c].launched:
                compo_to_stop.append(c)
        compo_to_restart = []
        for c in compo_to_stop:
            if Conf().data.components[c].enabled:
                compo_to_restart.append(c)

        print("Changed options: " + str(optchanged))
        print("Components: " + str(compo))
        print("Components to stop: " + str(compo_to_stop))
        print("Components to restart: " + str(compo_to_restart))

        # we need to save which components were launched before reading resolved.xml
        # because we will lose the information (launched is not in resolved.xml)
        launched_names = set()
        for c in Conf().data.components.values():
            if c.launched:
                launched_names.add(c.name)

        s = os.path.join(Conf().data.path_session, "resolved.xml")
        Conf().load_resolved_xml(s, True)
        Conf().load_alto_path()
        self.finish_options_choose()

        # reapply the launched information
        for name in launched_names:
            Conf().data.components[name].launched = True
            Conf().data.components[name].state = "Launched"

        if len(compo_to_stop) > 0:
            ret = Application().stop(compo_to_stop)
            if ret != 0:
                print("Error stopping components!")
                sys.exit(ret)

            Conf().pickle_dump(self.session.path_pickle_configuration)

        if len(compo_to_restart) > 0:
            ret = Application().start(compo_to_restart)
            if ret != 0:
                print("Error starting components!")
                sys.exit(ret)

        Conf().pickle_dump(self.session.path_pickle_configuration)

    def options_save(self, args):
        Conf().save_choices(os.path.join(self.session.path_startup, args.filename))

    def conf_load(self, args):
        Conf().local = args.local
        Conf().load_xml(args.filename, args.platforms, args.pref,
                        self.session.current_session.id, self.session.current_session.path_session)

        if args.interactive or args.gui or args.set is not None or args.file:
            self.options_choose(args)
        else:
            ret = Conf().parser.make_choices("")
            if ret:
                sys.exit(1)
        Conf().finish_load_xml()
        Conf().load_alto_path()

        self.finish_options_choose()

        # add session path to pathmappers
        if sys.platform != "win32":
            session_path_linux = self.session.current_session.path_session
            session_path_windows = "C:\\Temp\\alto\\" + self.session.current_session.id + "\\" +\
                os.path.basename(self.session.current_session.path_session)
        else:
            session_path_windows = self.session.current_session.path_session
            session_path_linux = "/local/home1/alto/" + self.session.current_session.id + "/" +\
                os.path.basename(self.session.current_session.path_session)
        Conf().data.current_pm.path['alto_session'] = PathMapperPath('alto_session',
                                                                     linux=session_path_linux,
                                                                     windows=session_path_windows,
                                                                     drive=None)

    def conf_show(self, args):
        if args.resolved is True:
            Conf().pretty_print_resolved()
        else:
            Conf().pretty_print()

    def convert(self, args):
        run_convertor()

    def srv_ping(self, args):
        hosts = self.__make_host_list(args.hostname)
        resolved_named = netloop.loop().resolve(hosts)
        dict_hostname_ip = OrderedDict(resolved_named)
        ips = [ip for (h, ip) in resolved_named if ip is not None]
        dict_ip_ping = OrderedDict(netloop.loop().srv_ping(ips))
        for (h, ip) in dict_hostname_ip.items():
            if ip is None:
                print(h + ": Unresolved")
            else:
                if h == ip:
                    print(ip + ": " + str(dict_ip_ping[ip]))
                else:
                    print(h + ": " + ip + ": " + str(dict_ip_ping[ip]))

    def srv_run(self, args):
        hosts = self.__make_host_list(args.hostname)
        cmd = args.cmd
        res = netloop.loop().srv_run(hosts, cmd)
        for (name, output) in res:
            print(name + ": " + str(output))

    def srv_runbg(self, args):
        hosts = self.__make_host_list(args.hostname)
        cmd = args.cmd
        res = netloop.loop().srv_runbg(hosts, cmd)
        for (name, output) in res:
            print(name + ": " + str(output))

    def srv_cp(self, args):
        import xmlrpc.client
        hosts = self.__make_host_list(args.hostname)
        path = args.fr if os.path.isabs(args.fr) else os.path.join(self.session.path_startup, args.fr)
        content = xmlrpc.client.Binary(open(path, "rb").read())
        res = netloop.loop().srv_put(hosts, args.to, content)
        for (name, output) in res:
            if output == 0:
                output_str = "copy succeeded"
            else:
                output_str = "copy failed (error code: " + output + ")"
            print(name + ": " + output_str)

    def srv_kill(self, args):
        hosts = self.__make_host_list(args.hostname) if args.hostname is not None else [
            h.name for h in Conf().data.current_plf.generichosts.values() and h.enabled_resolved]
        res = netloop.loop().srv_kill(hosts)
        for (name, output) in res:
            for o in str(output).splitlines():
                print(name + ": " + o)

    def appli_start(self, args):
        if args.configuration:
            args.filename = args.configuration
            if not (args.interactive or args.gui or args.set or args.file):
                args.set = []
            self.conf_load(args)
        else:
            Conf().load_alto_path()
            # check if configuration file or platform files have been modified since resolved.xml was generated
            if not os.path.isfile(Conf().data.filename):
                print("Error: file " + Conf().data.filename + " not found!")
                return 1
            currentTimestamp = os.path.getmtime(Conf().data.path_conf_file)
            currentSize = os.path.getsize(Conf().data.path_conf_file)
            if Conf().data.file_timestamp < currentTimestamp or Conf().data.file_size != currentSize:
                currentMd5Sum = Conf().get_check_sum(Conf().data.filename)
                if Conf().data.file_md5_sum != currentMd5Sum:
                    print("resolved older than conf")
                    sys.exit(2)
        ret = Application().start(args.component, args.dryrun, local=args.local)
        Conf().pickle_dump(self.session.path_pickle_configuration)
        sys.exit(ret)

    def appli_stop(self, args):
        ret = Application().stop(args.component, args.dryrun, local=args.local)
        Conf().pickle_dump(self.session.path_pickle_configuration)
        sys.exit(ret)

    def appli_reset(self, args):
        for component in Conf().data.components:
            compo = Conf().data.components[component]
            if isinstance(compo, configuration.AltoCli):
                altoComp = AltoCliComponent(compo.name)
                altoComp.set_config(compo, self.session.path_session)
                altoComp.reset()

            if isinstance(compo, configuration.AltoGui):
                altoComp = AltoGuiComponent(compo.name)
                altoComp.set_config(compo, self.session.path_session)
                altoComp.reset()

        Conf().pickle_load(self.session.path_pickle_configuration)
        ret = Application().reset(local=args.local)
        Conf().pickle_dump(self.session.path_pickle_configuration)
        sys.exit(ret)

    def drive_list(self, args):
        for s in windows_shares.list_shares():
            print(s.drive + " " + s.share)
        sys.exit(0)

    def drive_map(self, args):
        print("Mapped to drive " + windows_shares.map_share(args.share, args.drive, args.unmap))
        sys.exit(0)

    def drive_batchmap(self, args):
        param = [val.split(":") for val in args.share]
        for drive, share in param:
            windows_shares.map_share(share, drive + ":", True)
        print("Mappings done")
        sys.exit(0)

    def drive_unmap(self, args):
        windows_shares.unmap_share(args.drive)
        sys.exit(0)

    def drive_batchunmap(self, args):
        for drive in args.share:
            windows_shares.unmap_share(drive)
        print("Mappings removed")
        sys.exit(0)

    def local_launch(self, args):
        logging.info("read configuration from " + args.config_file)
        if os.path.isabs(args.config_file):
            config_file = args.config_file
        else:
            config_file = os.path.join(self.session.path_startup, args.config_file)
        config_dir = os.path.dirname(config_file)
        Conf().load_resolved_xml(config_file)
        if len(Conf().optlist) != 0:
            print("Error: The following variables should not have been set: " + str(list(Conf().optlist.keys())))
            sys.exit(1)
        if args.component_name in Conf().data.components:
            logging.info(args.component_name + " found in configuration")
        else:
            print("Error: " + args.component_name + " not found in configuration")
            sys.exit(1)
        compo = Conf().data.components[args.component_name]

        runon_display = ''
        for runon in Conf().data.distribution:
            if args.component_name == runon.component:
                if runon.display is not None:
                    runon_display = runon.display
                    # runon_display = Conf().data.platform.pc_genericname[runon.display].realname

        if isinstance(compo, configuration.Aspic):
            if platform.system() != "Linux":
                logging.info("Error: aspic not available on windows")
                print("Error: aspic not available on windows")
                sys.exit(1)
            asp = Aspic(compo.name)
            asp.set_config(compo, config_dir)
            if args.display:
                asp.launch(args.display)
            else:
                asp.launch(runon_display=runon_display)
        elif isinstance(compo, configuration.BiAtex):
            if platform.system() != "Linux":
                logging.info("Error: BiAtex not available on windows")
                print("Error: BiAtex not available on windows")
                sys.exit(1)
            bia = BiAtex(compo.name)
            bia.set_config(compo, config_dir)
            if args.display:
                bia.launch(args.display)
            else:
                bia.launch(runon_display=runon_display)
        elif isinstance(compo, configuration.BlackBox):
            bb = BlackBox(compo.name)
            bb.set_config(compo, config_dir)
            if args.display:
                bb.launch(args.display)
            else:
                bb.launch(runon_display=runon_display)
            logging.info("End of blackbox launch")
        elif isinstance(compo, configuration.AltoCli):
            altoComp = AltoCliComponent(compo.name)
            altoComp.set_config(compo, config_dir)
            if args.display:
                altoComp.launch(args.display)
            else:
                altoComp.launch(runon_display=runon_display)
            logging.info("End of alto cli component launch")
        elif isinstance(compo, configuration.AltoGui):
            altoComp = AltoGuiComponent(compo.name)
            altoComp.set_config(compo, config_dir)
            if args.display:
                altoComp.launch(args.display)
            else:
                altoComp.launch(runon_display=runon_display)
            logging.info("End of alto gui component launch")
        elif isinstance(compo, configuration.DssCommunityManager):
            cm = CommunityMgr(compo.name, compo.community)
            cm.set_config(compo, config_dir)
            cm.launch(compo.community.host, compo.community.port)
        elif isinstance(compo, configuration.DssLocalController):
            lc = LocalCtrl(compo.name, compo.community)
            lc.set_config(compo, config_dir)
            lc.launch(compo.community.host, compo.community.port)
        elif isinstance(compo, configuration.DssExternApp):
            ea = ExternApp(compo.name, compo.community)
            ea.set_config(compo, config_dir)
            ea.launch(compo.community.host, compo.community.port, runon_display=runon_display)
        elif isinstance(compo, configuration.DssMaestro):
            moni = Maestro(compo.name, compo.community)
            moni.set_config(compo, config_dir)
            moni.launch(compo.community.host, compo.community.port, runon_display=runon_display)
        elif isinstance(compo, configuration.DssTsar):
            moni = Tsar(compo.name, compo.community)
            moni.set_config(compo, config_dir)
            moni.launch(compo.community.host, compo.community.port)
        elif isinstance(compo, configuration.DssVmac):
            moni = Vmac(compo.name, compo.community)
            moni.set_config(compo, config_dir)
            moni.launch(compo.community.host, compo.community.port)
        elif isinstance(compo, configuration.DssRealtime):
            moni = Realtime(compo.name, compo.community)
            moni.set_config(compo, config_dir)
            moni.launch(compo.community.host, compo.community.port)
        elif isinstance(compo, configuration.DssSynoptic):
            syn = Synoptic(compo.name, compo.community)
            syn.set_config(compo, config_dir)
            syn.launch(compo.community.host, compo.community.port)
        elif isinstance(compo, configuration.DssCats):
            cats = Cats(compo.name, compo.community)
            cats.set_config(compo, config_dir)
            cats.launch(compo.community.host, compo.community.port)
        else:
            raise Exception("Composant " + compo.name + ": type inconnu: " + str(type(compo)))

    def local_stop(self, args):
        logging.info("read configuration from " + args.config_file)
        if os.path.isabs(args.config_file):
            config_file = args.config_file
        else:
            config_file = os.path.join(self.session.path_startup, args.config_file)
        config_dir = os.path.dirname(config_file)
        Conf().load_resolved_xml(config_file)
        if len(Conf().optlist) != 0:
            print("Error: The following variables should not have been set: " + str(list(Conf().optlist.keys())))
            sys.exit(1)
        if args.component_name in Conf().data.components:
            logging.info(args.component_name + " found in configuration")
        else:
            print("Error: " + args.component_name + " not found in configuration")
            sys.exit(1)
        compo = Conf().data.components[args.component_name]
        if isinstance(compo, configuration.Aspic):
            if platform.system() != "Linux":
                logging.info("Error: aspic not available on windows")
                print("Error: aspic not available on windows")
                sys.exit(1)
            asp = Aspic(compo.name)
            asp.set_config(compo, config_dir)
            asp.stop()
        elif isinstance(compo, configuration.BiAtex):
            if platform.system() != "Linux":
                logging.info("Error: biatex not available on windows")
                print("Error: biatex not available on windows")
                sys.exit(1)
            bia = BiAtex(compo.name)
            bia.set_config(compo, config_dir)
            bia.stop()
        elif isinstance(compo, configuration.BlackBox):
            bb = BlackBox(compo.name)
            bb.set_config(compo, config_dir)
            bb.stop()
        elif isinstance(compo, configuration.AltoCli):
            alto = AltoCliComponent(compo.name)
            alto.set_config(compo, config_dir)
            alto.stop()
        elif isinstance(compo, configuration.AltoGui):
            alto = AltoGuiComponent(compo.name)
            alto.set_config(compo, config_dir)
            alto.stop()
        elif isinstance(compo, configuration.DssCommunityManager):
            cm = CommunityMgr(compo.name, compo.community)
            cm.set_config(compo, config_dir)
            cm.stop()
        elif isinstance(compo, configuration.DssLocalController):
            lc = LocalCtrl(compo.name, compo.community)
            lc.set_config(compo, config_dir)
            lc.stop()
        elif isinstance(compo, configuration.DssExternApp):
            ea = ExternApp(compo.name, compo.community)
            ea.set_config(compo, config_dir)
            ea.stop()
        elif isinstance(compo, configuration.DssMaestro):
            moni = Maestro(compo.name, compo.community)
            moni.set_config(compo, config_dir)
            moni.stop()
        elif isinstance(compo, configuration.DssTsar):
            moni = Tsar(compo.name, compo.community)
            moni.set_config(compo, config_dir)
            moni.stop()
        elif isinstance(compo, configuration.DssVmac):
            moni = Vmac(compo.name, compo.community)
            moni.set_config(compo, config_dir)
            moni.stop()
        elif isinstance(compo, configuration.DssRealtime):
            moni = Realtime(compo.name, compo.community)
            moni.set_config(compo, config_dir)
            moni.stop()
        elif isinstance(compo, configuration.DssSynoptic):
            syn = Synoptic(compo.name, compo.community)
            syn.set_config(compo, config_dir)
            syn.stop()
        elif isinstance(compo, configuration.DssCats):
            cats = Cats(compo.name, compo.community)
            cats.set_config(compo, config_dir)
            cats.stop()
        else:
            raise Exception("Composant " + compo.name + ": type inconnu: " + str(type(compo)))

    def local_reset(self, args):
        if platform.system() == "Linux":
            try:
                # kill ASPIC
                print("Killing ASPIC instances...")
                logging.info("Killing ASPIC instances...")
                # create ASPIC properties file
                with open("/tmp/killASPIC.properties", 'w') as f:
                    f.write("ASPIC_PORT=1976\n")
                    f.write("ASPIC_SIMU_HOST=localhost\n")
                    f.write("ASPIC_APPLI_RACINE=/tmp\n")
                    f.write("KILL_DSS=yes\n")
                    f.close()

                aspic_kill_cmd = '/home/SIMU_ASPIC/ASPIC/ASPIC_V' + versions.ASPIC_VERSION\
                                 + '/sh/ASPIC -p /tmp/killASPIC.properties -dS'
                p = subprocess.Popen(aspic_kill_cmd, shell="True", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                (stdout, stderr) = p.communicate()
                print("Killing ASPIC instances done")
                logging.info("Killing ASPIC instances done")
            except:
                print("Killing ASPIC failed")
                logging.info("Killing ASPIC failed")

            try:
                # kill DSS related processes
                print("Killing DSS processes...")
                logging.info("Killing DSS processes...")
                dss_kill_cmd = "kill -9 $(ps -A | egrep 'DSS_|D2B_' | awk '{ print $1}' )"
                p = subprocess.Popen(dss_kill_cmd, shell="True", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                (stdout, stderr) = p.communicate()
                print("Killing DSS processes done")
                logging.info("Killing DSS processes done")
            except:
                print("Killing DSS processes failed")
                logging.info("Killing DSS processes failed")

            try:
                # kill IONEXT
                ionext_kill_cmd = "sudo /home/ioland/REF/MOTEURS_ES/IONEXT/V" + versions.IONEXT_VERSION\
                                  + "/BINARIES/Linux32/bin/clean_platform"
                print("Killing IONEXT processes...")
                logging.info("Killing IONEXT processes...")
                p = subprocess.Popen(ionext_kill_cmd, shell="True")
                p.communicate()
                print("Killing IONEXT processes done")
                logging.info("Killing IONEXT processes done")
            except:
                print("Killing IONEXT processes failed")
                logging.info("Killing IONEXT processes failed")

            try:
                # kill AFDX
                print("Killing AFDX processes...")
                logging.info("Killing AFDX processes...")
                afdx_kill_cmd = "sudo /home/ioland/REF/MOTEURS_ES/AFDX/V" + versions.AFDX_VERSION\
                                + "/BINARIES/Linux32/bin/arret_scheduler_afdx.sh"
                p = subprocess.Popen(afdx_kill_cmd, shell="True", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                p.communicate()
                print("Killing AFDX processes done")
                logging.info("Killing AFDX processes done")
            except:
                print("Killing AFDX processes failed")
                logging.info("Killing AFDX processes failed")

            try:
                # fin gestion prio
                print("Calling fin_gestion_prio...")
                logging.info("Calling fin_gestion_prio...")
                fin_gestion_prio_cmd = "sudo " + versions.GESTION_PRIO_PATH + "/fin_gestion_prio.ksh"
                p = subprocess.Popen(fin_gestion_prio_cmd, shell="True")
                p.communicate()
                print("Calling fin_gestion_prio done")
                logging.info("Calling fin_gestion_prio done")
            except:
                print("Calling fin_gestion_prio failed")
                logging.info("Calling fin_gestion_prio failed")

            try:
                print("CPU unprotect...")
                logging.info("CPU unprotect...")
                # cpu unprotect
                import multiprocessing
                for cpu in range(0, multiprocessing.cpu_count()):
                    unprotect_cmd = "sudo " + versions.NUCLEUS_PATH + "/bin/cpu unprotect " + str(cpu)
                    p = subprocess.Popen(unprotect_cmd, shell="True")
                    p.communicate()
                print("CPU unprotect done")
                logging.info("CPU unprotect done")
            except:
                print("CPU unprotect error")
                logging.info("CPU unprotect error")
            if args.linux_script != "None":
                # resolve true path if pathmapper or relative path
                script_path = args.linux_script
                if os.path.isfile(script_path):
                    try:
                        print("Calling user provided clean script...")
                        logging.info("Calling user provided clean script...")
                        p = subprocess.Popen(script_path, shell="True")
                        p.communicate()
                        print("User provided clean script executed")
                        logging.info("User provided clean script executed")
                    except:
                        print("Calling user provided clean script failed")
                        logging.info("Calling user provided clean script failed")
                else:
                    print("User provided clean script does not exist")
                    logging.error("User provided clean script does not exist")
        else:
            try:
                # kill DSS related processes
                print("Killing DSS processes...")
                logging.info("Killing DSS processes...")
                dss_kill_cmd = "taskkill /F /IM D2B* & taskkill /F /IM DSS*"
                p = subprocess.Popen(dss_kill_cmd, shell="True")
                p.communicate()
                print("Killing DSS processes done")
                logging.info("Killing DSS processes done")
            except:
                print("Killing DSS processes failed")
                logging.info("Killing DSS processes failed")
            if args.windows_script != "None":
                # resolve true path if pathmapper or relative path
                script_path = args.windows_script
                if os.path.isfile(script_path):
                    try:
                        print("Calling user provided clean script...")
                        logging.info("Calling user provided clean script...")
                        p = subprocess.Popen(script_path, shell="True")
                        p.communicate()
                        print("User provided clean script executed")
                        logging.info("User provided clean script executed")
                    except:
                        print("Calling user provided clean script failed")
                        logging.info("Calling user provided clean script failed")
                else:
                    print("User provided clean script does not exist")
                    logging.error("User provided clean script does not exist")
        print("Reset done")
        logging.info("Reset done")

    def local_diagnostic(self, args):
        logging.info("diagnostic not yet available")
        print("diagnostic not yet available")
        sys.exit(1)


def run():
    AltoCli(sys.argv[1:])
