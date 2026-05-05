import sys
import hmac
import hashlib
import struct
import time
import base64
import urllib.request
import urllib.error
import json

sys.setrecursionlimit(10000)


# ─────────────────────────────────────────
# PART 1: SOLUTION LOGIC
# ─────────────────────────────────────────

def power4(n):
    return n * n * n * n


def process_numbers(nums, index):
    if index == len(nums):
        return 0
    val = int(nums[index])
    contribution = power4(val) if val <= 0 else 0
    return contribution + process_numbers(nums, index + 1)


def process_test_cases(lines, idx, remaining):
    if remaining == 0:
        return

    X = int(lines[idx])
    nums = lines[idx + 1].split() if idx + 1 < len(lines) else []

    if len(nums) != X:
        print(-1)
    else:
        print(process_numbers(nums, 0))

    process_test_cases(lines, idx + 2, remaining - 1)


def main():
    data = sys.stdin.read().strip().split("\n")
    N = int(data[0])
    process_test_cases(data, 1, N)


# ─────────────────────────────────────────
# PART 2: TOTP + SUBMISSION LOGIC
# ─────────────────────────────────────────

def generate_totp(secret):
    K = secret.encode('utf-8')
    T = int(time.time()) // 30
    C = struct.pack(">Q", T)
    h = hmac.new(key=K, msg=C, digestmod=hashlib.sha512).hexdigest()
    offset = int(h[-1], 16)
    binary = int(h[offset * 2:(offset * 2) + 8], 16) & 0x7FFFFFFF
    totp = binary % (10 ** 10)
    return str(totp).zfill(10)


def generate_auth_header(email, totp):
    credentials = f"{email}:{totp}"
    encoded = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    return f"Basic {encoded}"


def submit_solution(email, totp):
    auth_header = generate_auth_header(email, totp)

    payload = {
        "github_url": "https://github.com/Ishwarij032005/GlobalIntern",
        "contact_email": email,
        "solution_language": "python"
    }

    data = json.dumps(payload).encode('utf-8')

    req = urllib.request.Request(
        "https://api.challenge.hennge.com/challenges/003/submissions",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": auth_header,
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as response:
            print("Status  :", response.status)
            print("Response:", response.read().decode())
    except urllib.error.HTTPError as e:
        print("HTTP Error:", e.code)
        print("Response  :", e.read().decode())


def main_submit():
    email = "ishwari03086@gmail.com"
    secret = email + "HENNGECHALLENGE003"

    totp = generate_totp(secret)
    print(f"TOTP    : {totp}")

    auth = generate_auth_header(email, totp)
    print(f"Header  : {auth}")

    submit_solution(email, totp)


# ─────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        main_submit()
    else:
        main()
