import webbrowser
import httpx
from pydantic import BaseModel
import requests
import json
from loguru import logger

from sweepai.app.config import SweepChatConfig
from sweepai.core.entities import PullRequest, Snippet
from sweepai.utils.constants import PREFIX

def break_json(raw_json: str):
    # turns something like {"function_call": {"arguments": " \""}}{"function_call": {"arguments": "summary"}} into two objects
    try:
        yield json.loads(raw_json)
    except json.JSONDecodeError:
        for i in range(1, len(raw_json)):
            try:
                obj = json.loads(raw_json[:i])
                yield obj
                for item in break_json(raw_json[i:]):
                    yield item
                break
            except json.JSONDecodeError:
                pass


class APIClient(BaseModel):
    config: SweepChatConfig
    api_endpoint = f"https://sweepai--{PREFIX}-ui.modal.run"

    def get_installation_id(self):
        results = requests.post(
            self.api_endpoint + "/installation_id",
            json= self.config.dict(),
        )
        if results.status_code == 401:
            print("Installation ID not found! Please install sweep first.")
            webbrowser.open_new_tab("https://github.com/apps/sweep-ai")
            raise Exception(results.json()["detail"])
        if results.status_code != 200:
            raise Exception(results.json()["detail"])
        obj = results.json()
        return obj["installation_id"]

    def search(
        self,
        query: str,
        n_results: int = 5,
    ):
        results = requests.post(
            self.api_endpoint + "/search",
            json={
                "query": query,
                "n_results": n_results,
                "config": self.config.dict(),
            }
        )
        snippets = [Snippet(**item) for item in results.json()]
        return snippets
    
    def create_pr(
        self,
        file_change_requests: list[tuple[str, str]],
        pull_request: PullRequest,
        messages: list[tuple[str | None, str | None]],
    ):
        results = requests.post(
            self.api_endpoint + "/create_pr",
            json={
                "file_change_requests": file_change_requests,
                "pull_request": pull_request,
                "messages": messages,
                "config": self.config.dict(),
            },
            timeout=10 * 60
        )
        return results.json()
    
    def chat(
        self, 
        messages: list[tuple[str | None, str | None]],
        snippets: list[Snippet] = [],
        model: str = "gpt-4-0613",
    ) -> str:
        results = requests.post(
            self.api_endpoint + "/chat",
            json={
                "messages": messages,
                "snippets": [snippet.dict() for snippet in snippets],
                "config": self.config.dict()
            }
        )
        return results.json()
    
    def stream_chat(
        self, 
        messages: list[tuple[str | None, str | None]], 
        snippets: list[Snippet] = [],
        model: str = "gpt-4-0613"
    ):
        with httpx.Client(timeout=30) as client: # sometimes this step is slow
            with client.stream(
                'POST', 
                self.api_endpoint + '/chat_stream',
                json={
                    "messages": messages,
                    "snippets": [snippet.dict() for snippet in snippets],
                    "config": self.config.dict()
                }
            ) as response:
                for delta_chunk in response.iter_text():
                    if not delta_chunk:
                        break
                    try:
                        for item in break_json(delta_chunk):
                            yield item
                    except json.decoder.JSONDecodeError as e: 
                        logger.error(delta_chunk)
                        raise e
