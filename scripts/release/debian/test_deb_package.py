# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import sys
import subprocess

python_minor_version = sys.version_info[1]
root_dir = f'/opt/az/lib/python3.{python_minor_version}/site-packages/azure/cli/command_modules'
mod_list = [mod for mod in sorted(os.listdir(root_dir)) if os.path.isdir(os.path.join(root_dir, mod)) and mod != '__pycache__']

pytest_base_cmd = '/opt/az/bin/python3 -m pytest -v --forked -p no:warnings --log-level=WARN'
pytest_parallel_cmd = '{} -n logical'.format(pytest_base_cmd)

# cloud: https://github.com/Azure/azure-cli/pull/14994
# appservice: https://github.com/Azure/azure-cli/pull/19810
# iot, resource, azure-cli-core: https://github.com/Azure/azure-cli/pull/26176
serial_test_modules = ['botservice', 'network', 'cloud', 'appservice', 'iot', 'resource']

for mod_name in mod_list:
    cmd = '{} --junit-xml /azure_cli_test_result/{}.xml --pyargs azure.cli.command_modules.{}'.format(
        pytest_base_cmd if mod_name in serial_test_modules else pytest_parallel_cmd, mod_name, mod_name)
    print('Running:', cmd, flush=True)
    exit_code = subprocess.call(cmd, shell=True)
    if exit_code == 5:
        print('No tests found for {}'.format(mod_name))
    elif exit_code != 0:
        sys.exit(exit_code)

exit_code = subprocess.call(['{} --junit-xml /azure_cli_test_result/azure-cli-core.xml --pyargs azure.cli.core'.format(pytest_base_cmd)], shell=True)
sys.exit(exit_code)
