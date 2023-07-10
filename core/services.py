from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from core.db.dal import StorageManager
from core.models import UserInput, UserOutput
from utils.hasher import hash_pass, check_hash
from utils.http_exceptions import user_doesnt_exist, same_password
from utils.verify_code_gen import generate_code


class UserManager:

    async def create_user(self, user: UserInput, db: AsyncSession) -> UserOutput:
        user_to_inset = user.model_copy()
        user_to_inset.password = hash_pass(user.password)
        manager = StorageManager(db)
        user_data = await manager.create(user_to_inset.model_dump())
        if user_data:
            user = UserOutput(**user_data)
            return user

    async def retrieve_user(self, user_id: str, db: AsyncSession) -> Optional[UserOutput]:
        manager = StorageManager(db)
        user_data = await manager.retrieve(user_id)
        if user_data:
            user_data.pop('password')
            user = UserOutput(**user_data)
            return user

    async def retrieve_user_by_email(self, email: str, db: AsyncSession) -> Optional[UserOutput]:
        manager = StorageManager(db)
        user_data = await manager.retrieve(email)
        if user_data:
            user = UserOutput(**user_data)
            return user
        else:
            raise user_doesnt_exist

    async def unset_password(self, email: str, db: AsyncSession) -> Optional[dict]:
        manager = StorageManager(db)
        verify_code = generate_code()
        user_data = await manager.update(user_email=email, verify_code=verify_code)
        """SEND EMAIL WITH CODE"""
        code = await manager.retrieve(email)  # delete
        if not code:
            raise user_doesnt_exist
        print(f'VERIFY CODE: {code.get("verify_code")}')  # delete
        return user_data

    async def verify(self, email: str, code: str, db: AsyncSession) -> bool:
        manager = StorageManager(db)
        user_data = await manager.retrieve(email)
        if not user_data:
            raise user_doesnt_exist
        flag = code == user_data.get('verify_code')
        if flag:
            await manager.unset_verify_status(email)
        return flag

    async def set_password(self, user: UserInput, db: AsyncSession) -> UserOutput:
        manager = StorageManager(db)
        user_data_db = await manager.retrieve(user.email)
        if not user_data_db:
            raise user_doesnt_exist
        hashed_password = user_data_db.get('password')
        new_password = user.password
        if check_hash(new_password, hashed_password):
            raise same_password
        new_password_hashed = hash_pass(new_password)
        user_data = await manager.update(user.email, new_password_hashed)
        if user_data:
            user = UserOutput(**user_data)
            return user
