
all: score-sheet-2019.pdf

%.pdf: %.svg
	inkscape -A $@ $<

clean:
	rm -f *.pdf
