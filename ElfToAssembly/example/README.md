# Simple bare metal C program for ARM Cortex M3 with QEMU

Create a file with `C` code that you want to run on the ARM Cortex M3 machine.
```c
static const int a = 7;
static int b = 8;
static int sum;

void main()
{
  sum = a + b;
}
```

Compile the `C` file into object files using gcc.
Use the startup code named `startup.c` from this repo.

```
arm-none-eabi-gcc -O0 -c -g -mcpu=cortex-m3 -mthumb -o test_program.o test_program.c
arm-none-eabi-gcc -O0 -c -g -mcpu=cortex-m3 -mthumb -o startup.o startup.c
```

Link the object files according to the rules in our linker script named `stm32.ld` using GNU linker `ld`.
```
arm-none-eabi-ld -Tstm32.ld -o test_program.elf startup.o test_program.o
```

Use objcopy to convert the `.elf` file from the linker into a “raw” binary. The “raw” binary is what we will run on the target.
```
arm-none-eabi-objcopy -O binary test_program.elf test_program.bin
```

Use QEMU with Cortex M3 machine to run the program.
```
qemu-system-arm -M lm3s811evb -serial stdio -kernel test_program.bin
```
