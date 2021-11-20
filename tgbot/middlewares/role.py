from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from tgbot.models.role import UserRole
from tgbot.services.repository import Repo

### to do: make sure user is on db
class RoleMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ['error', 'update']

    def __init__(self, admin_id: int):
        super().__init__()
        self.admin_id = admin_id

    async def pre_process(self, obj, data, *args):
        if not hasattr(obj, 'from_user'):
            data['role'] = None
        elif obj.from_user.id == self.admin_id:
            data['role'] = UserRole.ADMIN
        else:
            user_id = obj.from_user.id
            role = await data['repo'].status_check(user_id)
            role = int(role[0][0]) #####I HATE TUPLES SO MUCH HHHHFSDGLKHJDFGSHJKJSKHLDGFJHKSDFGJLHKHJLKFGDHJLKSDHJGKLSDFLKJHGSDHJFKGHSDG
            if role == 2:
                data['role'] = UserRole.ADMIN
            elif role == 1:
                data['role'] = UserRole.USER
            else:
                data['role'] = UserRole.NOBODY

    async def post_process(self, obj, data, *args):
        data.pop('role', None)
