# MVP Known Issues 

List the remaining issues honestly.
Required categories:
## Ingredient matching edge cases:
- When trying to generate recipes, if there is a lot of expired ingredients it will keep trying to generate recipes using expired ingredients and fail
  
## Unit conversion edge cases:
- n/a

## UI limitations:
- When generating a recipe, the chat window will close and need to be manually opened again to view recipe or recipe generation failure message
- The spacing could be improved when viewing inventory
  
## Data quality assumptions:
- No real way to evaluate quality of generated recipes besides using personal opinions on recipes
  
## Anything the team would fix next with one more sprint:
- Sometimes the LLM will generate the same recipes continuously when based on the same inventory
