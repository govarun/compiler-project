
section .text
	global main
main:
	mov edx, 0
	mov eax, 52
	push eax
	add esp, 4
	ret

section .data
	x	db	0
	y 	dw	32

