extern printf
extern scanf
extern malloc
section .text
	global main
binsearch:
	push ebp
	mov ebp, esp
	sub esp, 0
	mov eax, 1
	mov esp, ebp
	pop ebp
	ret
main:
	push ebp
	mov ebp, esp
	sub esp, 28
	mov eax, 2
	imul eax, 4
	push eax
	call malloc
	add esp, 4
	mov [ebp-4], eax
	mov dword [ebp-8], 0
	mov eax, dword [ebp-8]
	imul eax, 4
	mov ebx, dword [ebp-4]
	mov dword [ebp-16], ebx
	add ebx, eax
	mov dword [ebp-12], eax
	mov eax, [ebx] 
	mov dword [ebp-24], eax
	mov dword [ebx], 2
	push dword [ebp-4]
	mov dword [ebp-20], ebx
	call binsearch
	mov dword [ebp-28], eax
	add esp, 4
	mov eax, 0
	mov esp, ebp
	pop ebp
	ret
section	.data
