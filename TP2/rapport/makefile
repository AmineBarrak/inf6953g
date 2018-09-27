LATEX=rapport
rapport:rapport.tex

all: r

r: $(LATEX)
bib: $(LATEX)
	bibtex $<
	pdflatex $<


$(LATEX):
	pdflatex $<
