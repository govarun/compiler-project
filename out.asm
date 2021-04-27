extern printf
section .text
	global main
main:
	push ebp
	mov ebp, esp
	sub esp, 4
	mov dword [ebp-4], 0
	mov eax, dword [ebp-4]
	cmp eax, 0
	je __l0
	push __t_0
	call printf
	mov dword [__t_1], eax
	add esp, 4
	jmp __l1
__l0:
	push __t_2
	call printf
	mov dword [__t_3], eax
	add esp, 4
__l1:
	mov eax, 1
	mov esp, ebp
	pop ebp
	ret
section	.data
	__t_1	dd	0
	__t_3	dd	0
	__t_0:	db	`1`, 0
	__t_2:	db	`0`, 0
