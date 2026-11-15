from sitegate.signin_flows.remotes.github import Github
from sitegate.signin_flows.remotes.google import Google
from sitegate.signin_flows.remotes.yandex import Yandex
from sitegate.utils import register_remotes


register_remotes(
    Yandex(client_id='yandex-clid'),
    Google(client_id='google-clid'),
    Github(client_id='github-clid', client_secret='github-secret'),
)
