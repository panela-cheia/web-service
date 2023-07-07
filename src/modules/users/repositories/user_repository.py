from database.infra.orm import ORM
from database.schema.schema import User, File,Barn, Follows, UsersDive

from sqlalchemy.orm import joinedload

class UserRepository:
    def __init__(self):
        self.orm = ORM()
    
    def create(self, name, username, email, password):
        session = self.orm.get_session()

        user = User(name=name, username=username, email=email, password=password)
        session.add(user)
        session.commit()

        barn = Barn(user_id=user.id)
        session.add(barn)
        session.commit()

        user_dict = {
            'id': user.id,
            'name': user.name,
            'username': user.username,
            'email': user.email
        }

        session.close()

        return user_dict

    def findAll(self):
        session = self.orm.get_session()

        users = session.query(User).options(
            joinedload('barn'),
            joinedload('followers'),
            joinedload('following'),
            joinedload('owners_dive'),
            joinedload('photo'),
            joinedload('reactions'),
            joinedload('recipes'),
            joinedload('users_dive')
        ).all()

        session.close()

        return users

    def findByEmail(self, email):
        session = self.orm.get_session()

        user = session.query(User).filter(User.email == email).\
                options(
                    joinedload('barn'),
                    joinedload('followers'),
                    joinedload('following'),
                    joinedload('owners_dive'),
                    joinedload('photo'),
                    joinedload('reactions'),
                    joinedload('recipes'),
                    joinedload('users_dive')
                ).first()

        session.close()

        return user

    def findByUsername(self, username):

        session = self.orm.get_session()

        user = session.query(User).\
            filter(User.username == username).\
                options(
                    joinedload('barn'),
                    joinedload('followers'),
                    joinedload('following'),
                    joinedload('owners_dive'),
                    joinedload('photo'),
                    joinedload('reactions'),
                    joinedload('recipes'),
                    joinedload('users_dive')
                ).first()

        session.close()

        return user

    def findById(self, id):
        session = self.orm.get_session()

        user = session.query(User).options(
            joinedload('barn'),
            joinedload('followers'),
            joinedload('following'),
            joinedload('owners_dive'),
            joinedload('photo'),
            joinedload('reactions'),
            joinedload('recipes').joinedload('ingredients'),
            joinedload('recipes').joinedload('reactions'),
            joinedload('recipes').joinedload('photo'),
            joinedload('users_dive')
        ).filter(User.id == id).first()

        session.close()

        return user

    def update(self, id, name, username, bio):
        session = self.orm.get_session()

        user = session.query(User).filter(User.id == id).first()
        user.name = name
        user.username = username
        user.bio = bio
        session.commit()

        # Recarrega o usuário após a atualização
        session.refresh(user)

        session.close()

        return user

    def updatePhoto(self, id, photo_id):
        session = self.orm.get_session()

        user = session.query(User).filter(User.id == id).first()
        photo = session.query(File).filter(File.id == photo_id).first()

        if user:
            # Atualiza a foto existente ou atribui uma nova foto
            user.photo = photo

            session.merge(user)
            session.commit()

            # Recarrega o usuário da sessão para refletir as alterações
            session.refresh(user)

        session.close()

        return user

    def delete(self, id):

        session = self.orm.get_session()

        user = session.query(User).filter(User.id == id).first()
        session.delete(user)
        session.commit()

        session.close()

        return user

    def verifyFollowing(self, follower, following):

        session = self.orm.get_session()
        follows = session.query(Follows).filter(Follows.follower_id == follower, Follows.following_id == following).first()

        session.close()

        return follows is not None

    def followUser(self, user_id, follow_id):

        session = self.orm.get_session()

        follow = Follows(follower_id=user_id, following_id=follow_id)
        session.add(follow)
        session.commit()

        session.close()

        return follow

    def deleteFollow(self, user_id, unfollow_id):

        session = self.orm.get_session()

        session.query(Follows).filter(Follows.follower_id == user_id, Follows.following_id == unfollow_id).delete()
        session.commit()

        session.close()

    def findOther(self, id):

        session = self.orm.get_session()

        users = session.query(User).filter(User.id != id).options(
            joinedload('barn'),
            joinedload('followers'),
            joinedload('following'),
            joinedload('owners_dive'),
            joinedload('photo'),
            joinedload('reactions'),
            joinedload('recipes'),
            joinedload('users_dive')
        ).all()

        session.close()

        return users

    def searchUser(self, user_id, value):
        session = self.orm.get_session()

        users = session.query(User).filter(
            (User.name.contains(value) | User.username.contains(value)) & (User.id != user_id)
        ).options(
            joinedload('barn'),
            joinedload('followers'),
            joinedload('following'),
            joinedload('owners_dive'),
            joinedload('photo'),
            joinedload('reactions'),
            joinedload('recipes'),
            joinedload('users_dive')
        ).all()

        results = []

        for user in users:
            common_followers = session.query(Follows).filter(
                Follows.following_id == user.id,  # Use 'user.id' em vez de 'user_id'
                Follows.follower_id == user_id
            ).count()

            common_dives = session.query(UsersDive).filter(
                UsersDive.user_id == user_id,
                UsersDive.dive_id.in_([users_dive.dive_id for users_dive in user.users_dive])
            ).count()

            result = {
                "user": user,
                "common_followers": common_followers,
                "common_dives": common_dives
            }

            results.append(result)

        session.close()

        return results
