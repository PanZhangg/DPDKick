# DPDKick
Ultimate DPDK System Enabling Expert

# Usage
Straightly run
`./dpdkick.py`

# Add New Testcases

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

_./testcases/utility/env.py_

in `env.py`

```python
    self.mytestcases = mytest.mytest_class()
```

_./dpdkick.py_

in `dpdkick.py`

```python
mytest_suite = unittest.TestLoader().loadTestsFromTestCase(mytest.mytest_class)
runner.run(mytest_suite, description = 'Mytest suite')
```
