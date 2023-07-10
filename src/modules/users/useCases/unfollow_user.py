from modules.users.repositories.user_repository import UserRepository

class UnfollowUserUseCase:
    def __init__(self,userRepository:UserRepository) -> None:
        self.userRepository = userRepository

    def execute(self, user_id: str, unfollow_id: str):
        # Verificar se o usuário existe
        user = self.userRepository.findById(user_id)
        unfollow_user = self.userRepository.findById(unfollow_id)

        if not user:
            return {"error":"Invalid user ID"}

        if not unfollow_user:
            return {"error":"Invalid unfollow user ID"}

        # Verificar se o usuário está seguindo o usuário a ser deixado de seguir
        existing_follow = self.userRepository.verifyFollowing(follower=user_id,following=unfollow_id)
        if not existing_follow:
            return {"error":"Not following this user"}
        
        self.userRepository.deleteFollow(user_id=user_id,unfollow_id=unfollow_id)

        return { "ok":"Successfully unfollowed user" }