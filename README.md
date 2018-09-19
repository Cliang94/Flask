Use the Flask box to build the blog project



- Demand analysis



  \- user registration and login

  \- user information management

  \- blog post a reply

  \- blog list display

  \- blog pagination display

  \- blog collection thumb up

  \- search, statistics, sorting,...



  Project preparation



  \- create related directories and files based on directory structure

  \- write configuration file (configuration class)

  \- use the configuration file: define the factory function to create the app to complete the initialization configuration, then return, and call the factory function in the start control file

  \- add various extensions (import class libraries, create objects, initialize functions) and call the initialization functions where you can see the app

  \- add various blueprints and wrap functions to complete the registration, using similar routines to add extensions.

  \- port the mail sending function, which is actually the mail sending function pasted on the fourth day.

  \- customize the basic template of the project and complete the test by customizing the home page



  User management



  \- user registration and activation

  \- create template file for user registration

  \- add the user-registered view function and render the registered template file

  \- add a click-to-jump link to the navigation bar

  \- add user registration form class and finish rendering and validation

  \- register to activate mail delivery

  \- activate messages to carry user information

  \- account activation verification processing

  \- detailed information display

  \- add click jump links and logic

  \- display effect of writing details page



  Blog is published



  \- add post form and validation logic

  \- add the blog model to save the blog

  \- add blog check save