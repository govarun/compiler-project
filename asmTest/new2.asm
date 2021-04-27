global main

;Declare used libc functions
extern exit
extern puts
extern scanf
extern printf

section .text

main:

push dword msg
call puts
add esp, 4

push dword a
push dword b
push dword msg1
call scanf
add esp, 12

mov eax, dword [a]
add eax, dword [b]
mov eax, dword [c]
push eax
push dword msg2
call printf
add esp, 8

call exit
ret

section .data
msg  : db "An example of interfacing with GLIBC.",0xA,0
msg1 : db "%d%d",0
msg2 : db "%d", 0xA, 0
c   dw 4

section .bss
a resd 1
b resd 1