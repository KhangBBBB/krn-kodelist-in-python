TARGET= KrunUserManual.pdf
FILE=KrunUserManual.kdoc
KDOC2PDF=kdoc2pdf

all: $(FILE)
	cat $(FILE) | $(KDOC2PDF) > $(TARGET)

clean: $(TARGET)
	rm -R $(TARGET)
