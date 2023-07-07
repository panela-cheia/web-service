aux1 = {
    "topic": "@user/create_user",
    "body": {
        "name": "Mendes",
        "username": "@o.viniciusmendes",
        "email": "vinicius@gmail.com",
        "password": "12345678"
    }
}

aux2 = {
    "topic": "@user/login_with_email_user",
    "body": {
        "email": "joao.da.silva@gmail.com",
        "password": "12345678"
    }
}

aux3 = {
    "topic": "@user/login_with_username_user",
    "body": {
        "username": "@joaodasilva",
        "password": "12345678"
    }
}

aux4 = {
    "topic": "@user/list_user",
    "body": {
    }
}

aux5 = {
    "topic": "@user/list_others_user",
    "body": {
        "id": "6809d450-68e0-479f-91e1-7d2d5c52ad90"
    }
}

aux6 = {
    "topic": "@user/follow_user",
    "body": {
        "user_id": "823e3881-bda1-4f2a-9593-83c8d7fd0044",
        "follow_id": "5ca07281-0e46-4abc-8f1f-54b61ca27631"
    }
}

aux7 = {
    "topic": "@user/unfollow_user",
    "body": {
        "user_id": "5ca07281-0e46-4abc-8f1f-54b61ca27631",
        "unfollow_id": "f57255d9-afc0-478e-949b-0301f0bc05d0"
    }
}

aux8 = {
    "topic": "@user/update_user",
    "body": {
        "id": "75621072-e6b5-49ae-a5ff-424707d534b2",
        "bio": "amo comer!",
        "name": "Vinicius Mendes",
        "username": "@vinicmendes"
    }
}

aux9 = {
    "topic": "@user/update_photo_user",
    "body": {
        "id": "823e3881-bda1-4f2a-9593-83c8d7fd0044",
        "photo": "96a89a09-6d2b-431f-8216-f5403b45cea3"
    }
}

aux10 = {
    "topic": "@file/create_file",
    "body": {
        "name": "file.png",
        "path": "path"
    }
}

aux11 = {
    "topic": "@file/delete_file",
    "body": {
        "id": "f5881021-ab63-46d5-bce2-dfe91c5c1111"
    }
}

aux12 = {
    "topic": "@barn/save_recipe_barn",
    "body": {
        "id": "2eff2c98-8615-412b-a485-046cb4710b86",
        "recipe_id": "d0b81134-2a5f-43e7-86fa-3c9b04badf0e"
    }
}

aux13 = {
    "topic": "@barn/search_recipe_barn",
    "body": {
        "id": "fdbe4ceb-2895-40bb-bc19-55190ee3f555",
        "name": "Receita"
    }
}

aux14 = {
    "topic": "@barn/remove_recipe_barn",
    "body": {
        "id": "2eff2c98-8615-412b-a485-046cb4710b86",
        "recipe_id": "d0b81134-2a5f-43e7-86fa-3c9b04badf0e"
    }
}

aux15 = {
    "topic": "@recipe/create_recipe",
    "body": {
        "name": "dive-3",
        "description": "testar dive",
        "userId": "64542159-4fff-40ed-a22c-a3d0d5eb9196",
        "fileId": "fd337eb9-d292-493e-8835-e9f003e326e4",
        "ingredients": [
            {"name": "Ingredient 1", "amount": 1, "unit": "cup"},
            {"name": "Ingredient 2", "amount": 2, "unit": "teaspoon"},
            {"name": "Ingredient 3", "amount": 3, "unit": "gram"},
        ]
    }
}

# "diveId":"b9339c14-daba-4cc9-b736-50ac8da36d88",

aux16 = {
    "topic": "@recipe/list_recipe",
    "body": {
    }
}

aux17 = {
    "topic": "@recipe/reaction_recipe",
    "body": {
        "type": "bão",
        "recipe_id": "ab066eb8-0f05-434d-abad-fc1a8027d94f",
        "user_id": "5ca07281-0e46-4abc-8f1f-54b61ca27631"
    }
}

aux18 = {
    "topic": "@recipe/search_recipe",
    "body": {
        "name": "New"
    }
}

aux19 = {
    "topic": "@dive/create_dive",
    "body": {
        "name": "Açai",
        "description": "açai é legal, nutela é legal!",
        "fileId": "4a3dbb52-1076-4ef4-9c5e-306cf785091b",
        "userId": "f57255d9-afc0-478e-949b-0301f0bc05d0"
    }
}

aux20 = {
    "topic": "@dive/search_dive",
    "body": {
        "name": "a"
    }
}

aux21 = {
    "topic": "@dive/enter_dive",
    "body": {
        "id": "5f3df9b2-3b1e-422d-baff-d9e34a1ad73a",
        "diveId": "8a99fda0-07ee-4632-8747-45288802aa6a"
    }
}

aux22 = {
    "topic": "@dive/exit_dive",
    "body": {
        "user": "5f3df9b2-3b1e-422d-baff-d9e34a1ad73a",
        "new_owner": None,
        "diveId": "8a99fda0-07ee-4632-8747-45288802aa6a"
    }
}

aux23 = {
    "topic": "@dive/exit_dive",
    "body": {
        "user": "f57255d9-afc0-478e-949b-0301f0bc05d0",
        "new_owner": "823e3881-bda1-4f2a-9593-83c8d7fd0044",
        "diveId": "b9339c14-daba-4cc9-b736-50ac8da36d88"
    }
}

aux24 = {
    "topic": "@dive/exit_dive",
    "body": {
        "user": "9badd489-fe3f-4b93-a20d-caaa621d4213",
        "new_owner": "",
        "diveId": "76806064-77aa-4570-b85f-5f87d1152338"
    }
}

aux25 = {
    "topic": "@user/search_users_user",
    "body": {
        "user_id": "75621072-e6b5-49ae-a5ff-424707d534b2",
        "value": "a"
    }
}

aux26 = {
    "topic": "@dive/users_dive",
    "body": {
        "user_id": "823e3881-bda1-4f2a-9593-83c8d7fd0044"
    }
}

aux27 = {
    "topic": "@dive/list_recipes_dive",
    "body": {
        "dive_id": "b9339c14-daba-4cc9-b736-50ac8da36d88"
    }
}

aux28 = {
    "topic": "@search/dive_and_users",
    "body": {
        "user_id": "75621072-e6b5-49ae-a5ff-424707d534b2",
        "value": "a"
    }
}

aux29 = {
    "topic": "@user/profile_user",
    "body": {
        "user_id": "f57255d9-afc0-478e-949b-0301f0bc05d0",
    }
}

aux30 = {
    "topic": "@user/search_in_barn_user",
    "body": {
        "user_id": "75621072-e6b5-49ae-a5ff-424707d534b2",
        "value": "eita"
    }
}

aux31 = {
    "topic": "@user/barn_user",
    "body": {
        "user_id": "75621072-e6b5-49ae-a5ff-424707d534b2"
    }
}

aux32 = {
    "topic": "@ingredients_unit/create_ingredients_unit",
    "body": {
        "name": "Fio"
    }
}

aux33 = {
    "topic": "@ingredients_unit/delete_ingredients_unit",
    "body": {
        "id": "d6bc9f29-e78d-4bc1-b8cd-208303b890d3"
    }
}

aux34 = {
    "topic": "@ingredients_unit/list_ingredients_unit",
    "body": {
       
    }
}

aux35 = {
    "topic": "@dive/update_dive",
    "body": {
        "id": "b9339c14-daba-4cc9-b736-50ac8da36d88",
        "name": "Açai!",
        "description":"teste"
    }
}