# C to WebAssembly

To compile C file to WebAssembly you need to download: [Emscripten SDK](https://s3.amazonaws.com/mozilla-games/emscripten/releases/emsdk-portable.tar.gz), extract, enter the folder and execute the following commands:
```bash
./emsdk update
./emsdk install latest
./emsdk activate latest
source ./emsdk_env.sh
```

`make build` - creates a JavaScript file with the translated function that can be run in the browser.
`make wasm` - creates a .wasm file.
`make test` - runs a local server provided by Emscripten SDK on port 8080 [(localhost:8080/index.html)](localhost:8080/index.html)