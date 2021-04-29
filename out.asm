extern printf
extern scanf
section .text
	global main
	mov dword [x_0], 0
fib:
	push ebp
	mov ebp, esp
	sub esp, 32
	mov eax, dword [ebp+8]
	cmp eax, 1
	je __l5
	mov eax, 0
	jmp __l6
__l5:
	mov eax, 1
__l6:
	mov dword [ebp-4], eax
	cmp eax, 0
	je __l1
	mov dword [ebp-8], 1
	jmp __l0
__l1:
	mov eax, dword [ebp+8]
	cmp eax, 0
	je __l7
	mov eax, 0
	jmp __l8
__l7:
	mov eax, 1
__l8:
	mov dword [ebp-12], eax
	cmp eax, 0
	je __l2
	mov dword [ebp-8], 1
	jmp __l0
__l2:
	mov dword [ebp-8], 0
__l0:
	mov eax, dword [ebp-8]
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
	mov dword [ebp-16], eax
	call fib
	mov dword [ebp-20], eax
	add esp, 4
	mov eax, dword [ebp-20]
	mov ebx, dword [ebp+8]
	sub ebx, 2
	push ebx
	mov dword [ebp-20], eax
	mov dword [x_0], eax
	mov dword [ebp-24], ebx
	call fib
	mov dword [ebp-28], eax
	add esp, 4
	mov eax, dword [x_0]
	add eax, dword [ebp-28]
	mov dword [ebp-32], eax
	mov esp, ebp
	pop ebp
	ret
main:
	push ebp
	mov ebp, esp
	sub esp, 8
	push 6
	call fib
	mov dword [ebp-4], eax
	add esp, 4
	push dword [ebp-4]
	push __t_8
	call printf
	mov dword [ebp-8], eax
	add esp, 8
	mov eax, 1
	mov esp, ebp
	pop ebp
	ret
section	.data
	x_0	dd	0
	__t_8:	db	`%d`, 0
