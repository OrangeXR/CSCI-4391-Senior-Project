# MVP Retrospective 

In 1 to 2 pages, explain:


# What changed from Milestone 1 to Milestone 2
- There have been several changes and improvements to our development of Binny and Bloom recently. The first notable change is that we have implemented better
  ingredient matching. This avoids the issue of the validator not correctly matching ingredients even though they are available in the pantry. In cases such as:
  * "chicken breast" vs "chicken"
  * plural/singular differences
    
- The normalizeIngredient(name): does lowercase and trim whitespaces
  * egg vs eggs
    
- The ingredients_match(req_name, inv_name) handles the ingredients matching
  * chicken thighs and chicken breast → both count as "chicken."
  * milk vs whole milk
  * Ground beef → counts as turkey

- Another change we made was to implement our LLM into our Flask website.
  We made sure to add a small chatbot pop-up that lets the user chat and ask the BinnyBot  to create and suggest recipes.This returns the appropriate validation
  message.   

# What was cut from scope

In the current stage of the application, **virtual farm** was cut from the MVP scope. As this feature was deemed out of scope for this project due to its extensive development requirements, thus allowing the team to prioritize core functionalities in the project timeline.  Additionally, **calorie tracking** was cut from scope to ensure all development efforts align directly with our primary goal of food waste reduction. Furthermore, **spoilage detection** functionality was cut from scope. Due to the lack of integration with physical storage information, the application cannot reliably verify the real-time conditions of inventory items aside from expiration date. Finally, **barcode scanning** is currently cut from scope to focus on key features of application and will consider integrating it later in development.



# What is now truly MVP-ready

At this stage, the application has core features implemented and working cohesively. New users can **create an account**, as well as **log in and log out** without issue, with passwords securely hashed and stored in the database. After logging in, users are presented with a fully functional navigation bar that allows seamless movement throughout the application. The **navigation bar** provides access to the following pages: Home, Inventory, Add item to Inventory, User Profile, Scoreboard, Dashboard and Logout. On the inventory page, users can easily view their stored items through a simple table display. All inventory data is stored in a **database** file named “inventory”, which reliably manages and maintains items data without issues. Additionally, all navigation pages function as expected, as verified through extensive testing during feature integration.Furthermore, the application successfully **integrates AI** within the inventory page through a pop-up chat box, providing convenient access without requiring users to scroll. The AI operates effectively within this interface and can **generate recipes based on user prompts, taking into account the available inventory, item quantities, food allergies and dietary preferences**. The chat box also includes a “Save Recipe” feature, allowing users to effortlessly store generated recipes for later access in their Dashboard. The Dashboard also **displays notifications** for food items that are approaching expiration within three days, helping keep the users informed on their inventory. Finally, the **scoreboard is displayed prominently and correctly ordered ranking from lowest to highest (with lower scores indicating better performance). The scoring system** functions as intended: score increases when items are added based on price and decreases when users choose actions such as use, donate, or compose.


# What still needs work after MVP

- The implementation of decomposing and donations still needs to be included. Another necessary thing we still need to add is a function that decreases the amount of the pantry once the user decides to use a recipe or decompose, etc. In the front end, we still need to continue improving our UI. Improvements towards the LLM still need to be done.


