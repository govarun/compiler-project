extern printf
extern scanf
extern malloc
section .text
	global main
binsearch:
	push ebp
	mov ebp, esp
	sub esp, 20
	mov dword [ebp-4], 1
	mov eax, dword [ebp-4]
	imul eax, 4
	mov ebx, dword [ebp+8]
	mov dword [ebp-12], ebx
	add ebx, eax
	mov dword [ebp-8], eax
	mov eax, [ebx] 
	mov dword [ebp-20], eax
	mov dword [ebx], 2
	mov eax, 1
	mov esp, ebp
	pop ebp
	ret
main:
	push ebp
	mov ebp, esp
	sub esp, 8
	mov eax, 10
	imul eax, 4
	push eax
	call malloc
	add esp, 4
	mov [ebp-4], eax
	push dword [ebp-4]
	call binsearch
	mov dword [ebp-8], eax
	add esp, 4
	mov eax, 0
	mov esp, ebp
	pop ebp
	ret
section	.data
