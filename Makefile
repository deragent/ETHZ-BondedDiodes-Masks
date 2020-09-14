
PYTHON_FILES = $(shell find mask/ -name '*.py')

DIR = files/${PROJECT}/
GDS_FILE = ${DIR}${PROJECT}

all: check_project ${GDS_FILE}.gds

${GDS_FILE}.gds: ${PYTHON_FILES}
	mkdir -p ${DIR}
	python3 -m mask.sets.${PROJECT} --output ${GDS_FILE}.gds

show: check_project ${GDS_FILE}.gds
	klayout ${GDS_FILE}.gds

clean: check_project
	rm -r ${DIR}

export: check_project ${GDS_FILE}.gds
	mkdir -p ${DIR}export
	rm ${DIR}export/* -f
	python3 -m mask.sets.${PROJECT} --output ${GDS_FILE}.gds --export ${DIR}export

check_project:
	[ -f mask/sets/${PROJECT}.py ] || (>&2 echo "Project file [mask/sets/${PROJECT}.py] does not exist" && exit 1)

check: check_project ${GDS_FILE}.gds
	python3 -m mask.tools.HeidelbergLWFileCheck ${GDS_FILE}.gds
