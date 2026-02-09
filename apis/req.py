import requests
# import uuid

# email = f"test-{uuid.uuid4().hex[:6]}@example.com"
# username = f"user{uuid.uuid4().hex[:6]}"

headers = {'Accept': 'application/json'}

def api_test(url):
    response = None
    api = None
    # detect sigup or signin
    if ("signup" in url):
        input_signup = {"email":'ntc-test0@ggmail.com', "username":'test-user', "password":"1111111111"}
        api = "signup"
        response = requests.post('https://beta-eid-backend.townway.com.tw/accounts/signup', data = input_signup, headers=headers)
    elif ("signin" in url):
        input_signin = {"email":'ntc-test0@ggmail.com', "password":"1111111111"}
        api = "signin"
        response = requests.post('https://beta-eid-backend.townway.com.tw/accounts/signin', data = input_signin, headers=headers)

    return api, response.text
