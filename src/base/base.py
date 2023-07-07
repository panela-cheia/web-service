import json
from constants.topics import Topics
from loguru import logger

# Configuração básica do logger
logger.add("app.log", rotation="500 MB", retention="10 days", level="INFO")

# repositories
from modules.users.repositories.user_repository import UserRepository
from modules.files.repositories.files_repository import FilesRepository
from modules.recipes.repositories.recipe_repository import RecipeRepository
from modules.dive.repositories.dive_repository import DiveRepository
from modules.barn.repositories.barn_repository import BarnRepository
from modules.ingredients_unit.repositories.ingredients_unit_repository import IngredientsUnitRepository

# usecases
from modules.users.useCases.create_user import CreateUserUseCase
from modules.users.useCases.list_all_users import ListAllUsersUseCase
from modules.users.useCases.list_others import ListOthersUseCase
from modules.users.useCases.update_user import UpdateUserUseCase
from modules.users.useCases.update_photo_user import UpdatePhotoUserUseCase
from modules.users.useCases.login_user import LoginUserUseCase
from modules.users.useCases.login_user_with_username import LoginUserWithUsernameUseCase
from modules.users.useCases.follow_user import FollowUserUseCase
from modules.users.useCases.unfollow_user import UnfollowUserUseCase
from modules.users.useCases.search_users import SearchUsersUseCase
from modules.users.useCases.user_profile import UserProfileUseCase
from modules.users.useCases.search_in_users_barn import SearchInUsersBarnUseCase
from modules.users.useCases.users_barn import UsersBarnUseCase

from modules.files.useCases.create_file import CreateFileUseCase
from modules.files.useCases.delete_file import DeleteFileUseCase

from modules.recipes.useCases.create_recipe_usecase import CreateRecipeUseCase
from modules.recipes.useCases.list_usecase import ListRecipesUseCase
from modules.recipes.useCases.search_recipes_usecase import SearchRecipesUseCase
from modules.recipes.useCases.reaction_recipe_usecase import ReactionRecipeUseCase

from modules.barn.useCases.save_recipe import SaveRecipeUseCase
from modules.barn.useCases.search_recipe import SearhRecipeUseCase
from modules.barn.useCases.remove_recipe import RemoveRecipeUseCase

from modules.dive.useCases.create_dive_usecase import CreateDiveUseCase
from modules.dive.useCases.enter_dive import EnterDiveUseCase
from modules.dive.useCases.exit_dive import ExitDiveUseCase
from modules.dive.useCases.update_dive import UpdateDiveUseCase
from modules.dive.useCases.search_dive import SearchDiveUseCase
from modules.dive.useCases.list_users_dive import ListUserDiveUseCase
from modules.dive.useCases.list_dive_recipes_usecase import ListDiveRecipesUseCase

from modules.search.useCases.search_dive_and_users_usecase import SearchDiveAndUserUseCase

from modules.ingredients_unit.useCases.create_ingredients_unit_usecase import CreateIngredientsUnitUseCase
from modules.ingredients_unit.useCases.delete_ingredients_unit_usecase import DeleleIngredientsUnitUseCase
from modules.ingredients_unit.useCases.list_ingredients_unit_usecase import ListIngredientsUnitUseCase

# dtos
from modules.users.dtos.create_user_dto import CreateUserDTO
from modules.users.dtos.update_user_dto import UpdateUserDTO

from modules.files.dtos.create_file_dto import CreateFileDTO
from modules.files.dtos.delete_file_dto import DeleteFileDTO

from modules.recipes.dtos.create_recipe_dto import CreateRecipeDTO
from modules.recipes.dtos.reactions_dto import ReactionDTO,ReactionType

from modules.dive.dtos.create_dive_dto import CreateDiveDTO
from modules.dive.dtos.update_dive_dto import UpdateDiveDTO
from modules.dive.dtos.exit_dive_dto import ExitDiveDTO

