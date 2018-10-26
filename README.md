# DPDKick
Ultimate DPDK System Enabling Expert

# Usage

1. Complete ./dpdkick.conf
2. Straightly run
`./dpdkick.py`

# Add New Testcases

## Implement your testcase in a test suite
./testcases/mytest.py

_in `mytest.py`_

```python
import unittest

class mytest_class(unittest.TestCase):
    # Each testcase's def name must start with "test_"
    def test_mytest_test1(self):
        # Testlogic
        self.assertEqual(my_assert)
```

## Run the test suite
_./dpdkick.py_

in `dpdkick.py`

```python
mytest_suite = unittest.TestLoader().loadTestsFromTestCase(mytest.mytest_class)
runner.run(mytest_suite, description = 'Mytest suite')
```
