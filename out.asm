extern printf
extern scanf
extern malloc
section .text
	global main
binary_search:
	push ebp
	mov ebp, esp
	sub esp, 80
	mov eax, dword [ebp+12]
	cmp eax, dword [ebp+16]
	jg __l10
	mov eax, 0
	jmp __l11
__l10:
	mov eax, 1
__l11:
	mov dword [ebp-8], eax
	cmp eax, 0
	je __l0
	push __t_1
	call printf
	mov dword [ebp-76], eax
	add esp, 4
	mov esp, ebp
	pop ebp
	ret
__l0:
	mov eax, dword [ebp+12]
	add eax, dword [ebp+16]
	mov dword [ebp-12], eax
	mov ebx, 2
	cdq
	idiv ebx
	mov ebx, eax
	imul ebx, 4
	mov dword [ebp-20], eax
	mov ecx, dword [ebp+8]
	mov dword [ebp-28], ecx
	add ecx, ebx
	mov dword [ebp-24], ebx
	mov ebx, [ecx] 
	mov dword [ebp-36], ebx
	mov ebx, dword [ebp-36]
	cmp ebx, dword [ebp+20]
	je __l12
	mov ebx, 0
	jmp __l13
__l12:
	mov ebx, 1
__l13:
	mov dword [ebp-40], ebx
	cmp ebx, 0
	mov dword [ebp-16], eax
	mov dword [ebp-4], eax
	mov dword [ebp-32], ecx
	je __l2
	push dword [ebp-4]
	push __t_11
	call printf
	mov dword [ebp-80], eax
	add esp, 8
	mov esp, ebp
	pop ebp
	ret
__l2:
	mov eax, dword [ebp-4]
	mov ebx, eax
	imul ebx, 4
	mov dword [ebp-44], eax
	mov ecx, dword [ebp+8]
	mov dword [ebp-52], ecx
	add ecx, ebx
	mov dword [ebp-48], ebx
	mov ebx, [ecx] 
	mov dword [ebp-60], ebx
	mov ebx, dword [ebp-60]
	cmp ebx, dword [ebp+20]
	jg __l14
	mov ebx, 0
	jmp __l15
__l14:
	mov ebx, 1
__l15:
	mov dword [ebp-64], ebx
	cmp ebx, 0
	mov dword [ebp-4], eax
	mov dword [ebp-56], ecx
	je __l4
	mov eax, dword [ebp-4]
	sub eax, 1
	push dword [ebp+20]
	push eax
	push dword [ebp+12]
	push dword [ebp+8]
	mov dword [ebp-68], eax
	call binary_search
	add esp, 16
	mov esp, ebp
	pop ebp
	ret
__l4:
	mov eax, dword [ebp-4]
	add eax, 1
	push dword [ebp+20]
	push dword [ebp+16]
	push eax
	push dword [ebp+8]
	mov dword [ebp-72], eax
	call binary_search
	add esp, 16
	mov esp, ebp
	pop ebp
	ret
main:
	push ebp
	mov ebp, esp
	sub esp, 40
	mov eax, 500
	imul eax, 4
	push eax
	call malloc
	add esp, 4
	mov [ebp-4], eax
	mov dword [ebp-8], 0
	mov dword [ebp-8], 0
__l6:
	mov eax, dword [ebp-8]
	cmp eax, 500
	jl __l16
	mov eax, 0
	jmp __l17
__l16:
	mov eax, 1
__l17:
	mov dword [ebp-12], eax
	cmp eax, 0
	je __l7
	jmp __l8
__l9:
	mov eax, dword [ebp-8]
	mov dword [ebp-8], eax
	mov dword [ebp-16], eax
	inc eax
	mov dword [ebp-8], eax
	jmp __l6
__l8:
	mov eax, dword [ebp-8]
	mov ebx, eax
	imul ebx, 4
	mov dword [ebp-20], eax
	mov ecx, dword [ebp-4]
	mov dword [ebp-28], ecx
	add ecx, ebx
	mov dword [ebp-24], ebx
	mov ebx, [ecx] 
	mov dword [ebp-36], ebx
	mov dword [ebp-8], eax
	add eax, 1
	mov [ecx], eax
	mov dword [ebp-40], eax
	mov dword [ebp-32], ecx
	jmp __l9
__l7:
	push 147
	push 499
	push 0
	push dword [ebp-4]
	call binary_search
	add esp, 16
	push 700
	push 499
	push 0
	push dword [ebp-4]
	call binary_search
	add esp, 16
	push 0
	push 499
	push 0
	push dword [ebp-4]
	call binary_search
	add esp, 16
	mov eax, 0
	mov esp, ebp
	pop ebp
	ret
section	.data
	__t_1:	db	`not present\n`, 0
	__t_11:	db	`ans = %d\n`, 0
