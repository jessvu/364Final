# SI 364 - Winter 2018 - Final Project

**Final project submission deadline: April 20, 2018 at 11:59 pm**

**Total: 3200 points**

This application will allow users to register and sign in, and search and save business information (restaurants, salons, etc.) with the Yelp API. Once logged in users will only be able to see the businesses that they have saved and not other users' saved businesses. Users will be able to search for businesses by their name or food category and by location. The 10 best matches will be returned with the address, ratings, and url. My app will also allow users to save their businesses to lists- maybe by category of food, service, location, or however they wish. 

Without logging in, users can search for businesses and see past searches and all businesses that came up as results. Registered users can create lists of businesses and rate businesses.The app allows users to delete entire lists and individual items in their lists, usrs can also update the name of their lists as well. All search results come back as links to their yelp pages where users can learn more about the businesses.

There are no additional modules that need to be installed to run this application. To make API request, import your own api key assigned to variable "key" in a file called "yelp_key".

I kept my database name as 'SI364projectplanJESSVU' because when I changed it, my code stopped running as it should.


## Routes that exist and name of template each should render:
- '/login' --> render_template('login.html')
- '/logout' --> 'redirect(url_for('index'))
- '/register' --> if form.validate_on_submit(): --> redirect(url_for('login')), render_template('register.html')
- '/secret' --> return "Only authenticated users can do this! Try to log in or contact the site admin."
- '/' --> if form.validate_on_submit(): --> redirect(url_for('search_results')), render_template('base.html')
- '/businesses_searched/<name>/<location>' --> render_template('searched_businesses.html')
- '/getrating' --> render_template('get_rating.html')
- '/all_ratings' --> render_template('ratings.html')
- '/search_terms' --> render_template('search_terms.html')
- '/all_businesses' --> render_template('all_businesses.html')
- '/create_business_list' --> if request.method == 'POST' --> redirect(url_for('lists')), render_template('create_business_list.html')
- '/lists' --> render_template('lists')
- '/list/<id_num>' --> render_template('list.html')
- '/update/<lst>' --> render_template('update_business.html')
- '/delete_business/<business>' --> render_template('delete_business.html')
- '/delete/<lst>' --> render_template('delete_list.html')
- '/ajax' --> return x

- [ ] **Ensure that your `SI364final.py` file has all the setup (`app.config` values, import statements, code to run the app if that file is run, etc) necessary to run the Flask application, and the application runs correctly on `http://localhost:5000` (and the other routes you set up).**Your main file must be called** `SI364final.py`**, but of course you may include other files if you need.**

- [ ] **A user should be able to load `http://localhost:5000` and see the first page they ought to see on the application.**

- [ ] **Include navigation in `base.html` with links (using `a href` tags) that lead to every other page in the application that a user should be able to click on. (e.g. in the lecture examples from the Feb 9 lecture, [like this](https://www.dropbox.com/s/hjcls4cfdkqwy84/Screenshot%202018-02-15%2013.26.32.png?dl=0) )**

- [ ] **Ensure that all templates in the application inherit (using template inheritance, with `extends`) from `base.html` and include at least one additional `block`.**

- [ ] **Must use user authentication (which should be based on the code you were provided to do this e.g. in HW4).**

- [ ] **Must have data associated with a user and at least 2 routes besides `logout` that can only be seen by logged-in users.**

- [ ] **At least 3 model classes *besides* the `User` class.**

- [ ] **At least one one:many relationship that works properly built between 2 models.**

- [ ] **At least one many:many relationship that works properly built between 2 models.**

- [ ] **Successfully save data to each table.**

- [ ] **Successfully query data from each of your models (so query at least one column, or all data, from every database table you have a model for) and use it to effect in the application (e.g. won't count if you make a query that has no effect on what you see, what is saved, or anything that happens in the app).**

- [ ] **At least one query of data using an `.all()` method and send the results of that query to a template.**

- [ ] **At least one query of data using a `.filter_by(...` and show the results of that query directly (e.g. by sending the results to a template) or indirectly (e.g. using the results of the query to make a request to an API or save other data to a table).**

- [ ] **At least one helper function that is *not* a `get_or_create` function should be defined and invoked in the application.**

- [ ] **At least two `get_or_create` functions should be defined and invoked in the application (such that information can be saved without being duplicated / encountering errors).**

- [ ] **At least one error handler for a 404 error and a corresponding template.**

- [ ] **At least one error handler for any other error (pick one -- 500? 403?) and a corresponding template.**

- [ ] **Include at least 4 template `.html` files in addition to the error handling template files.**

  - [ ] **At least one Jinja template for loop and at least two Jinja template conditionals should occur amongst the templates.**

- [ ] **At least one request to a REST API that is based on data submitted in a WTForm OR data accessed in another way online (e.g. scraping with BeautifulSoup that *does* accord with other involved sites' Terms of Service, etc).**

  - [ ] **Your application should use data from a REST API or other source such that the application processes the data in some way and saves some information that came from the source *to the database* (in some way).**

- [ ] **At least one WTForm that sends data with a `GET` request to a *new* page.**

- [ ] **At least one WTForm that sends data with a `POST` request to the *same* page. (NOT counting the login or registration forms provided for you in class.)**

- [ ] **At least one WTForm that sends data with a `POST` request to a *new* page. (NOT counting the login or registration forms provided for you in class.)**

- [ ] **At least two custom validators for a field in a WTForm, NOT counting the custom validators included in the log in/auth code.**

- [ ] **Include at least one way to *update* items saved in the database in the application (like in HW5).**

- [ ] **Include at least one way to *delete* items saved in the database in the application (also like in HW5).**

- [ ] **Include at least one use of `redirect`.**

- [ ] **Include at least two uses of `url_for`. (HINT: Likely you'll need to use this several times, really.)**

- [ ] **Have at least 5 view functions that are not included with the code we have provided. (But you may have more! *Make sure you include ALL view functions in the app in the documentation and navigation as instructed above.*)**


## Additional Requirements for additional points -- an app with extra functionality!

**Note:** Maximum possible % is 102%.

- **[ ] (100 points) Include a use of an AJAX request in your application that accesses and displays useful (for use of your application) data.**
- [ ]  (100 points) Create, run, and commit at least one migration.
- [ ] (100 points) Include file upload in your application and save/use the results of the file. (We did not explicitly learn this in class, but there is information available about it both online and in the Grinberg book.)
- [ ]  (100 points) Deploy the application to the internet (Heroku) — only counts if it is up when we grade / you can show proof it is up at a URL and tell us what the URL is in the README. (Heroku deployment as we taught you is 100% free so this will not cost anything.)
- [ ]  (100 points) Implement user sign-in with OAuth (from any other service), and include that you need a *specific-service* account in the README, in the same section as the list of modules that must be installed.



