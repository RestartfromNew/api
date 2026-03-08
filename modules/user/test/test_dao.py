from modules.user.dao.userDAO import UserDAO
def test_selection(db,data):

    user1=UserDAO.get_by_email_or_username(db,data)

    print("select from email",user1)
    return user1
