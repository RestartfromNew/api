from modules.user.models.user_model import User
from sqlalchemy import or_
class UserDAO:
    #在DAO层中并不真正提交，而是在service层提交，因为业务不是一次数据库操作，
    # 而是一次多个操作的组合，如果出现错误，可以进行事务控制和回滚

    # -------- Create --------
    @staticmethod
    def create_user(db, user_info):
        user=User.create(
            username=user_info.get('username'),
            email=user_info.get('email'),
            password_hash=user_info.get('password_hash'),
        )
        db.add(user)
        db.flush()
        return user


    # -------- Read --------

    @staticmethod
    def get_by_id(db, user_id):
        """Get user by id"""
        try:
            user=db.query(User).filter(User.id == user_id).first()
            return user
        except Exception as e:
            print(e)
            return e



    @staticmethod
    def get_by_email(db, email):
        try:
            user=db.query(User).filter(User.email == email).first()
            return user
        except Exception as e:
            print(e)
            return e



    @staticmethod
    def get_by_username(db, username):
       try:
            users=db.query(User).filter(User.username == username).all()
            return users
       except Exception as e:
            print(e)
            return e


    @staticmethod
    def get_by_email_or_username(db, identifier):
        try:
            user = db.query(User).filter(
                or_(
                    User.email == identifier.get('email'),
                    User.username == identifier.get('username')
                )
            ).first()

            return user
        except Exception as e:
            print(e)
            return e



    @staticmethod
    def list_users(db, limit=100, offset=0):
        """List users with pagination"""
        pass


    # -------- Update --------

    @staticmethod
    def update_user(db, user):
        """Update user information"""
        pass


    @staticmethod
    def update_password(db, user_id, password_hash):
        """Update user password"""
        pass


    @staticmethod
    def update_email(db, user_id, email):
        """Update user email"""
        pass


    @staticmethod
    def update_username(db, user_id, username):
        """Update username"""
        pass


    @staticmethod
    def update_last_login(db, user_id):
        """Update last login time"""
        pass


    # -------- Status --------

    @staticmethod
    def activate_user(db, user_id):
        """Activate user"""
        pass


    @staticmethod
    def deactivate_user(db, user_id):
        """Deactivate user"""
        pass


    @staticmethod
    def verify_user(db, user_id):
        """Mark user as verified"""
        pass


    # -------- Delete --------

    @staticmethod
    def delete_user(db, user_id):
        """Delete user"""
        pass


    # -------- Utility --------

    @staticmethod
    def exists_by_email(db, email):
        """Check if email exists"""
        pass


    @staticmethod
    def exists_by_username(db, username):
        """Check if username exists"""
        pass