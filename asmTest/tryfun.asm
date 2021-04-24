section .text
	global main

fun:
	push rbp
	mov rbp, rsp

	mov [rbp - 8], rdi
	mov [rbp - 16], rsi

	mov r11, rdi
	add rsi, r11
	mov [rbp - 8], rsi
	mov rax, [rbp - 8]

	mov rsp, rbp
	pop rbp
	ret 

main:
	mov rsi, 8
	mov rdi, 4
	call fun
	ret