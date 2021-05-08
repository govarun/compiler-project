extern printf
extern scanf
extern malloc
extern free
section .text
	global main
main:
	push ebp
	mov ebp, esp
	sub esp, 136
	mov eax, 500
	imul eax, 4
	push eax
	call malloc
	add esp, 4
	mov [ebp-4], eax
	mov dword [ebp-8], 0
	mov dword [ebp-12], 0
	mov dword [ebp-16], 499
__l0:
	mov eax, dword [ebp-8]
	cmp eax, 500
	jl __l10
	mov eax, 0
	jmp __l11
__l10:
	mov eax, 1
__l11:
	mov dword [ebp-28], eax
	cmp eax, 0
	je __l1
	jmp __l2
__l3:
	mov eax, dword [ebp-8]
	mov dword [ebp-32], eax
	mov dword [ebp-8], eax
	inc eax
	mov dword [ebp-8], eax
	jmp __l0
__l2:
	mov eax, dword [ebp-8]
	mov ebx, eax
	imul ebx, 4
	mov dword [ebp-44], eax
	mov ecx, dword [ebp-4]
	mov dword [ebp-52], ecx
	add ecx, ebx
	mov dword [ebp-48], ebx
	mov ebx, [ecx] 
	mov dword [ebp-60], ebx
	mov dword [ebp-8], eax
	add eax, 1
	mov [ecx], eax
	mov dword [ebp-64], eax
	mov dword [ebp-56], ecx
	jmp __l3
__l1:
__l4:
	mov eax, dword [ebp-12]
	cmp eax, dword [ebp-16]
	jle __l12
	mov eax, 0
	jmp __l13
__l12:
	mov eax, 1
__l13:
	mov dword [ebp-36], eax
	cmp eax, 0
	je __l5
	mov eax, dword [ebp-12]
	add eax, dword [ebp-16]
	mov dword [ebp-68], eax
	mov ebx, 2
	cdq
	idiv ebx
	push eax
	push __t_11
	mov dword [ebp-72], eax
	mov dword [ebp-24], eax
	call printf
	mov dword [ebp-76], eax
	add esp, 8
	mov eax, dword [ebp-24]
	mov ebx, eax
	imul ebx, 4
	mov dword [ebp-80], eax
	mov ecx, dword [ebp-4]
	mov dword [ebp-88], ecx
	add ecx, ebx
	mov dword [ebp-84], ebx
	mov ebx, [ecx] 
	mov dword [ebp-96], ebx
	mov ebx, dword [ebp-96]
	cmp ebx, 150
	je __l14
	mov ebx, 0
	jmp __l15
__l14:
	mov ebx, 1
__l15:
	mov dword [ebp-100], ebx
	cmp ebx, 0
	mov dword [ebp-24], eax
	mov dword [ebp-92], ecx
	je __l6
	mov eax, dword [ebp-24]
	push eax
	push __t_19
	mov dword [ebp-20], eax
	mov dword [ebp-24], eax
	call printf
	mov dword [ebp-136], eax
	add esp, 8
	jmp __l5
__l6:
	mov eax, dword [ebp-24]
	mov ebx, eax
	imul ebx, 4
	mov dword [ebp-104], eax
	mov ecx, dword [ebp-4]
	mov dword [ebp-112], ecx
	add ecx, ebx
	mov dword [ebp-108], ebx
	mov ebx, [ecx] 
	mov dword [ebp-120], ebx
	mov ebx, dword [ebp-120]
	cmp ebx, 150
	jg __l16
	mov ebx, 0
	jmp __l17
__l16:
	mov ebx, 1
__l17:
	mov dword [ebp-124], ebx
	cmp ebx, 0
	mov dword [ebp-24], eax
	mov dword [ebp-116], ecx
	je __l8
	mov eax, dword [ebp-24]
	sub eax, 1
	mov dword [ebp-16], eax
	mov dword [ebp-128], eax
	jmp __l9
__l8:
	mov eax, dword [ebp-24]
	add eax, 1
	mov dword [ebp-132], eax
	mov dword [ebp-12], eax
__l9:
	jmp __l4
__l5:
	push dword [ebp-20]
	push __t_29
	call printf
	mov dword [ebp-40], eax
	add esp, 8
	mov eax, 0
	mov esp, ebp
	pop ebp
	ret
section	.data
	__t_11:	db	`mid = %d\n`, 0
	__t_19:	db	`ans = %d`, 0
	__t_29:	db	`ans = %d`, 0
