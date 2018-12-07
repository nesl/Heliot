This folder contains examples and test cases.

- base_test.py: the abstract class for a test case. All test cases mus follow the data structure.
- test_config_wrapper.py: definie configuration, export/import configuration to `config_simple`
- test_ddflow.py: read configuration from `config_ddflow_*` folder, compute good placements, output estimated latency
- test_ddflow_demo.py: given configuration from `config_ddflow_demo`, create a fixed virtual network and a set of computation resources
- test_ddflow_demo_all.py: just like `test_ddflow_demo.py` but the virtual network changes dynamically
- test_graph.py: given any configuration json files, read the configuration and compute a good placement

Test cases for code under development:

- test_config_base.py: test code for refactoring the configuration interfaces and logic.
