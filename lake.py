import sys, os, glob, itertools


class Terminal:
	def __init__(self):
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

		def onlyExtension(files, ext):
			if type(ext) == str:
				ext = { ext }
			else:
				ext = set(ext)
			for file in files:
				if file.split(".")[-1] in ext:
					yield file

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

		def runCCode(code):
			f = open("code.c", "w")
			f.write(code)
			f.close()
			os.system("gcc code.c -o code.o")
			os.system("./code.o")
			os.system("rm code.c code.o")

		self.globals = {
			"fcompile": lambda what, output, *flags: os.system(f"gcc {what} -o {output} {' '.join(list(flags))}"),
			"lcompile": lambda what, output, *flags: os.system(f"gcc {what} -c -o {output}.o {' '.join(list(flags))}") and os.system(f"ar rsc {output}.a {output}.o") and os.system(f"rm {output}.o"),
			"compile": lambda what, output, *flags: os.system(f"gcc {what} -o {output} {' '.join(list(flags))}"),
			"clear": lambda: os.system("clear"),
			"chained": itertools.chain,
			"run": os.system,
			"bash": os.system,
			"c": runCCode,
			"write": writeFileData,
			"read": readFileData,
			"append": appendFileData,
			"scan": getAllFileNames,
			"onlyExtension": onlyExtension,
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