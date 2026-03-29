from flask_sqlalchemy import SQLAlchemy

from modules.user.models.refresh_tokens_model import RefreshToken
class RefreshTokensDAO(SQLAlchemy):
    def create_refresh_token_record(db, user_info):
        new_token_record = RefreshToken.create(user_info)
        db.add(new_token_record)
        db.flush()
        return new_token_record
    def get_record_by_token_hash(db,token_hash):
            #查找token_hash
            record = db.query(RefreshToken) \
                .filter(RefreshToken.token_hash == token_hash) \
                .first()
            return record
    def revoke_token(db,token_record):
        token_record.revoked=True
        db.commit()