class PasswordMixin(object):
    def check_password(self, password: str) -> bool:
        return bcrypt_sha256.verify(password, self.password)

    def set_password(self, password: str) -> bool:
        """bcrypt 72 byte uzunluğa izin veriyor. bunu sha256 ile aşıyoruz"""
        _hash = bcrypt_sha256.using(rounds=12).hash(password)
        with db.atomic():
            return self.update_instance({"password": _hash})


class UserMixin:
    @property
    def is_authenticated(self) -> bool:
        return bool(self.id)

    @property
    def is_anonymous(self) -> bool:
        return not self.is_authenticated

    def get_id(self) -> int:
        return self.id

    def get_jwt_token(self) -> str:
        return generate_jwt_token(self.id)


class RolesMixin:
    def has_roles(self, roles: List) -> bool:
        return self.role in roles

USER_TYPES = (
    ("staff", "Staff"),
    ("admin", "Admin"),
    ("visitor","Visitor")
)
class User()