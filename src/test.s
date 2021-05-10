extern printf
extern scanf
extern malloc
extern free
extern pow
extern abs
section .text
	global main
main:
	push ebp
	mov ebp, esp
	sub esp, 12
	movss xmm0, dword [ebp-4]
	sub	esp, 8
	mov eax, [ebp-8]
	fld dword [eax]
	fstp qword [esp]
	push __t_1
	movss dword [ebp-8], xmm0
	movss dword [ebp-4], xmm0
	call printf
	mov dword [ebp-12], eax
	add esp, 8
	mov eax, 1
	mov esp, ebp
	pop ebp
	ret
section	.data
	NULL_0	dd	0
	__t_1:	db	`%f`, 0
	__t_0	dd	1.0
