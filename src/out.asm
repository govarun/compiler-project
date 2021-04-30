extern printf
extern scanf
section .text
	global main
main:
	push ebp
	mov ebp, esp
	sub esp, 20
