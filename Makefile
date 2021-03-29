BASE_DIR=/
BIN_DIR=$(BASE_DIR)usr/bin/
# MAKE=/usr/bin/make

all:
	cd src/krn && $(MAKE) all
	cd src/kodelist && $(MAKE) all
install:
	cp -R src/krn/krn $(BIN_DIR) && chmod +x $(BIN_DIR)krn
	cp -R src/kodelist/kodelist $(BIN_DIR) && chmod +x $(BIN_DIR)kodelist

clean:
	cd src/krn && $(MAKE) clean
	cd src/kodelist && $(MAKE) clean


