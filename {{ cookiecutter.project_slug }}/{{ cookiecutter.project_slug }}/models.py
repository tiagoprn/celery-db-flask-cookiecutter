from datetime import datetime
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from {{cookiecutter.project_slug}}.extensions import db


class SampleModel(db.Model):
    """
    Available datatypes:
    https://docs.sqlalchemy.org/en/13/core/type_basics.html
    """

    uuid = db.Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(), index=True
    )
    name = db.Column(db.String(255), nullable=False, index=True)
    value = db.Column(db.Float, nullable=False)
    extra_info = db.Column(db.Text, nullable=True)
