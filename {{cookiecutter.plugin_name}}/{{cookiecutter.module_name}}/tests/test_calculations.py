""" Tests for calculations

"""
from __future__ import print_function
from __future__ import absolute_import

import os
import {{cookiecutter.module_name}}.tests as tests
import pytest



# pylint: disable=unused-argument
@pytest.mark.process_execution
def test_process(new_database, new_workdir):
    """Test running a calculation
    note this does not test that the expected outputs are created of output parsing"""
    from aiida.orm.data.singlefile import SinglefileData

    # get code
    code = tests.get_code(entry_point='{{cookiecutter.entry_point_prefix}}')

    # Prepare input parameters
    from aiida.orm import DataFactory
    DiffParameters = DataFactory('{{cookiecutter.entry_point_prefix}}')
    parameters = DiffParameters({'ignore-case': True})

    file1 = SinglefileData(
        file=os.path.join(tests.TEST_DIR, "input_files", 'file1.txt'))
    file2 = SinglefileData(
        file=os.path.join(tests.TEST_DIR, "input_files", 'file2.txt'))

    # set up calculation
    calc = code.new_calc()
    calc.label = "{{cookiecutter.module_name}} test"
    calc.description = "Test job submission with the {{cookiecutter.module_name}} plugin"
    calc.set_max_wallclock_seconds(30)
    calc.set_withmpi(False)
    calc.set_resources({"num_machines": 1, "num_mpiprocs_per_machine": 1})

    calc.use_parameters(parameters)
    calc.use_file1(file1)
    calc.use_file2(file2)

    calc.store_all()

    ## output input files and scripts to temporary folder
    #from aiida.common.folders import SandboxFolder
    #with SandboxFolder() as folder:
    #    subfolder, script_filename = calc.submit_test(folder=folder)
    #    print("inputs created successfully at {0} with script {1}".format(
    #        subfolder.abspath, script_filename))
    # test process execution and check the expected outputs
    # for diff 0=no differences, 1=differences, >1=error
    tests.test_calculation_execution(
        calc, allowed_returncodes=(1, ), check_paths=[calc._OUTPUT_FILE_NAME])  # pylint: disable=protected-access
