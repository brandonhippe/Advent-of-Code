import sys, platform, os, re, importlib, subprocess

class Language:
    def __init__(self, lang):
        self.lang = lang
        try:
            self.run_func = language_funcs[lang][0]
            self.discover_func = language_funcs[lang][1]
            self.exists_func = language_funcs[lang][2]
        except KeyError:
            raise ValueError(f"Language {lang} not supported")
        
    def __hash__(self) -> int:
        return self.lang.__hash__()
    
    def __repr__(self) -> str:
        return self.lang

    def run(self, year, day, verbose):
        if self.exists(year, day):
            return self.run_func(year, day, verbose)
        
        raise FileNotFoundError(f"No file found for {year} day {day}")

    def discover(self, path=os.getcwd()):
        return self.discover_func(path)

    def exists(self, year, day):
        return self.exists_func(year, day)


def run_python(year, day, verbose):
    thisDir = os.getcwd()
    parent_dir = os.path.join(os.getcwd(), str(year))

    sys.path.append(parent_dir)
    code = importlib.import_module(f"{year}_{day}")
    os.chdir(parent_dir)

    (p1, p1_elapsed), (p2, p2_elapsed) = code.main(verbose)

    os.chdir(thisDir)
    sys.path.pop()
    del(sys.modules[f"{year}_{day}"])
    del(code)

    return (p1, p1_elapsed), (p2, p2_elapsed)

def discover_python(path):
    python_scripts = []
    for file in os.walk(path):
        for f in file[2]:
            if re.search('\d+_\d+.py$', f):
                year, day = re.findall('\d+', f)
                python_scripts.append((int(year), int(day)))

    return python_scripts

def exists_python(year, day):
    return os.path.exists(f"{year}{os.sep}{year}_{day}.py")


def run_rust(year, day, verbose):
    thisDir = os.getcwd()

    os.chdir(f"{year}{os.sep}rust_{year}_{day}")
    output = subprocess.run('cargo run -r', shell=True, capture_output=True, text=True)
    os.chdir(thisDir)
    
    if not output.stdout:
        raise ValueError(f"No output from C program: {year} day {day}")

    output = output.stdout.split("\n")
    try:
        output_start = output.index("Part 1:") - 1
    except ValueError:
        raise ValueError(f"Could not find output start for rust {year} day {day}")
    output = output[output_start:]

    if verbose:
        print("\n".join(output))

    for ix in range(len(output)):
        t = re.search("\d+\.\d+", output[ix])
        if not t:
            continue
        
        p1_ix = ix
        p1_elapsed = float(t.group(0))
        after_chars = output[ix][t.end():]
        if after_chars == "ms":
            p1_elapsed /= 1000
        elif after_chars == "Âµs" or after_chars == "µs":
            p1_elapsed /= 1000000
        elif after_chars == "ns":
            p1_elapsed /= 1000000000
        elif after_chars != "s":
            raise ValueError(f"Unknown time unit {after_chars}")
        
        break
    
    p1 = ""
    for ix in range(0, p1_ix): 
        if output[ix].startswith("Part"):
            try:
                p1 = output[ix + 1].split(":")[1].strip()
            except IndexError:
                pass

            break

    for ix in range(p1_ix + 1, len(output)):
        t = re.search("\d+\.\d+", output[ix])
        if not t:
            continue
        
        p2_ix = ix
        p2_elapsed = float(t.group(0))
        after_chars = output[ix][t.end():]
        if after_chars == "ms":
            p2_elapsed /= 1000
        elif after_chars == "Âµs" or after_chars == "µs":
            p2_elapsed /= 1000000
        elif after_chars == "ns":
            p2_elapsed /= 1000000000
        elif after_chars != "s":
            raise ValueError(f"Unknown time unit {after_chars}")
        
        break
    
    p2 = ""
    for ix in range(p1_ix + 1, p2_ix):
        if output[ix].startswith("Part"):
            try:
                p2 = output[ix + 1].split(":")[1].strip()
            except IndexError:
                pass

            break

    return (p1, p1_elapsed), (p2, p2_elapsed)

def discover_rust(path):
    rust_scripts = []
    for file in os.walk(path):
        for f in file[1]:
            if re.search('^rust_\d+_\d+$', f):
                year, day = re.findall('\d+', f)
                rust_scripts.append((int(year), int(day)))

    return rust_scripts

def exists_rust(year, day):
    return os.path.exists(f"{year}{os.sep}rust_{year}_{day}")


def run_c(year, day, verbose):
    thisDir = os.getcwd()

    os.chdir(f"{year}{os.sep}C")
    exe_name = f"{year}_{day}"
    exe_slash = "/"
    if platform.system() == "Windows":
        exe_name += ".exe"
        exe_slash = "\\"
    
    subprocess.run(f"gcc {year}_{day}.c -o {exe_name} -lm", shell=True, check=True)
    output = subprocess.run(f'.{exe_slash}{exe_name}', shell=True, capture_output=True, text=True)
    os.chdir(thisDir)

    if output.stderr:
        raise ValueError(output.stderr)
    
    if not output.stdout:
        raise ValueError(f"No output from C program: {year} day {day}")
    
    output = output.stdout.split("\n")
    try:
        output_start = output.index("Part 1:") - 1
    except ValueError:
        raise ValueError(f"Could not find output start for C {year} day {day}")
    output = output[output_start:]

    if verbose:
        print("\n".join(output))

    for ix in range(len(output)):
        t = re.search("\d+\.\d+", output[ix])
        if not t:
            continue
        
        p1_ix = ix
        p1_elapsed = float(t.group(0))        
        break
    
    p1 = ""
    for ix in range(0, p1_ix): 
        if output[ix].startswith("Part"):
            try:
                p1 = output[ix + 1].split(":")[1].strip()
            except IndexError:
                pass

            break

    for ix in range(p1_ix + 1, len(output)):
        t = re.search("\d+\.\d+", output[ix])
        if not t:
            continue
        
        p2_ix = ix
        p2_elapsed = float(t.group(0))        
        break
    
    p2 = ""
    for ix in range(p1_ix + 1, p2_ix):
        if output[ix].startswith("Part"):
            try:
                p2 = output[ix + 1].split(":")[1].strip()
            except IndexError:
                pass

            break

    return (p1, p1_elapsed), (p2, p2_elapsed)

def discover_c(path):
    c_scripts = []
    for file in os.walk(path):
        for f in file[2]:
            if re.search('^\d+_\d+.c$', f):
                year, day = re.findall('\d+', f)
                c_scripts.append((int(year), int(day)))

    return c_scripts

def exists_c(year, day):
    return os.path.exists(f"{year}{os.sep}C{os.sep}{year}_{day}.c")


def get_languages():
    return list(sorted(language_funcs.keys()))

language_funcs = {
    "c": [run_c, discover_c, exists_c],
    "python": [run_python, discover_python, exists_python],
    "rust": [run_rust, discover_rust, exists_rust],
}

if __name__ == "__main__":
    Language("c").run(2021, 17, True)