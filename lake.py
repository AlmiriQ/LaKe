import sys, os, glob, itertools


class Terminal:
	def __init__(self):
		# directory scan function
		def getAllFileNames(root):
			for fn in glob.iglob(root + "*", recursive=True):
				if not (fn.startswith("/") or fn.startswith("./") or fn.startswith("~")):
					fn = "./" + fn
				if "/." in fn:
					continue
				if os.path.isdir(fn) and not fn.endswith("/"):
					fn += "/"
				if os.path.isdir(fn):
					for eve in getAllFileNames(fn):
						yield eve
				else:
					yield fn
		# get only file extension
		def onlyExtension(files, ext):
			ext = ext = { ext } if type(ext) == str else ext = set(ext)
			for file in files:
				if file.split(".")[-1] in ext:
					yield file
		# write string data to file
		def writeFileData(file, data):
			with open(file, "w") as f:
				f.write(data)
		# read string data from file
		def readFileData(file):
			with open(file, "r") as f:
				return f.read()
		# append string data to file
		def appendFileData(file, data):
			with open(file, "a") as f:
				f.write(data)
		# run C code in string
		def runCCode(code):
			with open("code.c", "w") as f:
				f.write(code)
			os.system("gcc code.c -o code.o && ./code.o && rm code.c code.o")
		# pushing functional to lakefile env
		self.globals = {
			# gcc compilation
			"fcompile": lambda what, output, *flags: os.system(f"gcc {what} -o {output} {' '.join(list(flags))}"),
			"lcompile": lambda what, output, *flags: os.system(f"gcc {what} -c -o {output}.o {' '.join(list(flags))}") and os.system(f"ar rsc {output}.a {output}.o") and os.system(f"rm {output}.o"),
			"compile": lambda what, output, *flags: os.system(f"gcc {what} -o {output} {' '.join(list(flags))}"),
			# clear
			"clear": lambda: os.system("clear"),
			# join iterators
			"chained": itertools.chain,
			# run commands
			"run": os.system, "bash": os.system, 
			"c": runCCode,
			# file functions
			"write": writeFileData, "read": readFileData, "append": appendFileData, 
			"scan": getAllFileNames, "onlyExtension": onlyExtension,
			# run lua code
			"lua": lambda code: os.system('lua -e "' + code.replace("\"", "\\\"") + '"')
		}
	
	def exeqt(self, data, *args):
		data = data.replace(" then ", " ; ")
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


# running lakefile
def main():
	sys.argv, data = sys.argv[1:], ""
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
