# Create a clear demo scenario showing the system refusing when pantry has insufficient/incompatible ingredients

Scenarios 
1. The user has a vegetarian inventory, so we will test for incompatible ingredients by asking for a meat-based recipe, such as chicken or beef stew.

> First, we log in with our username, which is vegetarian. This only contains vegetarian-safe ingredients based on the user's dietary needs:
>
> <img src="/docs/ImagesPt2/veg_user_info.png" width="400">

> Then we go into the DB, and we can confirm that there are only vegetarian options.
>
> <img src="/docs/ImagesPt2/veg_DB.png" width="400">

> In our Binny Chat window, we ask: Hi chat! Can you make me a chicken stew or beef stew, please?
>
>  <img src="/docs/ImagesPt2/veg_prompt.png" width="500">

>The validator runs, and we end up getting this response:
>
><img src="/docs/ImagesPt2/veg_response.png" width="600">

2. The user has an empty inventory, so we will test insufficient ingredients. Basically, asking for anything should not give us any recipe response.

> First, we log in with our username, which is empty. Which contains no ingredients
>
> <img src="/docs/ImagesPt2/empty_user_info.png" width="400">

> Then we go into the DB, and we can confirm that there’s nothing on it.
>
> <img src="/docs/ImagesPt2/empty_DB.png" width="400">

> In our Binny Chat window, we ask: Hi chat! Can you make me a chicken taco?
>
> <img src="/docs/ImagesPt2/empty_prompt.png" width="600">

>The validator runs, and we end up getting this response:
>
> <img src="/docs/ImagesPt2/empty_response.png" width="600">
