from dataclasses import dataclass
from user.models import User


@dataclass(frozen=True)
class PasswordChangeResult:
    success: bool
    error: str | None = None


class PasswordService:
    def change_password(self, user: User, old_password: str, new_password: str) -> PasswordChangeResult:
        if not user.check_password(old_password):
            return PasswordChangeResult(success=False, error="Old password is incorrect.")

        user.set_password(new_password)
        user.save()
        return PasswordChangeResult(success=True)


default_password_service = PasswordService()
