class CodeGen:
    def gen_top_headers(self):
        print("section .text")
        print("\tglobal main")
        