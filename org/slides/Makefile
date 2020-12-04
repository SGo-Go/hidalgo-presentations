.PHONY: all clean

OUT_DIR=.
FILES=$(patsubst %.org, $(OUT_DIR)/%.html, $(wildcard *.org))

all: ${FILES}

%.html: %.org
	emacs $< --batch -f org-re-reveal-export-to-html

clean:
	rm ${FILES} *~
