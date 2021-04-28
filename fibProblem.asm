extern printf
section .text
	global main
fib:
	push ebp
	mov ebp, esp
	sub esp, 12
	mov eax, dword [ebp+8]
	mov ebx, eax
	cmp ebx, 0
	je __l5
	mov ebx, 0
	jmp __l6
__l5:
	mov ebx, 1
__l6:
	mov dword [ebp+8], eax
	mov dword [__t_0], ebx
	cmp ebx, 0
	je __l1
	mov dword [__t_1], 1
	mov dword [ebp-12], eax
	jmp __l0
__l1:
	mov eax, dword [ebp+8]
	cmp eax, 1
	je __l7
	mov eax, 0
	jmp __l8
__l7:
	mov eax, 1
__l8:
	mov dword [__t_2], eax
	cmp eax, 0
	je __l2
	mov dword [__t_1], 1
	jmp __l0
__l2:
	mov dword [__t_1], 0
__l0:
	mov eax, dword [__t_1]
	cmp eax, 0
	je __l3
	mov eax, dword [ebp+8]
	mov esp, ebp
	pop ebp
	ret
__l3:
	mov eax, dword [ebp+8]
	sub eax, 1
	push eax
	mov dword [__t_3], eax
	call fib
	mov dword [__t_4], eax
	add esp, 4
	mov eax, dword [ebp+8]
	sub eax, 2
	push eax
	mov dword [__t_5], eax
	call fib
	mov dword [__t_6], eax
	add esp, 4
	mov eax, dword [__t_4]
	add eax, dword [__t_6]
	mov dword [ebp-4], eax
	mov dword [__t_7], eax
	mov esp, ebp
	pop ebp
	ret
main:
	push ebp
	mov ebp, esp
	sub esp, 12
	mov dword [ebp-4], 5
	mov dword [ebp-8], 7
	mov dword [ebp-12], 1
	push 7
	call fib
	mov dword [__t_9], eax
	add esp, 4
	push dword [__t_9]
	push __t_8
	call printf
	mov dword [__t_10], eax
	add esp, 8
	mov eax, 1
	mov esp, ebp
	pop ebp
	ret
section	.data
	__t_0	dd	0
	__t_1	dd	0
	__t_2	dd	0
	__t_3	dd	0
	__t_4	dd	0
	__t_5	dd	0
	__t_6	dd	0
	__t_7	dd	0
	__t_9	dd	0
	__t_10	dd	0
	__t_8:	db	`%d\n`, 0
