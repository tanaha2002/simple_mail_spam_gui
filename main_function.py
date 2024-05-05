import re

def needs_review(message, dictionary, banned_words):
    if re.search(r'\b[Ii]\s+[Ll][Oo][Vv][Ee]\s+[Yy][Oo][Uu]\b', message):
        return True


    misspelled_words = 0
    for word in message.split():
        if word.lower() not in dictionary:
            misspelled_words += 1
            if misspelled_words >= 3:
                return True


    for banned_word in banned_words:
        if banned_word in message.lower():
            return True

    return False


def read_banned_words(filename):
    try:
        with open(filename, "r") as file:
            m = int(file.readline())
            banned_words = set(file.readline().strip() for _ in range(m))
        return banned_words
    except Exception as e:
        return set()


def read_dictionary(filename):
    try:
        with open(filename, "r",encoding='utf-8') as file:
            n = int(file.readline())
            dictionary = set(file.readline().strip() for _ in range(n))
        return dictionary
    except Exception as e:
        return set()


def read_messages(filename):
    try:
        with open(filename, "r") as file:
            t = int(file.readline())
            messages = []
            for _ in range(t):
                send_time = file.readline().strip()
                w = int(file.readline())
                message = file.readline().strip()
                messages.append((send_time, message))
        return messages
    except Exception as e:
        return []


# dictionary = read_dictionary("dictionary.txt")
# banned_words = read_banned_words("banned_words.txt")
# messages = read_messages("messages.txt")


# for i, (send_time, message) in enumerate(messages, 1):
#     match = re.match(r'(\d+):(\d+)', send_time)
#     if match:
#         hour, minute = map(int, match.groups())
#     if hour > 12:
#         send_time = f"{hour-12}:{minute:02d} CH"
#     else:
#         send_time = f"{hour}:{minute:02d} Sáng"




#     if 1 <= hour <= 6 and needs_review(message, dictionary, banned_words):
#         print(f"message  #{i}: FAILED TO SEND.")
#     else:
#         print(f"message  #{i}: {message.capitalize()}")


#     print()