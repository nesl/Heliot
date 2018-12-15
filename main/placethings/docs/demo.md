# Demo

All examples are in the folder `placethings/demo`

To run all test cases:
```
sudo python main.py demo -tc run_all.Test
```

To run one test case:
```
$ python main.py -tc TESTCASE_MODULE.TESTCASE -c CONFIGFILE
```
For example:
```
$ python main.py -tc test_ddflow_demo_local.Test -c sample_configs/test_ddflow_demo_local
```
- <b>TESTCASE_MODULE</b> is the file name of your test case in placethings/demo
- <b>TESTCASE</b> is the name of the class that contains your test function.

To add one test case, please inherit <b>placethings.demo.BaseTestCase</b> and implement your own test logic in <b>test()</b> method.

Some of the demo cases runs tasks that depends on code from the sample library.

The source code for those predefined tasks are in the folder `sample_tasklib`

Here are some sample demo cases:
- base_test.py: the abstract class for a test case. All test cases mus follow the data structure.
- test_config_wrapper.py: definie configuration, export/import configuration to `config_simple`
- test_ddflow.py: read configuration from `config_ddflow_*` folder, compute good placements, output estimated latency
- test_ddflow_demo.py: given configuration from `config_ddflow_demo`, create a fixed virtual network and a set of computation resources
- test_ddflow_demo_all.py: just like `test_ddflow_demo.py` but the virtual network changes dynamically
- test_graph.py: given any configuration json files, read the configuration and compute a good placement

Test cases for code under development:
- test_config_base.py: test code for refactoring the configuration interfaces and logic.
