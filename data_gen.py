import random

firstnames = ["John", "Jane", "Michael", "Emily", "Chris", "Katie", "David", "Laura", "Robert", "Sophia",
              "James", "Olivia", "Daniel", "Emma", "Matthew", "Ava", "Andrew", "Isabella", "Ryan", "Mia"]
lastnames = ["Smith", "Johnson", "Brown", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin",
             "Lee", "Perez", "Thompson", "Clark", "Lewis", "Robinson", "Walker", "Young", "Allen", "King"]

def generate_mock_users(n=100):
    users = [
        {"username": "h_narula", "firstname": "hemant", "lastname": "narula"},
        {"username": "john123", "firstname": "John", "lastname": "Doe"},
        {"username": "jdoe", "firstname": "Jonny", "lastname": "narual"},
        {"username": "hemant2324", "firstname": "hemant", "lastname": "Kumar"},
        {"username": "doej", "firstname": "Doe", "lastname": "John"},
    ]

    for i in range(n - len(users)):
        fname = random.choice(firstnames)
        lname = random.choice(lastnames)
        num = random.randint(1, 9999)
        uname_patterns = [
            f"{fname.lower()}{num}",
            f"{lname.lower()}{num}",
            f"{fname[0].lower()}{lname.lower()}{num}",
            f"{fname.lower()}_{lname.lower()}",
            f"{fname.lower()}.{lname.lower()}{num}",
        ]
        username = random.choice(uname_patterns)
        users.append({
            "username": username,
            "firstname": fname,
            "lastname": lname
        })

    with open("mock_users.txt", "w") as f:
        for user in users:
            line = f"username: {user['username']}, firstname: {user['firstname']}, lastname: {user['lastname']}\n"
            f.write(line)

    return users