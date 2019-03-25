var bytecode = new Uint8Array([
    // preamble
    0x00, 0x61, 0x73, 0x6d, 0x01, 0x00, 0x00, 0x00,     // The first 4 bytes is a uint32 'magic number' 0x6d736100 that spells out '\0asm' in ASCII.
                                                        // The point of this magic number is to quickly determine if this file is a wasm module or not.
                                                        // The next four bytes is a uint32 number that represents the version of the wasm specification this file was constructed with.
    // type section
    0x01, 0x07, 0x01, 0x60, 0x02, 0x7f, 0x7f, 0x01,     // Type section, the size of the rest of the section, the number of function signatures, the kind of function and parameters,
    0x7f,                                               // the function takes two i32 parameters and returns i32 number.

    // function section
          0x03, 0x02, 0x01, 0x00,                       // Func section, the size of the rest of the section, the number of functions, references the type signature with index 0.
    
    // export section
                                  0x07, 0x07, 0x01,     // Export section, the size of the rest of the section, the number of exported functions,
    0x03, 0x61, 0x64, 0x64, 0x00, 0x00,                 // the size of the name, name - 'add' (3 bytes), export a function, with index 0

    // code section
                                        0x0a, 0x09,     // Code section, the size of the rest of the section,
    0x01, 0x07, 0x00, 0x20, 0x00, 0x20, 0x01, 0x6a,     // the number of function bodies, size of the first function body, the number of local variables,
                                                        // load first and second argument onto the stack (2 x 2 bytes), replace the two topmost values on the stack with their sum,
    0x0b                                                // end (returns the last value placed on the stack - add result).
                                                ]);

WebAssembly.instantiate(bytecode).then(function(wasm) {
    console.log(wasm.instance.exports.add(1, 2))
});
