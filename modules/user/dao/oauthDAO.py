from modules.user.models.oauth_model import Oauth
from sqlalchemy import or_
class OauthDAO:
    @staticmethod
    def create_oauth_user(db,oauth_info):
        oauth = Oauth.create(
            provider=oauth_info['provider'],
            provider_user_id=oauth_info['provider_user_id'],
            user_id=oauth_info['user_id'],
        )
        db.add(oauth)
        db.flush()
        return oauth
    @staticmethod
    def get_oauth_user_by_provider_id(db,provider_user_id,provider):
        oauth_user=db.query(Oauth).filter(Oauth.provider_user_id == provider_user_id, Oauth.provider==provider).first()
        return oauth_user