from athena.brain import Brain 
from athena.conversation import ConversationManager
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
    brain = Brain()
    conversation = ConversationManager()
    print("ATHENA online.\n")
    try:
        while True:
            user =input("You > ")
            if user.lower() in {"exit", "quit"}:
                conversation.shutdown(brain)
                print("\nATHENA shutting down...\n")
                break
            reply = conversation.chat(brain, user)

            print(f"\nATHENA > {reply}\n")
    except KeyboardInterrupt:
        print("\n\n ATHENA shutting down...")
    finally:
        conversation.memory.end_session()
        print("Session Ended.")


if __name__ == "__main__":
    main()