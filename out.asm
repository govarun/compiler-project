extern printf
extern scanf
extern malloc
extern free
section .text
	global main
main:
	push ebp
	mov ebp, esp
	sub esp, 84
	mov dword [ebp-4], 0
	mov dword [ebp-4], 0
__l0:
	mov eax, dword [ebp-4]
	cmp eax, 10
	jl __l18
	mov eax, 0
	jmp __l19
__l18:
	mov eax, 1
__l19:
	mov dword [ebp-8], eax
	cmp eax, 0
	je __l1
	jmp __l2
__l3:
	mov eax, dword [ebp-4]
	mov dword [ebp-4], eax
	mov dword [ebp-12], eax
	inc eax
	mov dword [ebp-4], eax
	jmp __l0
__l2:
	mov eax, dword [ebp-4]
	mov ebx, eax
	imul ebx, 4
	mov dword [ebp-40], eax
	mov ecx, dword [val_0]
	mov dword [ebp-48], ecx
	add ecx, ebx
	mov dword [ebp-44], ebx
	mov ebx, [ecx] 
	mov dword [ebp-56], ebx
	mov dword [ebp-60], 1
	neg dword [ebp-60]
	mov ebx, dword [ebp-60]
	mov [ecx], ebx
	mov dword [ebp-4], eax
	mov dword [ebp-60], ebx
	mov dword [ebp-52], ecx
	jmp __l3
__l1:
	push 9
	call calc_odd
	mov dword [ebp-16], eax
	add esp, 4
	push __t_9
	call printf
	mov dword [ebp-20], eax
	add esp, 4
	mov dword [ebp-4], 0
__l4:
	mov eax, dword [ebp-4]
	cmp eax, 10
	jl __l20
	mov eax, 0
	jmp __l21
__l20:
	mov eax, 1
__l21:
	mov dword [ebp-24], eax
	cmp eax, 0
	je __l5
	jmp __l6
__l7:
	mov eax, dword [ebp-4]
	mov dword [ebp-4], eax
	mov dword [ebp-28], eax
	inc eax
	mov dword [ebp-4], eax
	jmp __l4
__l6:
	mov eax, dword [ebp-4]
	mov ebx, eax
	imul ebx, 4
	mov dword [ebp-64], eax
	mov ecx, dword [val_0]
	mov dword [ebp-72], ecx
	add ecx, ebx
	mov dword [ebp-68], ebx
	mov ebx, [ecx] 
	mov dword [ebp-80], ebx
	push dword [ebp-80]
	push eax
	push __t_13
	mov dword [ebp-4], eax
	mov dword [ebp-76], ecx
	call printf
	mov dword [ebp-84], eax
	add esp, 12
	jmp __l7
__l5:
	push __t_20
	call printf
	mov dword [ebp-32], eax
	add esp, 4
	push 8
	call calc_even
	mov dword [ebp-36], eax
	add esp, 4
	mov eax, 0
	mov esp, ebp
	pop ebp
	ret
calc_odd:
	push ebp
	mov ebp, esp
	sub esp, 100
	push dword [ebp+8]
	push __t_23
	call printf
	mov dword [ebp-4], eax
	add esp, 8
	mov eax, dword [ebp+8]
	mov ebx, 2
	cdq
	idiv ebx
	mov dword [ebp-8], edx
	cmp edx, 0
	je __l22
	mov edx, 0
	jmp __l23
__l22:
	mov edx, 1
__l23:
	mov dword [ebp-12], edx
	cmp edx, 0
	je __l8
	mov dword [ebp-16], 1
	neg dword [ebp-16]
	mov eax, dword [ebp-16]
	mov esp, ebp
	pop ebp
	ret
__l8:
	mov eax, dword [ebp+8]
	mov ebx, eax
	imul ebx, 4
	mov dword [ebp-20], eax
	mov ecx, dword [val_0]
	mov dword [ebp-28], ecx
	add ecx, ebx
	mov dword [ebp-24], ebx
	mov ebx, [ecx] 
	mov dword [ebp-36], ebx
	mov dword [ebp-40], 1
	neg dword [ebp-40]
	mov ebx, dword [ebp-36]
	cmp ebx, dword [ebp-40]
	jne __l24
	mov ebx, 0
	jmp __l25
__l24:
	mov ebx, 1
__l25:
	mov dword [ebp-44], ebx
	cmp ebx, 0
	mov dword [ebp+8], eax
	mov dword [ebp-32], ecx
	je __l10
	mov eax, dword [ebp+8]
	mov ebx, eax
	imul ebx, 4
	mov dword [ebp-48], eax
	mov ecx, dword [val_0]
	mov dword [ebp-56], ecx
	add ecx, ebx
	mov dword [ebp-52], ebx
	mov ebx, [ecx] 
	mov dword [ebp-64], ebx
	mov dword [ebp+8], eax
	mov eax, dword [ebp-64]
	mov esp, ebp
	pop ebp
	ret
	mov dword [ebp-60], ecx
