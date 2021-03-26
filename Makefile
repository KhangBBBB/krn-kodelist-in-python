
BASE_DIR=/
BIN_DIR=$(BASE_DIR)usr/bin/
# MAKE=/usr/bin/make

all:
	cd src/krun && $(MAKE) all
	cd src/kodelist && $(MAKE) all
install:
	cp -R src/krun/krun $(BIN_DIR)
	cp -R src/kodelist/kodelist $(BIN_DIR)

clean:
	cd src/krun && $(MAKE) clean
	cd src/kodelist && $(MAKE) clean

