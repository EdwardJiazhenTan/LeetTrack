from datetime import datetime
from app import db
from passlib.hash import bcrypt


class User(db.Model):
    """User model"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    leetcode_username = db.Column(db.String(50))
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    last_login = db.Column(db.DateTime(timezone=True))
    is_active = db.Column(db.Boolean, default=True)
    # New: admin flag
    is_admin = db.Column(db.Boolean, default=False)

    # Relationships
    user_questions = db.relationship(
        "UserQuestion", back_populates="user", cascade="all, delete-orphan"
    )
    review_schedules = db.relationship(
        "ReviewSchedule", back_populates="user", cascade="all, delete-orphan"
    )
    created_paths = db.relationship("LearningPath", back_populates="creator")
    learning_paths = db.relationship(
        "UserLearningPath", back_populates="user", cascade="all, delete-orphan"
    )

    def set_password(self, password):
        """Hash and set the user's password."""
        self.password_hash = bcrypt.hash(password)

    def check_password(self, password):
        """Check if the provided password matches the stored hash."""
        return bcrypt.verify(password, self.password_hash)

    @property
    def id(self):
        """Return user_id as id for compatibility with JWT and other systems."""
        return self.user_id

    def __repr__(self):
        return f"<User {self.email}>"