__l10:
	mov eax, dword [ebp+8]
	mov ebx, eax
	imul ebx, 4
	mov dword [ebp-68], eax
	mov ecx, dword [val_0]
	mov dword [ebp-76], ecx
	add ecx, ebx
	mov dword [ebp-72], ebx
	mov ebx, [ecx] 
	mov dword [ebp-84], ebx
	mov ebx, 2
	imul ebx, eax
	mov dword [ebp+8], eax
	sub eax, 1
	push eax
	mov dword [ebp-92], eax
	mov dword [ebp-88], ebx
	mov dword [ebp-80], ecx
	call calc_even
	mov dword [ebp-96], eax
	add esp, 4
	mov eax, dword [ebp-88]
	add eax, dword [ebp-96]
	mov dword [ebp-100], eax
	mov eax, dword [ebp-80]
	mov ebx, dword [ebp-100]
	mov [eax], ebx
	mov dword [ebp-80], eax
	mov eax, dword [ebp-84]
	mov esp, ebp
	pop ebp
	ret
calc_even:
	push ebp
	mov ebp, esp
	sub esp, 120
	push dword [ebp+8]
	push __t_49
	call printf
	mov dword [ebp-4], eax
	add esp, 8
	mov eax, dword [ebp+8]
	mov ebx, 2
	cdq
	idiv ebx
	mov dword [ebp-8], edx
	cmp edx, 0
	je __l12
	mov dword [ebp-12], 1
	neg dword [ebp-12]
	mov eax, dword [ebp-12]
	mov esp, ebp
	pop ebp
	ret
__l12:
	mov eax, dword [ebp+8]
	cmp eax, 0
	je __l26
	mov eax, 0
	jmp __l27
__l26:
	mov eax, 1
__l27:
	mov dword [ebp-16], eax
	cmp eax, 0
	je __l14
	mov eax, dword [ebp+8]
	mov ebx, eax
	imul ebx, 4
	mov dword [ebp-20], eax
	mov ecx, dword [val_0]
	mov dword [ebp-28], ecx
	add ecx, ebx
	mov dword [ebp-24], ebx
	mov ebx, [ecx] 
	mov dword [ebp-36], ebx
	mov dword [ecx], 0
	mov dword [ebp+8], eax
	mov eax, dword [ebp-36]
	mov esp, ebp
	pop ebp
	ret
	mov dword [ebp-32], ecx
__l14:
	mov eax, dword [ebp+8]
	mov ebx, eax
	imul ebx, 4
	mov dword [ebp-40], eax
	mov ecx, dword [val_0]
	mov dword [ebp-48], ecx
	add ecx, ebx
	mov dword [ebp-44], ebx
	mov ebx, [ecx] 
	mov dword [ebp-56], ebx
	mov dword [ebp-60], 1
	neg dword [ebp-60]
	mov ebx, dword [ebp-56]
	cmp ebx, dword [ebp-60]
	jne __l28
	mov ebx, 0
	jmp __l29
__l28:
	mov ebx, 1
__l29:
	mov dword [ebp-64], ebx
	cmp ebx, 0
	mov dword [ebp+8], eax
	mov dword [ebp-52], ecx
	je __l16
	mov eax, dword [ebp+8]
	mov ebx, eax
	imul ebx, 4
	mov dword [ebp-68], eax
	mov ecx, dword [val_0]
	mov dword [ebp-76], ecx
	add ecx, ebx
	mov dword [ebp-72], ebx
	mov ebx, [ecx] 
	mov dword [ebp-84], ebx
	mov dword [ebp+8], eax
	mov eax, dword [ebp-84]
	mov esp, ebp
	pop ebp
	ret
	mov dword [ebp-80], ecx
__l16:
	mov eax, dword [ebp+8]
	mov ebx, eax
	imul ebx, 4
	mov dword [ebp-88], eax
	mov ecx, dword [val_0]
	mov dword [ebp-96], ecx
	add ecx, ebx
	mov dword [ebp-92], ebx
	mov ebx, [ecx] 
	mov dword [ebp-104], ebx
	mov dword [ebp+8], eax
	mov ebx, 2
	cdq
	idiv ebx
	mov ebx, dword [ebp+8]
	sub ebx, 1
	push ebx
	mov dword [ebp-108], eax
	mov dword [ebp-112], ebx
	mov dword [ebp-100], ecx
	call calc_odd
	mov dword [ebp-116], eax
	add esp, 4
	mov eax, dword [ebp-108]
	add eax, dword [ebp-116]
	mov dword [ebp-120], eax
	mov eax, dword [ebp-100]
	mov ebx, dword [ebp-120]
	mov [eax], ebx
	mov dword [ebp-100], eax
	mov eax, dword [ebp-104]
	mov esp, ebp
	pop ebp
	ret
section	.data
	val_0	dd	0
	__t_9:	db	`\n`, 0
	__t_13:	db	`i = %d, val = %d\n`, 0
	__t_20:	db	`\n`, 0
	__t_23:	db	`n = %d\n`, 0
	__t_49:	db	`n = %d\n`, 0
