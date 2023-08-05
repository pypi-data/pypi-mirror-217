import requests
import json
import time
from typing import Dict, Any, Optional
from urllib.parse import urlencode
import argparse


class TistoryAPI:
    def __init__(self, blog_name: str, base_url: str = "https://www.tistory.com", api_base_url: str = "https://www.tistory.com/apis",
                 is_raw_response: bool = False, access_token: str = None):
        self.base_url = base_url
        self.api_base_url = api_base_url
        self.blog_name = blog_name
        self.is_raw_response = is_raw_response
        self.headers = {"Accept": "*/*", "Connection": "keep-alive"}
        self.access_token = access_token

    def authorize(self, tistory_client_id: str, tistory_redirect_uri: str) -> str:
        params = {
            "client_id": tistory_client_id,
            "redirect_uri": tistory_redirect_uri,
            "response_type": "code",
            "state": "",
        }
        query_string = urlencode(params)
        return f"{self.base_url}/oauth/authorize?{query_string}"

    def make_base_params(self) -> Dict[str, Any]:
        params = {
            "access_token": self.access_token,
            "blogName": self.blog_name,
            "output": "json",
        }
        return params

    def create_simple_response(self, response: requests.Response) -> Dict[str, Any]:
        return response.text

    def create_raw_response(self, response):
        output = {
            "headers": response.headers,
            "body": json.loads(response.text),
            "status_code": response.status_code,
        }
        return output

    def create_response(self, response: requests.Response) -> Dict[str, Any]:
        if self.is_raw_response == True:
            return self.create_raw_response(response)
        else:
            return self.create_simple_response(response)

    def read_info(self, **kwargs: Any) -> Dict[str, Any]:
        api_url = f"{self.api_base_url}/blog/info"
        params = dict(self.make_base_params(), **kwargs)
        response = requests.get(api_url, headers=self.headers, params=params)
        return self.create_response(response)

    def reads_category(self, **kwargs: Any) -> Dict[str, Any]:
        api_url = f"{self.api_base_url}/category/list"
        params = dict(self.make_base_params(), **kwargs)
        response = requests.get(api_url, headers=self.headers, params=params)
        return self.create_response(response)

    def create(self, title: str, content: str, category_id: int = 0, visibility: int = 3, accept_comment: int = 0,
               slogan: Optional[str] = None, tag: Optional[str] = None, **kwargs: Any,) -> Dict[str, Any]:
        api_url = f"{self.api_base_url}/post/write"
        current_timestamp = time.time()
        data = dict(
            {
                "title": title,
                "content": content,
                "visibility": visibility,
                "category": category_id,
                "published": current_timestamp,
                "slogan": slogan,
                "tag": tag,
                "acceptComment": accept_comment,
                "output": "json",
            },
            **self.make_base_params(),
            **kwargs,
        )
        response = requests.post(api_url, headers=self.headers, data=data)
        return self.create_response(response)

    def read(self, post_id: int, **kwargs: Any) -> Dict[str, Any]:
        api_url = f"{self.api_base_url}/post/read"
        params = dict(
            {
                "postId": post_id,
            },
            **self.make_base_params(),
            **kwargs,
        )
        response = requests.get(api_url, headers=self.headers, params=params)
        return self.create_response(response)

    def reads(self, page_number: int = 1, **kwargs: Any) -> Dict[str, Any]:
        api_url = f"{self.api_base_url}/post/list"
        params = dict(
            {
                "page": page_number,
            },
            **self.make_base_params(),
            **kwargs,
        )
        response = requests.get(api_url, headers=self.headers, params=params)
        return self.create_response(response)

    def update(self, post_id: int, title: str, content: str, category_id: int = 0,
               visibility: int = 0,
               accept_comment: int = 1,
               slogan: Optional[str] = None,
               tag: Optional[str] = None,
               **kwargs: Any,
               ) -> Dict[str, Any]:
        api_url = f"{self.api_base_url}/post/modify"
        current_timestamp = time.time()
        data = dict(
            {
                "postId": post_id,
                "title": title,
                "content": content,
                "visibility": visibility,
                "category": category_id,
                "published": current_timestamp,
                "slogan": slogan,
                "tag": tag,
                "acceptComment": accept_comment,
            },
            **self.make_base_params(),
            **kwargs,
        )
        response = requests.post(api_url, headers=self.headers, data=data)
        return self.create_response(response)

    def attach_file(self, file_path: str, **kwargs: Any) -> Dict[str, Any]:
        api_url = f"{self.api_base_url}/post/attach"

        data = dict(self.make_base_params(), **kwargs)
        files = {"uploadedfile": open(file_path, "rb")}
        response = requests.post(
            api_url, headers=self.headers, files=files, data=data)
        return self.create_response(response)

    def create_comment(self,
                       post_id: int,
                       content: str,
                       secret: int = 0,
                       parent_id: Optional[int] = None,
                       **kwargs: Any,
                       ) -> Dict[str, Any]:
        api_url = f"{self.api_base_url}/comment/write"
        data = dict(
            {
                "postId": post_id,
                "parentId": parent_id,
                "content": content,
                "secret": secret,
                "output": "json",
            },
            **self.make_base_params(),
            **kwargs,
        )
        response = requests.post(api_url, headers=self.headers, data=data)
        return self.create_response(response)

    def reads_comment(self, post_id: int, **kwargs: Any) -> Dict[str, Any]:
        api_url = f"{self.api_base_url}/comment/list"
        params = dict(
            {
                "postId": post_id,
            },
            **self.make_base_params(),
            **kwargs,
        )
        response = requests.get(api_url, headers=self.headers, params=params)
        return self.create_response(response)

    def update_comment(self, post_id: int, comment_id: int, content: str, secret: int = 0, parent_id: Optional[int] = None, **kwargs: Any) -> Dict[str, Any]:
        api_url = f"{self.api_base_url}/comment/modify"
        data = dict(
            {
                "postId": post_id,
                "parentId": parent_id,
                "commentId": comment_id,
                "content": content,
                "secret": secret,
            },
            **self.make_base_params(),
            **kwargs,
        )
        response = requests.post(api_url, headers=self.headers, data=data)
        return self.create_response(response)

    def delete_comment(self, post_id: int, comment_id: int, **kwargs: Any) -> Dict[str, Any]:
        api_url = f"{self.api_base_url}/comment/delete"
        data = dict(
            {"postId": post_id, "commentId": comment_id, "output": "json"},
            **self.make_base_params(),
            **kwargs,
        )
        response = requests.post(api_url, headers=self.headers, data=data)
        return self.create_response(response)

