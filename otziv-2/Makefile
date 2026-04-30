all: otziv.pdf

otziv.pdf: otziv.tex
	pdflatex otziv.tex
	pdflatex otziv.tex

clean:
	rm -f *.aux *.log *.out *.toc *.pdf

.PHONY: all clean
