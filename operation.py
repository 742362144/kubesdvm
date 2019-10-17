import os
import traceback
from xml.etree.ElementTree import fromstring
from xmljson import badgerfish as bf
from json import dumps, loads
from sys import exit

from utils.exception import *
# from utils.libvirt_util import get_pool_info, get_volume_xml, get_volume_path, get_volume_snapshots, is_pool_started, \
#     is_pool_defined
from utils.libvirt_util import get_xml, vm_state
from utils.utils import *
from utils import logger

LOG = "/var/log/kubesdvm.log"

logger = logger.set_logger(os.path.basename(__file__), LOG)


class Executor(object):
    def __init__(self, cmd, params, with_result=False):
        if cmd is None or cmd == "":
            raise Exception("plz give me right cmd.")
        if not isinstance(params, dict):
            raise Exception("plz give me right parameters.")

        self.params = params
        self.cmd = cmd
        self.params = params
        self.with_result = with_result

    def get_cmd(self):
        cmd = self.cmd
        for key in self.params.keys():
            cmd = cmd + " --" + key + " " + self.params[key] + " "
        return cmd

    def execute(self):
        cmd = self.get_cmd()
        logger.debug(cmd)

        if self.with_result:
            return runCmdWithResult(cmd)
        else:
            return runCmd(cmd)


class Operation:
    def __init__(self, op, params):
        self.op = op
        self.params = params

    def prepare(self):
        raise ExecuteException('not impl prepare interface', 'not impl prepare interface')

    def check(self):
        raise ExecuteException('not impl check interface', 'not impl check interface')

    def do(self):
        raise ExecuteException('not impl do interface', 'not impl do interface')

    def invoke(self):
        logger.debug(self.params)

        try:
            self.do()
        except ExecuteException, e:
            logger.debug(self.params)
            logger.debug(traceback.format_exc())
            print dumps(
                {"result": {"code": 400, "msg": "error occur while " + self.op + ". " + e.message},
                 "data": {}})
            exit(1)
        except Exception:
            logger.debug("opreation: " + self.op)
            logger.debug(self.params)
            logger.debug(traceback.format_exc())
            print dumps(
                {"result": {"code": 300, "msg": "error occur while " + self.op + "."}, "data": {}})
            exit(1)


class CreateVM(Operation):
    def check(self):
        pass

    def do(self):
        pass

class StartVM(Operation):
    def check(self):
        pass

    def do(self):
        pass

class StopVM(Operation):
    def check(self):
        pass

    def do(self):
        pass

class StopVMForce(Operation):
    def check(self):
        pass

    def do(self):
        pass

class DeleteVM(Operation):
    def check(self):
        pass

    def do(self):
        pass

class RebootVM(Operation):
    def check(self):
        pass

    def do(self):
        pass

class ResetVM(Operation):
    def check(self):
        pass

    def do(self):
        pass

class ResumeVM(Operation):
    def check(self):
        pass

    def do(self):
        pass

class SuspendVM(Operation):
    def check(self):
        pass

    def do(self):
        pass

class SaveVM(Operation):
    def check(self):
        pass

    def do(self):
        pass

class RestoreVM(Operation):
    def check(self):
        pass

    def do(self):
        pass

class MigrateVM(Operation):
    def check(self):
        pass

    def do(self):
        pass

class ManageISO(Operation):
    def check(self):
        pass

    def do(self):
        pass

class UpdateOS(Operation):
    def check(self):
        pass

    def do(self):
        pass

class PlugDevice(Operation):
    def check(self):
        pass

    def do(self):
        pass

class UnplugDevice(Operation):
    def check(self):
        pass

    def do(self):
        pass

class PlugDisk(Operation):
    def check(self):
        pass

    def do(self):
        pass

class UnplugDisk(Operation):
    def check(self):
        pass

    def do(self):
        pass

class PlugNIC(Operation):
    def check(self):
        pass

    def do(self):
        pass

class UnplugNIC(Operation):
    def check(self):
        pass

    def do(self):
        pass

class ChangeNumberOfCPU(Operation):
    def check(self):
        pass

    def do(self):
        pass

class ResizeRAM(Operation):
    def check(self):
        pass

    def do(self):
        pass

class ResizeMaxRAM(Operation):
    def check(self):
        pass

    def do(self):
        pass

class ResizeVM(Operation):
    def check(self):
        pass

    def do(self):
        pass

class TuneDiskQoS(Operation):
    def check(self):
        pass

    def do(self):
        pass

class TuneNICQoS(Operation):
    def check(self):
        pass

    def do(self):
        pass

class SetBootOrder(Operation):
    def check(self):
        pass

    def do(self):
        pass

class SetVncPassword(Operation):
    def check(self):
        pass

    def do(self):
        pass

class UnsetVncPassword(Operation):
    def check(self):
        pass

    def do(self):
        pass

def queryVM(domain):
    logger.debug(domain)
    try:
        vm_xml = get_xml(domain)
        vm_power_state = vm_state(domain).get(domain)
        vm_json = toKubeJson(xmlToJson(vm_xml))
        vm_json = updateDomain(loads(vm_json))

        print dumps(
            {"result": {"code": 0, "msg": "query vm "+domain+" success."},
             "data": vm_json})
        exit(0)
    except ExecuteException, e:
        logger.debug(traceback.format_exc())
        print dumps(
            {"result": {"code": 400, "msg": "error occur while " + ". " + e.message},
             "data": {}})
        exit(1)
    except Exception:
        traceback.print_exc()
        print dumps(
            {"result": {"code": 300, "msg": "error occur while " "."}, "data": {}})
        exit(1)

def updateDomain(jsondict):
    with open('/root/arraylist.cfg' % os.path.dirname(__file__)) as fr:
        for line in fr:
            l = str.strip(line)
            alist = l.split('-')
            _userDefinedOperationInList('domain', jsondict, alist)
    return jsondict

'''
Cautions! Do not modify this function because it uses reflections!
'''
def _userDefinedOperationInList(field, jsondict, alist):
    jsondict = jsondict[field]
    tmp = jsondict
    do_it = False
    for index, value in enumerate(alist):
        if index == 0:
            if value != field:
                break;
            continue
        tmp = tmp.get(value)
        if not tmp:
            do_it = False
            break;
        do_it = True
    if do_it:
        tmp2 = None
        for index, value in enumerate(alist):
            if index == 0:
                tmp2 = 'jsondict'
            else:
                tmp2 = '{}[\'{}\']'.format(tmp2, value)
        exec('{} = {}').format(tmp2, _addListToSpecificField(tmp))
    return

def _addListToSpecificField(data):
    if isinstance(data, list):
        return data
    else:
        return [data]

def xmlToJson(xmlStr):
    return dumps(bf.data(fromstring(xmlStr)), sort_keys=True, indent=4)

def toKubeJson(json):
    return json.replace('@', '_').replace('$', 'text').replace(
            'interface', '_interface').replace('transient', '_transient').replace(
                    'nested-hv', 'nested_hv').replace('suspend-to-mem', 'suspend_to_mem').replace('suspend-to-disk', 'suspend_to_disk')
