PROG_NAME=CalcSimilarity
OBJ_DIR=obj
OUT_DIR=bin
INC=-Ilibs/includes


all: directories main

directories: ${OBJ_DIR} ${OUT_DIR}
${OBJ_DIR}:
	mkdir -p ${OBJ_DIR}
${OUT_DIR}:
	mkdir -p ${OUT_DIR}

main: main.cpp Point ResultStructure FileIO
	g++ -Wall -O2 $(INC) -o ${OUT_DIR}/${PROG_NAME} main.cpp ${OBJ_DIR}/FileIO.o


FileIO: FileIO.cpp FileIO.hpp
	g++ -Wall $(INC) -c FileIO.cpp -o ${OBJ_DIR}/FileIO.o
Point: Point.hpp
ResultStructure: ResultStructure.hpp

clean:
	rm -rf ${OBJ_DIR} ${OUT_DIR}