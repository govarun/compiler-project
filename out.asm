extern printf
extern scanf
section .text
	global main
even:
	push ebp
	mov ebp, esp
	sub esp, 12
	mov eax, dword [ebp+8]
	cmp eax, 0
	je __l4
	mov eax, 0
	jmp __l5
__l4:
	mov eax, 1
__l5:
	mov dword [ebp-4], eax
	cmp eax, 0
	je __l0
	mov eax, 1
	mov esp, ebp
	pop ebp
	ret
__l0:
	mov eax, dword [ebp+8]
	sub eax, 1
	push eax
	mov dword [ebp-8], eax
	call odd
	mov dword [ebp-12], eax
	add esp, 4
	mov eax, dword [ebp-12]
	mov esp, ebp
	pop ebp
	ret
odd:
	push ebp
	mov ebp, esp
	sub esp, 12
	mov eax, dword [ebp+8]
	cmp eax, 0
	je __l6
	mov eax, 0
	jmp __l7
__l6:
	mov eax, 1
__l7:
	mov dword [ebp-4], eax
	cmp eax, 0
	je __l2
	mov eax, 0
	mov esp, ebp
	pop ebp
	ret
__l2:
	mov eax, dword [ebp+8]
	sub eax, 1
	push eax
	mov dword [ebp-8], eax
	call even
	mov dword [ebp-12], eax
	add esp, 4
	mov eax, dword [ebp-12]
	mov esp, ebp
	pop ebp
	ret
main:
	push ebp
	mov ebp, esp
	sub esp, 24
	push __t_6
	call printf
	mov dword [ebp-8], eax
	add esp, 4
	lea eax, [ebp-4]
	push eax
	push __t_8
	mov dword [ebp-12], eax
	call scanf
	mov dword [ebp-16], eax
	add esp, 8
	push dword [ebp-4]
	call even
	mov dword [ebp-20], eax
	add esp, 4
	push dword [ebp-20]
	push __t_11
	call printf
	mov dword [ebp-24], eax
	add esp, 8
	mov eax, 1
	mov esp, ebp
	pop ebp
	ret
section	.data
	__t_6:	db	`Enter number : `, 0
	__t_8:	db	`%d`, 0
	__t_11:	db	`Is the number even? %d\n`, 0
