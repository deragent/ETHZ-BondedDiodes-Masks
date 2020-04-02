
PYTHON_FILES = $(shell find mask/ -name '*.py')

DIR = files/${PROJECT}/
GDS_FILE = ${DIR}${PROJECT}

${GDS_FILE}.gds: ${PYTHON_FILES}
	mkdir -p ${DIR}
	python3 -m mask.sets.${PROJECT} --output ${GDS_FILE}.gds

all: ${GDS_FILE}.gds

show: ${GDS_FILE}.gds
	klayout ${GDS_FILE}.gds

export: ${GDS_FILE}.gds
	mkdir -p ${DIR}export
	## TODO
