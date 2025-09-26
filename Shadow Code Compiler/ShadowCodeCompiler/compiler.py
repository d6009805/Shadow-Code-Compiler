import sys
import re
import generate_file


def main():
	instance = Compiler()
	if len(sys.argv) > 1:
		try:
			open(sys.argv[1])
		except FileNotFoundError:
			print(f"File '{sys.argv[1]}' not found")
			quit(1234)
		if len(sys.argv) > 2:
			instance.compile_code(sys.argv[1], sys.argv[2])
		else:
			instance.compile_code(sys.argv[1])
	else:
		print("compiler use for python file: python compiler.py <file> <separator>")
		print(r"compiler use for batch file: (path)\compiler <file> <separator>")
		print("use '/n' for newline separator")


class Compiler:
	binary_op = ["+", "-", "*", "/"]
	comparison_op = ["<", ">", "=="]

	def __init__(self):
		self.i = 1
		self.error_raised = 0
		self.task_counter = 0
		self.sep = ""
		self.line = ""
		self.cmd = ""
		self.compiled_code = ""
		self.args = []
		self.var_list = []
		self.task_list = []

	@staticmethod
	def is_number(num):
		return re.match(r"^-?\d+(\.\d+)?$", num) is not None

	@staticmethod
	def combine_strs(tokens):
		if not tokens:
			return []
		line = " ".join(tokens)
		out = []
		cur = []
		in_quotes = False
		escape = False
		i = 0
		while i < len(line):
			ch = line[i]
			if in_quotes:
				if escape:
					cur.append(ch)
					escape = False
				elif ch == "\\":
					escape = True
				elif ch == '"':
					out.append("".join(cur))
					cur = []
					in_quotes = False
				else:
					cur.append(ch)
			else:
				if ch.isspace():
					if cur:
						out.append("".join(cur))
						cur = []
				elif ch == '"':
					in_quotes = True
					escape = False
				else:
					cur.append(ch)
			i += 1
		if cur:
			out.append("".join(cur))
		return out

	def var_modify(self, var):
		if self.check_var_exists(var):
			self.sasm(f"ramwrite *{var}")

	def check_var_exists(self, var):
		if not var in self.var_list:
			self.throw(f"Variable {var} is not defined")
			return 0
		else:
			return 1

	def sasm(self, code):
		if self.sep == "/n":
			self.compiled_code += (str(code)) + "\n"
		else:
			self.compiled_code += (str(code)) + str(self.sep)

	def throw(self, desc="Error occurred", extra=None, include_line=True):
		if not self.error_raised: print("Compiler messages:\n")
		self.error_raised = 1
		print(f"Error: {desc}")
		if extra:
			print(extra)
		if include_line:
			print(f"line {self.i + 1}: {self.line}", end="\n\n")
		return True

	def min_args(self, m, extra=None):
		if len(self.args) < m:
			if extra:
				self.throw(f"Got {len(self.args)} arguments for function '{self.cmd}'",
						   f"Minimum arguments is {m}: {", ".join(extra)}")
			else:
				self.throw(f"Got {len(self.args)} arguments for function '{self.cmd}'", f"Minimum arguments is {m}")
			return False
		return True

	def compile_line(self, line):
		if not line:
			return
		cmd, *args = line.split(" ")
		cmd = cmd.strip()
		args = self.combine_strs(args)
		for i, arg in enumerate(args):
			args[i] = arg.strip()
		self.cmd, self.args = cmd, args
		if cmd == "@no_exit":
			return
		elif cmd == "task":
			if args[0] in self.task_list:
				self.throw(f"Task '{args[0]}' already exists")
			self.sasm(f".{args[0]}")
			self.task_list.append(args[0])
		elif cmd == "var":
			if not args[0] in self.var_list:
				if len(args) == 1:
					self.var_list.append(args[0])
					self.sasm(f"push")
					self.sasm(f"${args[0]}")
				else:
					self.var_list.append(args[0])
					self.sasm(f"push {args[1]}")
					self.sasm(f"${args[0]}")
			else:
				if len(args) > 1:
					self.sasm(f"push {args[1]}")
					self.sasm(f"ramwrite *{args[0]}")
				else:
					self.throw(f"Variable '{args[0]}' has already been declared")
		elif cmd == "print":
			self.sasm(f"push {args[0]}")
			self.sasm(f"out")
		elif cmd == "eval":
			self.sasm(f"push {args[0]}")
			self.sasm(f"push {args[2]}")
			if args[1] == "+":
				self.sasm("add")
			elif args[1] == "-":
				self.sasm("sub")
			elif args[1] == "*":
				self.sasm("mul")
			elif args[1] == "/":
				self.sasm("div")
			self.var_modify(args[3])
		elif cmd == "syscall":
			self.sasm(f"syscall {args[0]}")
		elif cmd == "read":
			self.sasm("scan")
			if not args[0] == "_":
				self.var_modify(args[0])
		elif cmd == "sasm":
			self.sasm(str(args[0]))
		elif cmd == "return":
			if len(args) == 0:
				self.sasm("ret")
			else:
				self.sasm(f"push {args[0]}")
				self.sasm(f"$return_value")
				self.sasm("ret")
		elif cmd == "exit":
			self.sasm("exit")
		elif cmd == "call":
			self.sasm(f"call {args[0]}")
		elif cmd == "user_wait":
			self.sasm("push press enter to continue")
			self.sasm("out")
			self.sasm("scan")
		elif cmd == "sleep":
			self.sasm(f"sleep {args[0]}")
		elif cmd == "is":
			self.sasm(f"push {args[0]}")
			self.sasm(f"push {args[2]}")
			if args[1] == "==":
				self.sasm(f"strcmp")
				self.var_modify(args[3])
			elif args[1] == ">":
				self.sasm(f"sub")
				self.sasm("cmpz")
				self.sasm("push 1")
				self.sasm("strcmp")
				self.var_modify(args[3])
			elif args[1] == "<":
				self.sasm(f"sub")
				self.sasm("cmpz")
				self.sasm("push -1")
				self.sasm("strcmp")
				self.var_modify(args[3])
		elif cmd == "callif":
			self.sasm(f"push {args[0]}")
			self.sasm(f"push {args[1]}")
			self.sasm("strcmp")
			self.sasm(f"cg {args[2]}")


		else:
			self.throw(f"Function '{cmd}' does not exist")

	def check_line(self, line):
		if "|" in line:
			self.throw("Illegal Character '|'")
		cmd, *args = line.split(" ")
		args = self.combine_strs(args)
		cmd = cmd.strip()
		self.cmd, self.args = cmd, args
		if cmd == "task":
			self.min_args(1)
		elif cmd == "var":
			self.min_args(1)
			if " " in args[0]:
				self.throw(f"Variable '{args[0]}' includes spaces which are not allowed")
		elif cmd == "eval":
			if self.min_args(4, ["num1", "arithmetic_operator", "num2", "store_location"]):
				if not self.is_number(args[0]) and not args[0].startswith("$"):
					self.throw(f"Incorrect type '{args[0]}' for number 1 in 'eval' function")
				if not self.is_number(args[2]) and not args[2].startswith("$"):
					self.throw(f"Incorrect type '{args[2]}' for number 2 in 'eval' function")
				if not args[1] in Compiler.binary_op:
					self.throw(f"Incorrect type '{args[1]}' for operation in 'eval' function")
		elif cmd == "print":
			self.min_args(1)
		elif cmd == "read":
			self.min_args(1)
		elif cmd == "syscall":
			self.min_args(1)
		elif cmd == "sasm":
			self.min_args(1)
		elif cmd == "call":
			self.min_args(1)
		elif cmd == "sleep":
			self.min_args(1)
		elif cmd == "is":
			if self.min_args(4, ["value1", "comparison_operator", "value2", "store_location"]):
				if not args[1] in Compiler.comparison_op:
					self.throw(f"Incorrect type '{args[1]}' for operation in 'is' function")
		elif cmd == "callif":
			self.min_args(3, ["value1", "value2", "task"])

	def compile_code(self, file, sep="|"):
		self.sep = sep
		lines = []
		if sep == "/n":
			self.compiled_code = ".start\n"
		else:
			self.compiled_code = ".start" + str(sep)
		with open(file, encoding="utf-8") as f:
			try:
				for line in f:
					lines.append(line.strip("\n"))
			except UnicodeDecodeError:
				print("Error decoding file\nFile contains non-ASCII characters")
				return
		for i, line in enumerate(lines):
			self.line = line
			self.i = i
			self.check_line(line)
		if self.error_raised:
			print("Cannot compile code due to errors")
			return
		for i, line in enumerate(lines):
			self.line = line
			self.i = i
			self.compile_line(line.strip())
		if not "exit" in lines and not "@no_exit" in lines:
			self.throw("No exit statement\n", include_line=False)
		if self.error_raised:
			print("Cannot compile code due to errors")
		else:
			print("\ncode: " + self.compiled_code + "\n\nsuccessfully compiled code \ncode is available in 'out' directory with filename")
			generate_file.gen_file(file, self.compiled_code)
			generate_file.log_file(file)


if __name__ == "__main__":
	main()
