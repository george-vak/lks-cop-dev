import argparse
import subprocess
import re


def clean_cow_output(output):
    return re.sub(r'(\n\s*)\w+(\s+\|\|)', lambda m: m.group(1) + ' ' * len(m.group(2).strip()) + m.group(2), output)


def list_cows():
    command = ["cowsay", "-l"]
    result = subprocess.run(command, capture_output=True, text=True)
    cow_list = result.stdout.split("\n")[1:]
    cows = []
    for line in cow_list:
        cows.extend(line.strip().split())
    return cows


def generate_cow_speech(message, cowfile=None, eyes='oo', tongue='  '):
    command = ["cowsay", message, "-e", eyes, "-T", tongue]
    if cowfile:
        command.extend(["-f", cowfile])
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout


def pad_cow(lines, target_height):
    padding = target_height - len(lines)
    return [' ' * len(lines[0])] * padding + lines if padding > 0 else lines



parser = argparse.ArgumentParser(description='Two cows talking with original cowsay output')

available_cows = list_cows()

parser.add_argument('message1', help='Message for the first cow')
parser.add_argument('message2', help='Message for the second cow')
parser.add_argument('-e', '--eyes', default='oo', help='Eyes for the first cow')
parser.add_argument('-f', '--cowfile', default='default', choices=available_cows, help='Cow type for the first cow')
parser.add_argument('-t', '--tongue', default='  ', help='Tongue for the first cow')

parser.add_argument('-E', '--eyes2', default='oo', help='Eyes for the second cow')
parser.add_argument('-N', '--cowfile2', default='default', choices=available_cows,
                    help='Cow type for the second cow')
parser.add_argument('-T', '--tongue2', default='  ', help='Tongue for the second cow')

args = parser.parse_args()

cow1_speech = generate_cow_speech(args.message1, args.cowfile, args.eyes, args.tongue)
cow2_speech = generate_cow_speech(args.message2, args.cowfile2, args.eyes2, args.tongue2)

cow1_speech = clean_cow_output(cow1_speech)
cow2_speech = clean_cow_output(cow2_speech)

lines1 = cow1_speech.strip().split('\n')
lines2 = cow2_speech.strip().split('\n')

max_height = max(len(lines1), len(lines2))
max_width1 = max(len(line) for line in lines1)

padded_lines1 = pad_cow(lines1, max_height)
padded_lines2 = pad_cow(lines2, max_height)

result = ''
for line1, line2 in zip(padded_lines1, padded_lines2):
    result += f"{line1.ljust(max_width1)}    {line2}\n"

print(result.strip())

