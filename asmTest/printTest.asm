extern printf
extern scanf
section .text
	global main
main:
    push ebp
	mov ebp, esp

    mov edx, dword [y]
    push 4
    push str
    call printf

	mov esp, ebp
	pop ebp
	ret 

section .data
	x	dd	0
	y 	dd	32
    str: db  "Hello there %d", 0

