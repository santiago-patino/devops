from flask_sqlalchemy import SQLAlchemy
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone

db = SQLAlchemy()

class Blacklists(db.Model):
    __tablename__ = 'blacklists'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(255), unique=True, nullable=False)
    app_uuid = db.Column(UUID(as_uuid=True), nullable=False)
    #app_uuid = db.Column(db.String(80), nullable=False)
    blocked_reason = db.Column(db.String(255), nullable=False)
    ip_address = db.Column(db.String(255), nullable=False)
    createdAt = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))