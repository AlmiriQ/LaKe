import sys, os


class Terminal:
	def __init__(self):
		def writeFileData(file, data):
			f = open(file, "w")
			f.write(data)
			f.close()
		
		def readFileData(file):
			f = open(file, "r")
			result = f.read()
			f.close()
			return result
		
		def appendFileData(file, data):
			f = open(file, "a")
			f.write(data)
			f.close()

		self.globals = {
			"fcompile": lambda what, output, *flags: os.system(f"gcc {what} -o {output} {' '.join(list(flags))}"),
			"lcompile": lambda what, output, *flags: os.system(f"gcc {what} -c -o {output}.o {' '.join(list(flags))}") and os.system(f"ar rsc {output}.a {output}.o") and os.system(f"rm {output}.o"),
			"compile": lambda what, output, *flags: os.system(f"gcc {what} -o {output} {' '.join(list(flags))}"),
			"run": os.system,
			"write": writeFileData,
			"read": readFileData,
			"append": appendFileData,
			"lua": lambda code: os.system('lua -e "' + code.replace("\"", "\\\"") + '"')
		}

	def exeqt(self, data, *args):
		exec(data, self.globals)
		if args:
			for arg in args:
				if arg:
					if arg in self.globals:
						try:
							self.globals[arg]()
						except Exception as e:
							print(e)
							sys.exit(2)
		else:
			if "all" in self.globals:
				try:
					self.globals["all"]()
				except Exception as e:
					print(e)
					sys.exit(3)


def main():
	sys.argv = sys.argv[1:]
	data = ""
	try:
		lf = open("lakefile")
		data = lf.read()
		lf.close()
	except:
		sys.exit(1)
	term = Terminal()
	term.exeqt(data, *sys.argv)
	sys.exit(0)


if __name__ == "__main__":
	main()