import re

pattern = r"(Failed|Accepted) (password|publickey) for (invalid user )?(\S+) from (\S+)"

with open("samples/auth.log") as f:
    for line in f:
        match = re.search(pattern, line)
        if match:
            time = line[:15]
            result = match.group(1)
            user = match.group(4)
            ip = match.group(5)
            print(time, "|", result, "| user:", user, "| ip:", ip)
