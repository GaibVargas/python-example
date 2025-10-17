import unittest
from unittest.mock import AsyncMock, MagicMock
from app.dtos.user_dtos import UserCreate
from app.models.user_model import User
from app.services.user_service import UserService


class TestUserService(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.mock_repo.get_by_cpf = AsyncMock()
        self.mock_repo.create = AsyncMock()
        self.service = UserService(repo=self.mock_repo)

    async def test_create_user_success(self):
        """Deve criar o usuário quando CPF não existe."""
        payload = UserCreate(cpf="12345678900", full_name="Alice")
        self.mock_repo.get_by_cpf.return_value = None
        created_user = User(id=1, cpf=payload.cpf, full_name=payload.full_name)
        self.mock_repo.create.return_value = created_user

        result = await self.service.create_user(payload)

        self.mock_repo.get_by_cpf.assert_awaited_once_with("12345678900")
        self.mock_repo.create.assert_awaited_once_with(payload)
        self.assertEqual(result, created_user)

    async def test_create_user_already_exists(self):
        """Deve lançar ValueError quando CPF já existir."""
        payload = UserCreate(cpf="12345678900", full_name="Bob")
        self.mock_repo.get_by_cpf.return_value = User(id=1, cpf=payload.cpf, full_name=payload.full_name)

        with self.assertRaises(ValueError) as ctx:
            await self.service.create_user(payload)

        self.assertEqual(str(ctx.exception), "User with this CPF already exists")
        self.mock_repo.create.assert_not_called()
