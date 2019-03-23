EMCC = emcc
SOURCES = diceroll.c
EMFLAGS = -O1 -s WASM=1	# set optimization flag and
						# information for the compiler to work in WASM mode, otherwise the asm.js code will be generated

build:	$(SOURCES)
		$(EMCC) $(EMFLAGS) $(SOURCES) -o diceroll.js

test:
		emrun --no_browser --port 8080 .
