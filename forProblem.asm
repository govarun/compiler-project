extern printf
section .text
	global main
main:
	push ebp
	mov ebp, esp
	sub esp, 12
	mov dword [ebp-4], 5
	mov dword [ebp-8], 7
	mov dword [ebp-12], 1
	mov dword [ebp-8], 1
__l0:
	mov eax, dword [ebp-8]
	cmp eax, dword [ebp-4]
	jl __l4
	mov eax, 0
	jmp __l5
__l4:
	mov eax, 1
__l5:
	mov dword [__t_0], eax
	cmp eax, 0
	je __l1
	jmp __l2
__l3:
	mov eax, dword [ebp-8]
	add eax, 1
	jmp __l0
__l2:
	mov ebx, dword [ebp-12]
	imul ebx, eax
	mov dword [ebp-8], eax
	jmp __l3
__l1:
	push ebx
	push __t_3
	mov [__t_1], eax
	mov [__t_2], ebx
	mov [ebp-12], ebx
	call printf
	mov dword [__t_4], eax
	add esp, 8
	mov eax, 1
	mov esp, ebp
	pop ebp
	ret
section	.data
	__t_0	dd	0
	__t_1	dd	0
	__t_2	dd	0
	__t_4	dd	0
	__t_3:	db	`%d`, 0
