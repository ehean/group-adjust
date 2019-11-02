This repo contains two implementations of group_adjust: pure python and numpy. To test either one, run the following:
	pytest pure_python_implementation.py
	pytest numpy_implementation.py

The pure python is about 5-6 times faster than the numpy implementation. While the pure python solution executes the test_performance() in about 10-12 seconds, the numpy solution executes it in about 55-60 seconds. However, the numpy implementation demonstrates some basic numpy array manipulation, which I wanted to include for the sake of completeness. 
