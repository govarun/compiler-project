extern printf
extern scanf
extern malloc
section .text
	global main
main:
	push ebp
	mov ebp, esp
	sub esp, 64
	mov eax, 7
	shl eax, 2
	push eax
	call malloc
	add esp, 4
	mov dword [ebp-8], 0
	mov dword [ebp-8], 0
	mov dword [ebp-4], eax
__l0:
	mov eax, dword [ebp-8]
	cmp eax, 7
	jl __l6
	mov eax, 0
	jmp __l7
__l6:
	mov eax, 1
__l7:
	mov dword [ebp-12], eax
	cmp eax, 0
	je __l1
	jmp __l2
__l3:
	mov eax, dword [ebp-8]
	mov dword [ebp-16], eax
	mov dword [ebp-8], eax
	inc eax
	mov dword [ebp-8], eax
	jmp __l0
__l2:
	mov eax, dword [ebp-8]
	cmp eax, 2
	je __l8
	mov eax, 0
	jmp __l9
__l8:
	mov eax, 1
__l9:
	mov dword [ebp-20], eax
	cmp eax, 0
	je __l4
	jmp __l3
__l4:
	mov eax, dword [ebp-8]
	mov ebx, eax
	imul ebx, 4
	mov dword [ebp-24], eax
	lea ecx, [ebp-4]
	mov dword [ebp-32], ecx
	add ecx, ebx
	mov dword [ebp-28], ebx
	mov ebx, [ecx] 
	mov dword [ebp-40], ebx
	mov dword [ecx], 4
	mov ebx, eax
	imul ebx, 4
	mov dword [ebp-44], eax
	lea edx, [ebp-4]
	mov dword [ebp-52], edx
	add edx, ebx
	mov dword [ebp-48], ebx
	mov ebx, [edx] 
	mov dword [ebp-60], ebx
	push dword [ebp-60]
	push __t_8
	mov dword [ebp-8], eax
	mov dword [ebp-36], ecx
	mov dword [ebp-56], edx
	call printf
	mov dword [ebp-64], eax
	add esp, 8
	jmp __l3
__l1:
	mov eax, 0
	mov esp, ebp
	pop ebp
	ret
section	.data
	__t_8:	db	`%d `, 0
