#Stripping the markodown fence off the final code
def strip_code(code: str) -> str:
    code = code.strip()
    if code.startswith("```"):
        lines = code.split("\n")
        lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        code = "\n".join(lines)
    return code