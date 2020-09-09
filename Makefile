
PYTHON_FILES = $(shell find mask/ -name '*.py')

DIR = files/${PROJECT}/
GDS_FILE = ${DIR}${PROJECT}

${GDS_FILE}.gds: ${PYTHON_FILES}
	[ -f mask/sets/${PROJECT}.py ] || (>&2 echo "Project file [mask/sets/${PROJECT}.py] does not exist" && exit 1)
	mkdir -p ${DIR}
	python3 -m mask.sets.${PROJECT} --output ${GDS_FILE}.gds

all: ${GDS_FILE}.gds

show: ${GDS_FILE}.gds
	klayout ${GDS_FILE}.gds

export: ${GDS_FILE}.gds
	mkdir -p ${DIR}export
	rm ${DIR}export/* -f
	python3 -m mask.sets.${PROJECT} --output ${GDS_FILE}.gds --export ${DIR}export
