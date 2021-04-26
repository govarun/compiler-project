
section .text
	global main
main:
	mov rdx, 0
	mov rax, 512
	not byte [x]
	mov al, byte [x]
	ret

section .data
	x	db	0
	y 	dw	32

