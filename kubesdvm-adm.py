import argparse
import os
import traceback
from sys import exit

from analyser.analyse import get_cmd_configs, get_cmd_map
from operation import *
from utils import logger

LOG = "/var/log/kubesds.log"

logger = logger.set_logger(os.path.basename(__file__), LOG)



def query(args):
    queryVM(args.name)


# --------------------------- cmd line parser ---------------------------------------
parser = argparse.ArgumentParser(prog="kubesdvm-adm", description="All vm operation tools")

subparsers = parser.add_subparsers(help="sub-command help")

# -------------------- add QueryVM cmd ----------------------------------
parser_query_vm = subparsers.add_parser("queryVM", help="queryVM help")
parser_query_vm.add_argument("--name", metavar="[NAME]", type=str,
                                help="query vm info")

# set default func
parser_query_vm.set_defaults(func=query)


# query1 = parser.parse_args(["queryVM", "--name", "vm003"])
#
# try:
#     query1.func(query1)
# except TypeError:
#     logger.debug(traceback.format_exc())


# --------------------- auto generate------------------------------
cmd_configs = get_cmd_configs()
cmd_map = get_cmd_map()
for cmd in cmd_configs.keys():
    # -------------------- add QueryVM cmd ----------------------------------
    description = cmd_configs[cmd]
    parser_cmd = subparsers.add_parser(cmd, help=description)

    params = cmd_configs[cmd]['params']
    for param in params.keys():
        p_name = param
        p_type = params[param]['p_type']
        # arguments are all optional, if not set, exeception will be raise, when virsh cmd is executing,
        if p_type == 'str':
            parser_cmd.add_argument("--"+p_name, metavar="["+p_name+"]", type=str,
                                         help="")
        elif p_type == 'bool':
            parser_cmd.add_argument("--"+p_name, metavar="["+p_name+"]", type=bool,
                                         help="")

    def cmd_func(args):
        createInstance("operation", cmd_map[cmd], cmd='virsh '+cmd, op=cmd_map[cmd], params=args)
        createInstance.invoke()
    # set default func
    parser_cmd.set_defaults(func=cmd_func)



try:
    args = parser.parse_args()
    args.func(args)
except TypeError:
    # print "argument number not enough"
    logger.debug(traceback.format_exc())



