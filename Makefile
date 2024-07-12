# If you are new to Makefiles: https://makefiletutorial.com

PAPER := output/paper.pdf
PRESENTATION := output/presentation.pdf

TARGETS :=  $(PAPER) $(PRESENTATION)

# Configs
STATIC_DATA := data/external/wscp_static.txt
PANEL_DATA := data/external/wscp_panel.xlsx

.PHONY: all clean very-clean dist-clean

all: $(TARGETS)

clean:
	rm -f $(TARGETS)

very-clean: clean
	rm -f $(STATIC_DATA) $(PANEL_DATA)

dist-clean: very-clean
	rm -f config.csv

$(PAPER): doc/paper_mine.qmd doc/references.bib
	quarto render $< --quiet
	mv doc/paper_mine.pdf output
	rm -f doc/paper_mine.ttt doc/paper_mine.fff

$(PRESENTATION): doc/presentation_mine.qmd doc/beamer_theme_trr266.sty
	quarto render $< --quiet
	mv doc/presentation_mine.pdf output
	rm -rf doc/presentation_mine_files