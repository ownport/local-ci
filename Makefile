PYTHON ?= /usr/bin/env python
PROJECT_NAME_BIN ?= local-ci
PROJECT_NAME_SRC ?= local_ci

clean:
	@ echo "[INFO] Cleaning directory:" $(shell pwd)/bin
	@ rm -rf $(shell pwd)/bin
	@ echo "[INFO] Cleaning directory:" $(shell pwd)/.local-ci
	@ rm -rf $(shell pwd)/.local-ci
	@ echo "[INFO] Cleaning directory:" $(shell pwd)/local-ci.egg-info
	@ rm -rf $(shell pwd)/local-ci.egg-info
	@ echo "[INFO] Cleaning files: *.pyc"
	@ find . -name "*.pyc" -delete
	@ echo "[INFO] Cleaning files: .coverage"
	@ rm -rf $(shell pwd)/.coverage


$(PROJECT_NAME_BIN): clean
	@ echo "[INFO] Compiling to binary, $(PROJECT_NAME_BIN)"
	@ mkdir -p $(shell pwd)/bin
	@ cd $(shell pwd)/$(PROJECT_NAME_SRC)/; zip --quiet -r ../bin/$(PROJECT_NAME_BIN) *
	@ echo '#!$(PYTHON)' > bin/$(PROJECT_NAME_BIN) && \
		cat bin/$(PROJECT_NAME_BIN).zip >> bin/$(PROJECT_NAME_BIN) && \
		rm bin/$(PROJECT_NAME_BIN).zip && \
		chmod a+x bin/$(PROJECT_NAME_BIN)


test-all: clean
	@ py.test

test-all-with-coverage: clean
		@ py.test --cov=local_ci --cov-report term-missing --cov-config=.coveragerc

run-local-ci: clean $(PROJECT_NAME_BIN)
	@ ./bin/local-ci -r $(shell pwd) -s .local-ci.yml
