from sitegate.signin_flows.remotes.discord import Discord
from sitegate.signin_flows.remotes.github import Github
from sitegate.signin_flows.remotes.gitlab import Gitlab
from sitegate.signin_flows.remotes.google import Google
from sitegate.signin_flows.remotes.yandex import Yandex
from sitegate.utils import register_remotes


register_remotes(
    Yandex(client_id='yandex-clid'),
    Google(client_id='google-clid'),
    Github(client_id='github-clid', client_secret='github-secret'),
    Gitlab(client_id='gitlab-clid', client_secret='gitlab-secret'),
    Discord(client_id='discord-clid', client_secret='discord-secret'),
)