from modules.barn.dtos.save_recipe_dto import BarnSaveRecipeDTO
from modules.barn.dtos.search_recipe_in_barn_dto import SearchRecipeInBarnDTO
from modules.barn.dtos.remove_recipe_dto import RemoveRecipeDTO

from modules.search.dtos.search_dive_and_users_dto import SearchDiveAndUserDTO

# utils
from utils.convert_list_convert_to_ingredient_dtos import convert_list_to_ingredient_dtos


class Bootstrap:
    def __init__(self)-> None:
        pass

    def run(self,message:str):
        userRepository = UserRepository()
        filesRepository = FilesRepository()
        recipeRepository = RecipeRepository()
        diveRepository = DiveRepository()
        barnRepository = BarnRepository()
        ingredientsUnitRepository = IngredientsUnitRepository()

        createUserUseCase = CreateUserUseCase(userRepository=userRepository)
        loginUserUseCase= LoginUserUseCase(userRepository=userRepository)
        loginUserWithUsernameUseCase= LoginUserWithUsernameUseCase(userRepository=userRepository)
        listAllUsersUseCase = ListAllUsersUseCase(userRepository=userRepository)
        listOthersUseCase = ListOthersUseCase(userRepository=userRepository)
        followUserUseCase= FollowUserUseCase(userRepository=userRepository)
        unfollowUserUseCase= UnfollowUserUseCase(userRepository=userRepository)
        updateUserUseCase= UpdateUserUseCase(userRepository=userRepository)
        updatePhotoUserUseCase = UpdatePhotoUserUseCase(userRepository=userRepository)
        searchUsersUseCase = SearchUsersUseCase(userRepository=userRepository)
        userProfileUseCase = UserProfileUseCase(userRepository=userRepository)
        searchInUsersBarnUseCase = SearchInUsersBarnUseCase(userRepository=userRepository,barnRepository=barnRepository)
        usersBarnUseCase = UsersBarnUseCase(userRepository=userRepository,barnRepository=barnRepository)

        createFileUseCase = CreateFileUseCase(repository=filesRepository)
        deleteFileUseCase = DeleteFileUseCase(repository=filesRepository)

        createRecipeUseCase = CreateRecipeUseCase(repository=recipeRepository)
        listRecipesUseCase = ListRecipesUseCase(repository=recipeRepository)
        searchRecipesUseCase = SearchRecipesUseCase(repository=recipeRepository)
        reactionRecipeUseCase = ReactionRecipeUseCase(repository=recipeRepository)

        saveRecipeInBarnUseCase = SaveRecipeUseCase(repository=barnRepository)
        searchRecipeUseCase = SearhRecipeUseCase(repository=barnRepository)
        removeRecipeUseCase = RemoveRecipeUseCase(repository=barnRepository)

        createDiveUseCase = CreateDiveUseCase(repository=DiveRepository)
        createDiveUseCase = CreateDiveUseCase(repository=diveRepository)
        enterDiveUseCase = EnterDiveUseCase(repository=diveRepository)
        exitDiveUseCase = ExitDiveUseCase(repository=diveRepository)
        updateDiveUseCase = UpdateDiveUseCase(repository=diveRepository)
        searchDiveUseCase = SearchDiveUseCase(repository=diveRepository)
        listUserDiveUseCase = ListUserDiveUseCase(repository=diveRepository)
        listDiveRecipesUseCase = ListDiveRecipesUseCase(repository=diveRepository,recipeRepository=recipeRepository)

        searchDiveAndUserUseCase = SearchDiveAndUserUseCase(userRepository=userRepository,diveRepository=diveRepository)

        createIngredientsUnitUseCase = CreateIngredientsUnitUseCase(repository=ingredientsUnitRepository)
        deleleIngredientsUnitUseCase = DeleleIngredientsUnitUseCase(repository=ingredientsUnitRepository)
        listIngredientsUnitUseCase = ListIngredientsUnitUseCase(repository=ingredientsUnitRepository)

        content = json.loads(message)

        answer = ""

        try:
            topic = Topics(content["topic"])
            body = content["body"]
        except (KeyError, ValueError):
            logger.critical("Invalid message format")

        if topic == Topics.USER_CREATE.value:
            createUserDTO = CreateUserDTO(
                name=body["name"],
                username=body["username"],
                email=body["email"],
                password=body["password"]
            )

            try:
                user = createUserUseCase.execute(createUserDTO=createUserDTO)
                logger.info("{topic} - {user}",topic=Topics.USER_CREATE.value,user=json.dumps(user,indent=4,ensure_ascii=False))
                
                answer = user
            except (ValueError):
                raise Exception(ValueError)

        elif topic == Topics.USER_LOGIN_EMAIL.value:
            user = loginUserUseCase.execute(email=body["email"],password=body["password"])
            logger.info("{topic} - {user}",topic=Topics.USER_LOGIN_EMAIL.value,user=json.dumps(user,indent=4,ensure_ascii=False))

            answer = user

        elif topic == Topics.USER_LOGIN_USERNAME.value:
            user = loginUserWithUsernameUseCase.execute(username=body["username"],password=body["password"])
            logger.info("{topic} - {user}",topic=Topics.USER_LOGIN_USERNAME.value,user=json.dumps(user,indent=4,ensure_ascii=False))

            answer = user

        elif topic == Topics.USER_LIST.value:
            users = listAllUsersUseCase.execute()
            logger.info("{topic} - {users}",topic=Topics.USER_LIST.value,users=users)

            answer = users

        elif topic == Topics.USER_LIST_OTHERS.value:
            users = listOthersUseCase.execute(id=body["id"])
            logger.info("{topic} - {users}",topic=Topics.USER_LIST_OTHERS.value,users=users)

            answer = users

        elif topic == Topics.USER_FOLLOW.value:
            follow = followUserUseCase.execute(user_id=body["user_id"],follow_id=body["follow_id"])
            logger.info("{topic} - {response}",topic=Topics.USER_FOLLOW.value,response=follow)
            
            answer = follow

        elif topic == Topics.USER_UNFOLLOW.value:
            unfollow = unfollowUserUseCase.execute(user_id=body["user_id"],unfollow_id=body["unfollow_id"])
            logger.info("{topic} - {response}",topic=Topics.USER_UNFOLLOW.value,response=unfollow)

            answer = unfollow

        elif topic == Topics.USER_UPDATE.value:
            updateUserDTO = UpdateUserDTO(
                bio=body["bio"],
                name=body["name"],
                username=body["username"]
            )

            update = updateUserUseCase.execute(id=body["id"],updateUserDTO=updateUserDTO)
            logger.info("{topic} - {response}",topic=Topics.USER_UPDATE.value,response=update)

            answer = update

        elif topic == Topics.USER_UPDATE_PHOTO.value:
            update = updatePhotoUserUseCase.execute(id=body["id"],photo=body["photo"])
            logger.info("{topic} - {response}",topic=Topics.USER_UPDATE_PHOTO.value,response=update)

            answer = update
        
        elif topic == Topics.USER_SEARCH_USERS.value:
            users = searchUsersUseCase.execute(user_id=body["user_id"],value=body["value"])
            logger.info("{topic} - {response}",topic=Topics.USER_SEARCH_USERS.value,response=json.dumps(users,indent=4,ensure_ascii=False))

            answer = users

        elif topic == Topics.USER_PROFILE.value:
            user = userProfileUseCase.execute(user_id=body["user_id"])
            logger.info("{topic} - {response}",topic=Topics.USER_PROFILE.value,response=json.dumps(user,indent=4,ensure_ascii=False))

            answer = user

        elif topic == Topics.USER_SEARCH_IN_BARN.value:
            user = searchInUsersBarnUseCase.execute(user_id=body["user_id"],value=body["value"])
            logger.info("{topic} - {response}",topic=Topics.USER_SEARCH_IN_BARN.value,response=json.dumps(user,indent=4,ensure_ascii=False))

            answer = user

        elif topic == Topics.USER_BARN.value:
            user = usersBarnUseCase.execute(user_id=body["user_id"])
            logger.info("{topic} - {response}",topic=Topics.USER_BARN.value,response=json.dumps(user,indent=4,ensure_ascii=False))

            answer = user

        elif topic == Topics.BARN_SEARCH_RECIPE.value:
            dto = SearchRecipeInBarnDTO(barnId=body["id"],recipeName=body["name"])
            recipes = searchRecipeUseCase.execute(data=dto)
            logger.info("{topic} - {response}",topic=Topics.BARN_SEARCH_RECIPE.value,response=recipes)

            answer = recipes

        elif topic == Topics.BARN_SAVE_RECIPE.value:
            dto = BarnSaveRecipeDTO(barnId=body["id"],recipeId=body["recipe_id"])
            barn = saveRecipeInBarnUseCase.execute(data=dto)
            logger.info("{topic} - {response}",topic=Topics.BARN_SAVE_RECIPE.value,response=json.dumps(barn,indent=4,ensure_ascii=False))

            answer = barn

        elif topic == Topics.BARN_REMOVE_RECIPE.value:
            dto = RemoveRecipeDTO(barnId=body["id"],recipeId=body["recipe_id"])
            barn = removeRecipeUseCase.execute(data=dto)
            logger.info("{topic} - {response}",topic=Topics.BARN_REMOVE_RECIPE.value,response=json.dumps(barn,indent=4,ensure_ascii=False))

            answer = barn

        elif topic == Topics.FILE_CREATE.value:
            createFileDTO = CreateFileDTO(name=body["name"],path=body["path"])
            file = createFileUseCase.execute(createFileDTO=createFileDTO)
            logger.info("{topic} - {response}",topic=Topics.FILE_CREATE.value,response=file)

            answer = file

        elif topic == Topics.FILE_DELETE.value:
            deleteFileDTO = DeleteFileDTO(id=body["id"])
            file = deleteFileUseCase.execute(deleteFileDTO=deleteFileDTO)
            logger.info("{topic} - {response}",topic=Topics.FILE_DELETE.value,response=file)
        
            answer = file

        elif topic == Topics.RECIPE_CREATE.value:
            createRecipeDTO = CreateRecipeDTO(
                name=body["name"],
                description=body["description"],
                ingredients=convert_list_to_ingredient_dtos(data=body["ingredients"]),
                userId=body["userId"],
                fileId=body["fileId"],
                diveId=body["diveId"] if "diveId" in body else None
            )

            recipe = createRecipeUseCase.execute(data=createRecipeDTO)
            logger.info("{topic} - {response}",topic=Topics.RECIPE_CREATE.value,response=json.dumps(recipe,indent=4,ensure_ascii=False))

            answer = recipe

        elif topic == Topics.RECIPE_LIST.value:
            recipes = listRecipesUseCase.execute()
            logger.info("{topic} - {response}",topic=Topics.RECIPE_LIST.value,response=json.dumps(recipes,indent=4,ensure_ascii=False))

            answer = recipes

        elif topic == Topics.RECIPE_REACTION.value:
            type = ReactionType(body["type"])
            dto = ReactionDTO(type=type.value,recipe_id=body["recipe_id"],user_id=body["user_id"])
            reaction = reactionRecipeUseCase.execute(reaction_data=dto) 
            logger.info("{topic} - {response}",topic=Topics.RECIPE_REACTION.value,response=reaction)

            answer = reaction

        elif topic == Topics.RECIPE_SEARCH.value:
            recipes = searchRecipesUseCase.execute(name=body["name"])
            logger.info("{topic} - {response}",topic=Topics.RECIPE_SEARCH.value,response=json.dumps(recipes,indent=4,ensure_ascii=False))

            answer = recipes

        elif topic == Topics.DIVE_CREATE.value:
            createDiveDTO = CreateDiveDTO(
                name=body["name"],
                description=body["description"],
                fileId=body["fileId"],
                userId=body["userId"]
            )

            dive = createDiveUseCase.execute(data=createDiveDTO)
            logger.info("{topic} - {response}",topic=Topics.DIVE_CREATE.value,response=dive)

            answer = dive

        elif topic == Topics.DIVE_SEARCH.value:
            dive = searchDiveUseCase.execute(diveName=body["name"])
            logger.info("{topic} - {response}",topic=Topics.DIVE_SEARCH.value,response=json.dumps(dive,indent=4,ensure_ascii=False))

            answer = dive

        elif topic == Topics.DIVE_ENTER.value:
            dive = enterDiveUseCase.execute(user_id=body["id"],dive_id=body["diveId"])
            logger.info("{topic} - {response}",topic=Topics.DIVE_ENTER.value,response=json.dumps(dive,indent=4,ensure_ascii=False))

            answer = dive

        elif topic == Topics.DIVE_EXIT.value:
            exitDiveDTO = ExitDiveDTO(
                user=body["user"],
                new_owner=body["new_owner"] if "new_owner" in body else None,
                diveId=body["diveId"]
            )
            
            dive = exitDiveUseCase.execute(data=exitDiveDTO)
            logger.info("{topic} - {response}",topic=Topics.DIVE_EXIT.value,response=json.dumps(dive,indent=4,ensure_ascii=False))

            answer = dive

        elif topic == Topics.DIVE_UPDATE.value:
            dto = UpdateDiveDTO(
                id=body["id"],
                description=body["description"] if "description" in body else None,
                fileId=body["fileId"] if "fileId" in body else None,
                name=body["name"] if "name" in body else None,
            )

            dive_updated = updateDiveUseCase.execute(updateDiveDTO=dto)
            logger.info("{topic} - {response}",topic=Topics.DIVE_UPDATE.value,response=json.dumps(dive_updated,indent=4,ensure_ascii=False))

            answer = dive_updated

        elif topic == Topics.DIVE_USERS_DIVE.value:
            dives = listUserDiveUseCase.execute(user_id=body["user_id"])
            logger.info("{topic} - {response}",topic=Topics.DIVE_USERS_DIVE.value,response=json.dumps(dives,indent=4,ensure_ascii=False))

            answer = dives

        elif topic == Topics.DIVE_LIST_RECIPES.value:
            dives = listDiveRecipesUseCase.execute(dive_id=body["dive_id"])
            logger.info("{topic} - {response}",topic=Topics.DIVE_LIST_RECIPES.value,response=json.dumps(dives,indent=4,ensure_ascii=False))

            answer = json.dumps(dives)

        elif topic == Topics.SEARCH_DIVE_AND_USERS.value:
            dto = SearchDiveAndUserDTO(user_id=body["user_id"],search_value=body["value"])

            data = searchDiveAndUserUseCase.execute(data=dto)

            logger.info("{topic} - {response}",topic=Topics.SEARCH_DIVE_AND_USERS.value,response=json.dumps(data,indent=4,ensure_ascii=False))

            answer = data

        elif topic == Topics.INGREDIENT_UNI_CREATE.value:
            unit = createIngredientsUnitUseCase.execute(name=body["name"])
            logger.info("{topic} - {response}",topic=Topics.INGREDIENT_UNI_CREATE.value,response=json.dumps(unit,indent=4,ensure_ascii=False))

            answer = unit

        elif topic == Topics.INGREDIENT_UNIT_DELETE.value:
            unit = deleleIngredientsUnitUseCase.execute(id=body["id"])
            logger.info("{topic} - {response}",topic=Topics.INGREDIENT_UNIT_DELETE.value,response=json.dumps(unit,indent=4,ensure_ascii=False))
        
            answer = unit

        elif topic == Topics.INGREDIENT_UNIT_LIST.value:
            units = listIngredientsUnitUseCase.execute()
            logger.info("{topic} - {response}",topic=Topics.INGREDIENT_UNIT_LIST.value,response=json.dumps(units,indent=4,ensure_ascii=False))

            answer = units

        return answer