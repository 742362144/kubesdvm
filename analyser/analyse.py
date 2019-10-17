from utils.utils import runCmdAndGetOutput


def get_all_cmd():
    fp = open('cmd')
    cmds = []
    for line in fp.readlines():
        cmds.append(line.split()[0])
    print cmds
    return cmds

def get_cmd_description_and_params(subcmd):
    param_lines = runCmdAndGetOutput('virsh ' + subcmd +' --help')[1:]
    description, params = None, {}
    for i in range(len(param_lines)):
        if param_lines[i].strip() == 'DESCRIPTION':
            description = param_lines[i+1].strip()
        if param_lines[i].find('[--') >= 0 and param_lines[i].find('<string>') >= 0:
            k = param_lines[i].split()[0].replace('-', '').replace('[', '').replace(']', '')
            v = {'p_type': 'str', 'required': True}
            params[k] = v
        elif param_lines[i].find('--') >= 0 and param_lines[i].find('<string>') >= 0:
            k = param_lines[i].split()[0].replace('-', '').replace('[', '').replace(']', '')
            v = {'p_type': 'str', 'required': False}
            params[k] = v
        elif param_lines[i].find('--') >= 0 and param_lines[i].find('<string>') < 0:
            k = param_lines[i].split()[0].replace('-', '').replace('[', '').replace(']', '')
            v = {'p_type': 'bool', 'required': False}
            params[k] = v

    return description, params


def get_cmds(subcmd):
    cmds = []
    cmd_lines = runCmdAndGetOutput('virsh help '+subcmd)[1:]
    for line in cmd_lines:
        cmds.append(line.split()[0])
    return cmds

def get_cmd_config():
    result = {}
    for subcmd in get_cmds('domain'):
        result[subcmd] = get_cmd_description_and_params(subcmd)

# get_all_cmd()
# for subcmd in get_cmds('domain'):
#     print get_cmd_description_and_params(subcmd)
