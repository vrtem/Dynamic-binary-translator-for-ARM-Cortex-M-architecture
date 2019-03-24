(module
    ;; Define a function that takes two i32 parameters and returns a i32 number.
    (type $0 (func (param i32 i32) (result i32)))
    (memory $0 0)
    ;; Export the first function defined in the type section with name 'sum'.
    (export "sum" (func $0))
    ;; The body of the function defined above.
    (func $0 (type $0) (param $var$0 i32) (param $var$1 i32) (result i32) 
        ;; The opcode (operation code) that stands for addition of i32.
        (i32.add    ;; 'i32.add' grabs the previous two values pushed onto the stack, computes their sum,
                    ;; and pushes the resulting i32 value.
            (get_local $var$0)  ;; Load first param by pushing it to the stack.
            (get_local $var$1)  ;; Load second param by pushing it to the stack.
            ;; The return value of the function is just the final value left on the stack.
        )
    )
)