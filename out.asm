extern printf
extern scanf
extern malloc
section .text
	global main
main:
	push ebp
	mov ebp, esp
	sub esp, 120
	mov eax, 4
	shl eax, 2
	push eax
	call malloc
	add esp, 4
	mov [ebp-4], eax
	mov dword [ebp-8], 0
	mov dword [ebp-12], 0
	mov dword [ebp-8], 0
__l0:
	mov eax, dword [ebp-8]
	cmp eax, 2
	jl __l16
	mov eax, 0
	jmp __l17
__l16:
	mov eax, 1
__l17:
	mov dword [ebp-16], eax
	cmp eax, 0
	je __l1
	jmp __l2
__l3:
	mov eax, dword [ebp-8]
	mov dword [ebp-8], eax
	mov dword [ebp-20], eax
	inc eax
	mov dword [ebp-8], eax
	jmp __l0
__l2:
	mov dword [ebp-12], 0
__l4:
	mov eax, dword [ebp-12]
	cmp eax, 2
	jl __l18
	mov eax, 0
	jmp __l19
__l18:
	mov eax, 1
__l19:
	mov dword [ebp-32], eax
	cmp eax, 0
	je __l5
	jmp __l6
__l7:
	mov eax, dword [ebp-12]
	mov dword [ebp-12], eax
	mov dword [ebp-36], eax
	inc eax
	mov dword [ebp-12], eax
	jmp __l4
__l6:
	push dword [ebp-12]
	push dword [ebp-8]
	push __t_4
	call printf
	mov dword [ebp-40], eax
	add esp, 12
	mov eax, dword [ebp-8]
	mov ebx, eax
	imul ebx, 2
	mov dword [ebp-44], eax
	mov dword [ebp-52], ebx
	add ebx, dword [ebp-12]
	mov dword [ebp-48], ebx
	imul ebx, 4
	mov ecx, dword [ebp-4]
	mov dword [ebp-60], ecx
	add ecx, ebx
	mov dword [ebp-56], ebx
	mov ebx, [ecx] 
	mov dword [ebp-68], ebx
	push ecx
	push __t_6
	mov dword [ebp-8], eax
	mov dword [ebp-64], ecx
	mov dword [ebp-72], ecx
	call scanf
	mov dword [ebp-76], eax
	add esp, 8
	jmp __l7
__l5:
	jmp __l3
__l1:
	mov dword [ebp-8], 0
__l8:
	mov eax, dword [ebp-8]
	cmp eax, 2
	jl __l20
	mov eax, 0
	jmp __l21
__l20:
	mov eax, 1
__l21:
	mov dword [ebp-24], eax
	cmp eax, 0
	je __l9
	jmp __l10
__l11:
	mov eax, dword [ebp-8]
	mov dword [ebp-28], eax
	mov dword [ebp-8], eax
	inc eax
	mov dword [ebp-8], eax
	jmp __l8
__l10:
	mov dword [ebp-12], 0
__l12:
	mov eax, dword [ebp-12]
	cmp eax, 2
	jl __l22
	mov eax, 0
	jmp __l23
__l22:
	mov eax, 1
__l23:
	mov dword [ebp-80], eax
	cmp eax, 0
	je __l13
	jmp __l14
__l15:
	mov eax, dword [ebp-12]
	mov dword [ebp-12], eax
	mov dword [ebp-84], eax
	inc eax
	mov dword [ebp-12], eax
	jmp __l12
__l14:
	mov eax, dword [ebp-8]
	mov ebx, eax
	imul ebx, 2
	mov dword [ebp-92], eax
	mov dword [ebp-100], ebx
	add ebx, dword [ebp-12]
	mov dword [ebp-96], ebx
	imul ebx, 4
	mov ecx, dword [ebp-4]
	mov dword [ebp-108], ecx
	add ecx, ebx
	mov dword [ebp-104], ebx
	mov ebx, [ecx] 
	mov dword [ebp-116], ebx
	push dword [ebp-116]
	push __t_20
	mov dword [ebp-8], eax
	mov dword [ebp-112], ecx
	call printf
	mov dword [ebp-120], eax
	add esp, 8
	jmp __l15
__l13:
	push __t_29
	call printf
	mov dword [ebp-88], eax
	add esp, 4
	jmp __l11
__l9:
	mov eax, 0
	mov esp, ebp
	pop ebp
	ret
section	.data
	__t_4:	db	`Enter the number at x[%d][%d] : `, 0
	__t_6:	db	`%d`, 0
	__t_20:	db	`%d `, 0
	__t_29:	db	`\n`, 0
