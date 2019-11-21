all:
	@echo 'make clean | build | test'

clean:
	rm -rf *.pyc __pycache__
	rm -rf priority_queue.egg-info build dist

build: clean
	python setup.py sdist bdist_wheel

test:
	py.test tests/* \
		--cov priority_queue \
		--cov-config .coveragerc \
		--cov-report html \
		--cov-report term \
		--cov-fail-under=100
