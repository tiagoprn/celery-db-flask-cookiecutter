from datetime import datetime
from typing import List, Union
from uuid import uuid4

from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import UUID

from {{cookiecutter.project_slug}}.commons import get_query_raw_sql
from {{cookiecutter.project_slug}}.extensions import db, bcrypt

"""
Available datatypes:
https://docs.sqlalchemy.org/en/13/core/type_basics.html
"""


class User(db.Model):
    uuid = db.Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    # NOTE: use backref here to automatically create the reverse side so on the DependantModel model
    #       I can get e.g. "dependant_model_instance.user.email".
    #       The alternative would be to use back_populates to make this explicit on both models
    #       (so I would need to declare the relationship on both models)
    # dependant_instances = db.relationship("DependantModel", backref="user", lazy=True)

    def hash(self, password: str) -> object:
        return bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)

    def register(self, username: str, email: str, password: str) -> "User":
        # TODO: handle existing user
        new_user = User(
            username=username, email=email, password_hash=self.hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        db.session.refresh(new_user)
        return new_user

    def update(self, email: str = "", password: str = ""):
        if (not email) and (not password):
            return self

        if email:
            self.email = email

        if password:
            self.password_hash = self.hash(password)

        self.last_updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)

    @staticmethod
    def get_by(
        uuid: str = "", email: str = "", username: str = ""
    ) -> Union[None, "User"]:
        if uuid:
            return User.query.filter_by(uuid=uuid).first()
        if email:
            return User.query.filter_by(email=email).first()
        if username:
            return User.query.filter_by(username=username).first()
        return None
