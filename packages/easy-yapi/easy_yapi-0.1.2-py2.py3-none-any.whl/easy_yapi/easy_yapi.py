"""Main module."""
from .user import UserMixIn
from .group import GroupMixIn
from .project import ProjectMixIn


class Yapi(UserMixIn, GroupMixIn, ProjectMixIn):
    """封装yapi接口"""

    def __init__(self, base_url):
        """登录"""
        super().__init__(base_url)


if __name__ == '__main__':
    yapi = Yapi('nocoding@126.com', 'ymfe.org')
