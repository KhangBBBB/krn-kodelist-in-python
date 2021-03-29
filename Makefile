BASE_DIR=/
BIN_DIR=$(BASE_DIR)usr/bin/
# MAKE=/usr/bin/make

all:
	cd src/krn && $(MAKE) all
	cd src/kodelist && $(MAKE) all
install:
	cp -R src/krn/krn $(BIN_DIR)
	cp -R src/kodelist/kodelist $(BIN_DIR)

clean:
	cd src/krn && $(MAKE) clean
	cd src/kodelist && $(MAKE) clean


