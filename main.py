import re
import math

def calculate_entropy(user_password):
    charsets = {
        r'[a-z]': 26,
        r'[A-Z]': 26,
        r'\d': 10,
        r'[!@#$%^&*(),.?":{}|<>]': len('!@#$%^&*(),.?":{}|<>')
    }
    
    charset_size = sum(size for pattern, size in charsets.items() if re.search(pattern, user_password))

    return len(user_password) * math.log2(charset_size) if charset_size > 0 else 0

def evaluate_password(user_password, blacklisted_passwords, pets_names, names_list):
    if user_password in blacklisted_passwords:
        print("Password is blacklisted. It's too weak.")
        return [], 0, 0

    pets_names_regex = re.compile(r'(?:' + '|'.join(map(re.escape, pets_names)) + r')', re.IGNORECASE)
    person_name_regex = re.compile(r'(?:' + '|'.join(map(re.escape, names_list)) + r')', re.IGNORECASE)

    is_long = len(user_password) >= 12
    has_digit = bool(re.search(r'\d', user_password))
    has_special_char = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', user_password))
    has_uppercase = bool(re.search(r'[A-Z]', user_password))
    has_lowercase = bool(re.search(r'[a-z]', user_password))

    contain_pet_name = bool(pets_names_regex.search(user_password))
    contain_person_name = bool(person_name_regex.search(user_password))

    pet_name_substring_tolerance = len(user_password) <= 5 and contain_pet_name
    person_name_substring_tolerance = len(user_password) <= 5 and contain_person_name

    score = 0

    conditions = {
        'is_long': 2,
        'has_digit': 1,
        'has_special_char': 2,
        'has_uppercase_and_lowercase': 2,
        'contain_pet_name': -1,
        'contain_person_name': -1
    }

    score += conditions['is_long'] if is_long else 0
    score += conditions['has_digit'] if has_digit else 0
    score += conditions['has_special_char'] if has_special_char else 0
    score += conditions['has_uppercase_and_lowercase'] if (has_uppercase and has_lowercase) else 0
    score += conditions['contain_pet_name'] if contain_pet_name and not pet_name_substring_tolerance else 0
    score += conditions['contain_person_name'] if contain_person_name and not person_name_substring_tolerance else 0

    pass_infos = {
        "Password length": "Password is sufficiently long." if is_long else "Password is too short.",
        "Digit check": "Password contains at least one digit." if has_digit else "Password should contain a digit.",
        "Special character check": "Password contains a special character." if has_special_char else "Password should contain a special character.",
        "Case variation": "Password contains both uppercase and lowercase letters." if has_uppercase and has_lowercase else "Password should have both uppercase and lowercase letters.",
        "Pet name check": "Password doesn't contain a pet's name." if not contain_pet_name else "Password contains a pet's name, not recommended.",
        "Person name check": "Password doesn't contain a person's name." if not contain_person_name else "Password contains a person's name, not recommended."
    }

    pass_informations = [f"+ {key}: {value}" for key, value in pass_infos.items()]

    entropy = calculate_entropy(user_password)

    return pass_informations, score, entropy

file_paths = [
    'utils/pass_list.txt', 
    'utils/pets_names.txt', 
    'utils/names_list.txt'
]

blacklisted_passwords, pets_names, names_list = [open(file).read().splitlines() for file in file_paths]

print("Enter your password:")
user_password = input("> ").strip()

pass_informations, score, entropy = evaluate_password(user_password, blacklisted_passwords, pets_names, names_list)

print("\n".join(pass_informations))
print(f"Password score: {score}/7")
print(f"Password entropy: {entropy:.2f} bits")