from athena.brain import Brain 
from athena.config import APP_NAME, VERSION


def banner():
    print("=" * 50)
    print(f"{APP_NAME} v{VERSION}")
    print("Adaptive Technology for Human Enhancement,")
    print("Navigation & Assistance")
    print("=" * 50)
    print()

def main():

    banner()
    print("Initializing Brain...")
    brain = Brain()
    print("Ready\n")
    while True:
        user =input("You > ")
        if user.lower() in {"exit", "quit"}:
            break
        response = brain.think(user)

        print(f"\nATHENA > {response}\n]")


if __name__ == "__main__":
    main()