# Tistory API Wrapper

## Overview
Tistory API Wrapper

### Install
```
$ pip install tech-ninja-tistory-api
```

### Usage  
```
from tech_ninja_tistory_api import TistoryAPI

blog_name = 'yscho03'
tistory_api = TistoryAPI(blog_name)

tistory_client_id = 'xxxxxxxxxx'
tistory_redirect_uri = 'http://localhost/tistory/auth/callback'

oauth_url = tistory_api.authorize(tistory_client_id, tistory_redirect_uri)
print('>>> Generated Oauth URL')
print(oauth_url)

"""
https://www.tistory.com/oauth/authorize?client_id=xxxxxxxxxx&redirect_uri=http://localhost/tistory/auth/callback&response_type=code&state=
"""

# access_token
tistory.access_token = '<YOUR_ACCESS_TOKEN>'
```


