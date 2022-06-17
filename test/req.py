from requests import get, post, delete

print(delete("http://xsolj.pythonanywhere.com/api/v1/user/3").json())
