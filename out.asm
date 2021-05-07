extern printf
extern scanf
extern malloc
section .text
	global main
main:
	push ebp
	mov ebp, esp
	sub esp, 64
	push 80
	call malloc
	mov dword [ebp-12], eax
	add esp, 4
	mov eax, dword [ebp-12]
	mov dword [ebp-8], 0
	mov dword [ebp-16], eax
	mov dword [ebp-4], eax
	mov dword [ebp-12], eax
__l0:
	mov eax, dword [ebp-8]
	cmp eax, 4
	jl __l8
	mov eax, 0
	jmp __l9
__l8:
	mov eax, 1
__l9:
	mov dword [ebp-20], eax
	cmp eax, 0
	je __l1
	jmp __l2
__l3:
	mov eax, dword [ebp-8]
	mov dword [ebp-8], eax
	mov dword [ebp-24], eax
	inc eax
	mov dword [ebp-8], eax
	jmp __l0
__l2:
	mov eax, dword [ebp-8]
	imul eax, 4
	mov ebx, dword [ebp-4]
	add ebx, eax
	mov dword [ebp-40], eax
	mov eax, [ebx] 
	mov dword [ebp-44], eax
	mov eax, dword [ebp-8]
	imul eax, 1000
	mov [ebx], eax
	mov dword [ebp-48], eax
	mov dword [ebp-36], ebx
	jmp __l3
__l1:
	mov dword [ebp-8], 0
__l4:
	mov eax, dword [ebp-8]
	cmp eax, 4
	jl __l10
	mov eax, 0
	jmp __l11
__l10:
	mov eax, 1
__l11:
	mov dword [ebp-28], eax
	cmp eax, 0
	je __l5
	jmp __l6
__l7:
	mov eax, dword [ebp-8]
	mov dword [ebp-8], eax
	mov dword [ebp-32], eax
	inc eax
	mov dword [ebp-8], eax
	jmp __l4
__l6:
	mov eax, dword [ebp-8]
	imul eax, 4
	mov ebx, dword [ebp-4]
	add ebx, eax
	mov dword [ebp-56], eax
	mov eax, [ebx] 
	mov dword [ebp-60], eax
	push dword [ebp-60]
	push __t_10
	mov dword [ebp-52], ebx
	call printf
	mov dword [ebp-64], eax
	add esp, 8
	jmp __l7
__l5:
	mov eax, 0
	mov esp, ebp
	pop ebp
	ret
section	.data
	__t_10:	db	`%d\n`, 0
