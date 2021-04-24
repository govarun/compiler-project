
section .text
	global main
main:
	mov rdx, 0
	mov ebx, 0
	mov rax, 0
lbl1: 
	cmp ebx, 10
	jg lbl2
	add rax, qword [x]
	inc ebx
	jmp lbl1
lbl2:
	ret

section .data
	x	dw	12
	y 	dd	32

