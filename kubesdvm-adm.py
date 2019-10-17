import argparse
import os
import traceback
from sys import exit

from analyser.analyse import get_cmd_config
from operation import *
from utils import logger

LOG = "/var/log/kubesds.log"

logger = logger.set_logger(os.path.basename(__file__), LOG)



def query(args):
    queryVM(args.domain)


# --------------------------- cmd line parser ---------------------------------------
parser = argparse.ArgumentParser(prog="kubesdvm-adm", description="All vm operation tools")

subparsers = parser.add_subparsers(help="sub-command help")

# -------------------- add QueryVM cmd ----------------------------------
parser_query_vm = subparsers.add_parser("queryVM", help="queryVM help")
parser_query_vm.add_argument("--domain", metavar="[DOMAIN]", type=str,
                                help="query vm info")

# set default func
parser_query_vm.set_defaults(func=query)


# query1 = parser.parse_args(["queryVM", "--domain", "vm003"])
#
# try:
#     query1.func(query1)
# except TypeError:
#     logger.debug(traceback.format_exc())


# --------------------- auto generate------------------------------
cmd_config = get_cmd_config()
