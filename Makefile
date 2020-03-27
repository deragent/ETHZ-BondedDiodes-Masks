
PYTHON_FILES = $(shell find mask/ -name '*.py')

${PROJECT}.gds: ${PYTHON_FILES}
	python3 -m mask.sets.${PROJECT}

all: ${PROJECT}.gds

show: ${PROJECT}.gds
	klayout ${PROJECT}.gds
