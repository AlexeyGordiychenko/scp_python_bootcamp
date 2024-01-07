PYTHON=python3

ex00:
	cd EX00/ &&	${PYTHON} setup.py install
	pytest EX00

ex01:
	${PYTHON} EX01/monotonic.py

ex02:
	cd EX02/ &&	${PYTHON} setup.py build_ext --inplace
	pytest EX02
	${PYTHON} EX02/test_mul_perf.py

.PHONY: ex00 ex01 ex02