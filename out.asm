extern printf
extern scanf
extern malloc
section .text
	global main
binsearch:
	push ebp
	mov ebp, esp
	sub esp, 56
	mov dword [ebp-4], 1
	mov eax, dword [ebp-4]
	imul eax, 4
	mov ebx, dword [ebp+64]
	mov dword [ebp-12], ebx
	add ebx, eax
	mov dword [ebp-8], eax
	mov eax, [ebx] 
	mov dword [ebp-20], eax
	mov eax, dword [ebp-20]
	mov dword [ebp-24], eax
	mov dword [ebp-20], eax
	mov eax, 0
	mov dword [ebp-24], eax
	mov dword [ebp-16], ebx
__l0:
	mov eax, dword [ebp-24]
	cmp eax, 10
	jl __l8
	mov eax, 0
	jmp __l9
__l8:
	mov eax, 1
__l9:
	mov dword [ebp-28], eax
	cmp eax, 0
	je __l1
	jmp __l2
__l3:
	mov eax, dword [ebp-24]
	mov dword [ebp-32], eax
	mov dword [ebp-24], eax
	inc eax
	mov dword [ebp-24], eax
	jmp __l0
__l2:
	mov eax, dword [ebp-24]
	mov ebx, eax
	imul ebx, 4
	mov dword [ebp-36], eax
	mov ecx, dword [ebp+64]
	mov dword [ebp-44], ecx
	add ecx, ebx
	mov dword [ebp-40], ebx
	mov ebx, [ecx] 
	mov dword [ebp-52], ebx
	push dword [ebp-52]
	push __t_7
	mov dword [ebp-24], eax
	mov dword [ebp-48], ecx
	call printf
	mov dword [ebp-56], eax
	add esp, 8
	jmp __l3
__l1:
	mov eax, 1
	mov esp, ebp
	pop ebp
	ret
main:
	push ebp
	mov ebp, esp
	sub esp, 40
	mov eax, 10
	shl eax, 2
	push eax
	call malloc
	add esp, 4
	mov [ebp-4], eax
	mov dword [ebp-8], 0
__l4:
	mov eax, dword [ebp-8]
	cmp eax, 10
	jl __l10
	mov eax, 0
	jmp __l11
__l10:
	mov eax, 1
__l11:
	mov dword [ebp-12], eax
	cmp eax, 0
	je __l5
	jmp __l6
__l7:
	mov eax, dword [ebp-8]
	mov dword [ebp-8], eax
	mov dword [ebp-16], eax
	inc eax
	mov dword [ebp-8], eax
	jmp __l4
__l6:
	mov eax, dword [ebp-8]
	mov ebx, eax
	imul ebx, 4
	mov dword [ebp-24], eax
	mov ecx, dword [ebp-4]
	mov dword [ebp-32], ecx
	add ecx, ebx
	mov dword [ebp-28], ebx
	mov ebx, [ecx] 
	mov dword [ebp-40], ebx
	mov [ecx], eax
	mov dword [ebp-8], eax
	mov dword [ebp-36], ecx
	jmp __l7
__l5:
	push dword [ebp-4]
	call binsearch
	mov dword [ebp-20], eax
	add esp, 4
	mov eax, 0
	mov esp, ebp
	pop ebp
	ret
section	.data
	__t_7:	db	`%d\n`, 0
