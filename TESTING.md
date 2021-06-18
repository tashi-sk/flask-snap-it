## Automated Testing

### CSS Validation Check

The website's CSS passed the W3C CSS Validation checker:

**CSS: Pass**

![W3c css validation](https://github.com/tashi-sk/flask-snap-it/blob/master/wireframes/w3c-css-validation.png "Snap-it w3c validation")

### W3C Markup Validation Check

The website's HTML passed the W3C HTML Validation checker:

**Homepage: Pass**

![home-page html5 validation](https://github.com/tashi-sk/flask-snap-it/blob/master/wireframes/home-testing-warning.png "Snap-it html validation")

**Login Page: was Fail first**

![login-page html5 test error](https://github.com/tashi-sk/flask-snap-it/blob/master/wireframes/login-testing-error.png "Snap-it html test fail")

**Issues & Fixes**
  * test was failed because of different ids on passwrod label and  password input field
  - ID's were edited to same name 
  * test was passed with one warning after fix
  
![login-page html5 test warning](https://github.com/tashi-sk/flask-snap-it/blob/master/wireframes/login-testing-warning.png "Snap-it html test pass")

**Register Page: was Fail first**

![Register-page html5 test error](https://github.com/tashi-sk/flask-snap-it/blob/master/wireframes/register-testing-error.png "Snap-it html test fail")

**Issues & Fixes**
  * test was failed because of different ids on passwrod label and  password input field
  - ID's were edited to same name 
  * test was passed with one warning after fix
  
![login-page html5 test warning](https://github.com/tashi-sk/flask-snap-it/blob/master/wireframes/register-testing-warning.png "Snap-it html test pass")


### Python PEP8 Compliant

The website's Python code was checked for [PEP8 compliance](http://pep8online.com/) and returned no errors:

![python pep8 check](https://github.com/tashi-sk/flask-snap-it/blob/master/wireframes/pep8-testing.png "Snap-itpep8 check")


### JSHint JavaScript Test

The website's JavaScript was tested for errors using [JSHint](https://jshint.com/).

**Issues and Fixes**

JSHint returned 6 warnings - all those warnings were because of missing semicolon.


### Web Accessibility 

The website's homepage was tested to ensure it was accessible to people with disabilities using the [Web Accessibility](https://www.webaccessibility.com/) checker.

![web accessibility test](https://github.com/tashi-sk/flask-snap-it/blob/master/wireframes/web-accessibility-testing.png "Snap-it web accessibility test")

**Issues and Fixes**

  * Three violations were highlighted to ensure link text is meaningful within context for the social media links. As these were icons, and did not contain text, I left these       unchanged. Overall, the homepage received a good score of 89%.
 
 ## Mannual Testing
 * Manual testing was carried out on:
    * Desktop: Dell
    * Tablets: Apple
    * Mobile: Apple, Samsung and Huawei
    * Browsers: Chrome, Safari, Edge and Internet Explorer

* During manual testing the following tests were carried out:
    * All links worked and took the user to the desired target. These links included:
        - all nav bar links (including logo)
        - home page Signup and login links
        - Profile page buttons and links
        - login button and Register link on login page
        - Register button and login link on Register page
        - All footer links
        - All links and buttons on comments page, upload/edit pages 
        - All links on 404.html and 500.html
        - All links on community page
        - pagination links
        - all form buttons and modals

     - The nav bar collapsed in smaller screens and became reachable through a hamburger icon.
     - If no user is logged in, any url requiring a valid username redirect user to 404 page which includes a link back to the home page.

## Testing User Stories
* User
 * As a User, I want that website layout is easy to understand and navigate through out all the pages.
     - The pages are easy to navigate through navbar on top of each page. 

 * As a User, I want to be able to register myself to the website.
     - on homepage there is a button for signup if user wants to register

 * As a User, I want to upload post from my profile.
     - To upload post from profile there is upload button on profile page if user wants to upload post

 * As a User, I want to be able to Edit and Delete my post.
     - on profile page when user have post, edit and delete button are available at bottom of every post

 * As a User, I want to be able to comment on post.
     - to comment on post user must login/register first to access community page. there is a comment button on every post. which redirect user to comments page of a post

 * As a user, i want to be able to edit and delete my comments.
     - user can edit and delete his own comment only. if there is a comment on post by a user. a dropdown icon will be visible. clicking that will show edit and delelte buttons

 * As a User, I want to be able to see other user post.
     - every register user can access community page to view other user post and comment.

 * As a user, I want to be able to contact site owner.
     - there is contact detail available on footer section of site on every page. 

 * As a user, i want to be able to see social media link relate to website.
     - Social media links are also available at very bottom of every page at footer section.

* Returning user 
    * As a returning user, i would like to see if there is any comment on my post.
     - comments are available to view with in comment section of post
    
    * As a returning user, i i would like to see if there is any new post from other users.
     - new post will be available to view on community page for register users.
    
