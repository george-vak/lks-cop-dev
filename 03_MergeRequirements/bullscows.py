import random
import sys
import urllib

from typing import List, Tuple, Callable

def bullscows(guess: str, secret: str) -> Tuple[int, int]:
    bulls = sum(g == s for g, s in zip(guess, secret))
    cows = sum(min(guess.count(c), secret.count(c)) for c in set(guess)) - bulls
    return bulls, cows

def gameplay(ask: Callable[[str, List[str]], str], inform: Callable[[str, int, int], None], words: List[str]) -> int:
    secret = random.choice(words)
    atts = 0

    while True:
        guess = ask("Введите слово: ")
        atts += 1

        bulls, cows = bullscows(guess, secret)
        inform("Быки: {}, Коровы: {}", bulls, cows)

        if guess == secret:
            return atts

def ask(prompt: str, valid: List[str] = None) -> str:
    return input(prompt)

def inform(form_str: str, bulls: int, cows: int) -> None:
    print(form_str.format(bulls, cows))

def load_words(source: str, length: int = 5) -> List[str]:
    if source.startswith(("http://", "https://")):
        with urllib.request.urlopen(source) as f:
            words = f.read().decode().splitlines()
    else:
        with open(source, "r", encoding="utf-8") as f:
            words = f.read().splitlines()

    return [word for word in words if len(word) == length]


def main():
    if len(sys.argv) < 2:
        sys.exit(1)
    dictionary = sys.argv[1]
    length = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    words = load_words(dictionary, length)
    if not words:
        print(f"Нет слов длиной {length} в словаре.")
        sys.exit(1)

    attempts = gameplay(ask, inform, words)
    print(f"Вы угадали слово за {attempts} попыток!")

if __name__ == "__main__":
    main()
