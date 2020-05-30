import requests
url = 'http://localhost:8000/posts'
data = {
'text':'hello world'
}

"""headers = { "access_token" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFqaW5reWFyb3giLCJwYXNzd29yZCI6IkFqaW5reWE0NyZAIiwiaXNzdWFsX3RpbWUiOjE1OTA4MjU1NDksImV4cGlyZV90aW1lIjoxNTkwODI1ODQ5fQ.XmLIOZx3ODOJ2UUS4of40ueD5_xYgrklt4McS13-sn8",
            "refresh_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFqaW5reWFyb3giLCJwYXNzd29yZCI6IkFqaW5reWE0NyZAIn0.6CjePPh8NGtXu57L-rugkmYgiofgtTYz4zTwSyz4SsM",
            "Content-Type" : "application/json"}"""
rt='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFqaW5reWFyb3giLCJwYXNzd29yZCI6IkFqaW5reWE0NyZAIn0.6CjePPh8NGtXu57L-rugkmYgiofgtTYz4zTwSyz4SsM'
headers = {'refresh-token': rt,
           ''}
response = requests.post(url, data=data,headers=headers)
print(response.json())