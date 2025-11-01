SHELL := /bin/bash
PYTHON := python3

.PHONY: all setup lint sim cov runtime test docs bench clean

all: runtime test

setup:
	$(PYTHON) -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -r scripts/requirements.txt

lint:
	verilator --lint-only rtl/top/gb10_soc_top.sv rtl/cpu/gb10_cpu_cluster.sv rtl/gpu/gb10_gpu_core.sv rtl/interconnect/axi_noc_router.sv rtl/memory/lpddr5x_controller.sv
	$(PYTHON) scripts/infra.py lint

sim:
	$(PYTHON) scripts/infra.py sim

cov:
	$(PYTHON) scripts/infra.py cov

runtime:
	cmake -S runtime/libquasim -B build/libquasim -DCMAKE_BUILD_TYPE=RelWithDebInfo
	cmake --build build/libquasim

bench: runtime
	$(PYTHON) scripts/infra.py bench

install:
	cmake --install build/libquasim --prefix install

test:
	PYTHONPATH=runtime/python:quantum $(PYTHON) -m pytest -q

docs:
	$(PYTHON) scripts/infra.py docs

clean:
	rm -rf build install .venv
	rm -f tests/software/*.pyc runtime/python/quasim/__pycache__
