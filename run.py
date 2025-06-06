import json


def check_capacity(max_capacity: int, guests: list) -> bool:
    events = []
    for guest in guests:
        if guest["check-out"] < guest["check-in"]:
            return False
        events.append((guest["check-in"], 1))
        events.append((guest["check-out"], -1))
    events.sort()

    current = 0
    for _, delta in events:
        current += delta
        if current > max_capacity:
            return False

    return True


if __name__ == "__main__":
    max_capacity = int(input())
    n = int(input())

    guests = []
    for _ in range(n):
        guest_json = input()
        guest_data = json.loads(guest_json)
        guests.append(guest_data)

    result = check_capacity(max_capacity, guests)
    print(result)
