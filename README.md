# **Elite PT Pro**

This website was created as the 3rd Milestone Project for Code Institute's web application development course.

[**__link to deployed site here__**](https://elite-pt-pro-a6d44ea21364.herokuapp.com/)
<br><br>

<img src="eliteptpro/docs/readme-images/responsive-mockup.png">
<br><br>

# Contents

* [User Experience](#user-experience-ux)
    * [Owner Goals](#owners-goals)
    * [Visitor Goals](#visitor-goals)
* [Design](#design)
    * [Wireframes](#wireframes)
    * [Database Schema](#database-schema)
    * [Materialize](#materialize)
    * [Images](#images)
* [Features](#features)
    * [Multi-page Features](#multi-page-features)

<br><br>

# User Experience

A local gym "Elite Fitness" require an app for their members to easily book and manage PT sessions, and for thier Personal trainers to keep a track of upcoming sessions.
<br><br>

## Owners Goals
- Give my small gym clients a system to book 1 hour pt sessions
- Give my pt employees a system to track booked sessions
<br><br>

## Visitor Goals
As user:
- I want to immediately identify the purpose of the site
- I want navigation to be simple and intuitive
- I want to be able to view the site on any device
- I want to be able to easily navigate to the homepage incase of broken link or site error
<br><br>

As a logged out user: 
- I want to be able to login/signup to the service
<br><br>

As a logged in gym member user:
- I want to be able to book a 1 hour pt session
- I want to be able to see sessions I have currently booked and edit/delete them
<br><br>

As an employee/pt user:
- I want to be able to see what sessions users have booked with me
- I want to be able to set days that im unavailable for
- I want to be able to edit/delete user sessions I cannot make
<br><br>

As a managment user
- I want to be able to add/edit users both members of gym and trainers
- I want to be able to manage Holidays of the trainers
- I want to be able to see all session booked with pt employees and edit/delete them
<br><br>

# Design

## WireFrames 

Wireframes created using balsamiq.

<details>
<summary>Homepage Desktop</summary>
<br>
<img src="eliteptpro/docs/wireframes/homepage-desktop.png">
</details>
<details>
<summary>Homepage Mobile</summary>
<br>
<img src="eliteptpro/docs/wireframes/homepage-mobile.png">
</details>
<details>
<summary>Register Desktop</summary>
<br>
<img src="eliteptpro/docs/wireframes/register-desktop.png">
</details>
<details>
<summary>Register Mobile</summary>
<br>
<img src="eliteptpro/docs/wireframes/register-mobile.png">
</details>
<details>
<summary>Login Desktop</summary>
<br>
<img src="eliteptpro/docs/wireframes/login-desktop.png">
</details>
<details>
<summary>Login Mobile</summary>
<br>
<img src="eliteptpro/docs/wireframes/login-mobile.png">
</details>
<details>
<summary>My Sessions Desktop</summary>
<br>
<img src="eliteptpro/docs/wireframes/my-sessions-desktop.png">
</details>
<details>
<summary>My Sessions Mobile</summary>
<br>
<img src="eliteptpro/docs/wireframes/my-sessions-mobile.png">
</details>
<details>
<summary>PT Sessions Desktop</summary>
<br>
<img src="eliteptpro/docs/wireframes/pt-sessions-desktop.png">
</details>
<details>
<summary>PT Sessions Mobile</summary>
<br>
<img src="eliteptpro/docs/wireframes/pt-sessions-mobile.png">
</details>
<details>
<summary>Book/Edit Session Desktop</summary>
<br>
<img src="eliteptpro/docs/wireframes/book-session-desktop.png">
</details>
<details>
<summary>Book/Edit Session Mobile</summary>
<br>
<img src="eliteptpro/docs/wireframes/book-session-mobile.png">
</details>
<details>
<summary>Add/Edit Holiday Desktop</summary>
<br>
<img src="eliteptpro/docs/wireframes/book-session-desktop.png">
</details>
<details>
<summary>Add/Edit Holiday Mobile</summary>
<br>
<img src="eliteptpro/docs/wireframes/book-session-mobile.png">
</details>
<details>
<summary>Add/Edit Holiday Desktop</summary>
<br>
<img src="eliteptpro/docs/wireframes/holiday-form-desktop.png">
</details>
<details>
<summary>Add/Edit Holiday Mobile</summary>
<br>
<img src="eliteptpro/docs/wireframes/holiday-form-mobile.png">
</details>
<details>
<summary>Add/Edit Holiday Desktop</summary>
<br>
<img src="eliteptpro/docs/wireframes/holiday-form-desktop.png">
</details>
<details>
<summary>Add/Edit Holiday Mobile</summary>
<br>
<img src="eliteptpro/docs/wireframes/holiday-form-mobile.png">
</details>
<details>
<summary>Management Desktop</summary>
<br>
<img src="eliteptpro/docs/wireframes/manage-desktop.png">
</details>
<details>
<summary>Management Mobile</summary>
<br>
<img src="eliteptpro/docs/wireframes/manage-mobile.png">
</details>
<br><br>

## Database Schema

Schema for PostgreSQL database was created on [Diagrams.net](https://app.diagrams.net/)
<details>
<summary>DB Schema</summary>
<br>
<img src="eliteptpro/docs/readme-images/db-scherma.png">
</details>
<br><br>

## Materialize

Materialize CSS was used and customized for the main part of the front-end development.
<br><br> 

## Images 

All images were sourced from [Unsplash](https://unsplash.com/), [Convertio](https://convertio.co/) was used to convert the images into webp and [TinyPNG](https://tinypng.com/) to compress the image even further. Main Logo in the Header was created in Adobe.
<br><br>


# Features

## Multi-page Features

### Navbar

The navbar is present across all pages ecxept for custom pages to catch errors. On mobile devices collapses to a hamburger icon which opens as a sidenav. The links visible are dependant on if the user is logged in and what level of user they are.

<details>
<summary>Navbar Logged Out</summary>
<br>
<img src="eliteptpro/docs/readme-images/navbar-logged-out.png">
</details>
<br><br>
<details>
<summary>Navbar Member Logged In</summary>
<br>
<img src="eeliteptpro/docs/readme-images/navbar-member-logged-in.png">
</details>
<br><br>
<details>
<summary>Navbar Trainer Logged In</summary>
<br>
<img src="eliteptpro/docs/readme-images/navbar-member-logged-in.png">
</details>
<br><br>
<details>
<summary>Navbar Admin Logged In</summary>
<br>
<img src="eliteptpro/docs/readme-images/navbar-admin-logged-in.png">
</details>
<br><br>

### Footer

Footer is present across all pages ecxept for custom pages to catch errors, with a disclaimer and links to GitHub profile and LinkedIn profile.

<details>
<summary>Footer</summary></summary>
<br>
<img src="eliteptpro/docs/readme-images/footer.png">
</details>
<br><br>

### Favicon

Favicon was made by cropping the the first part of the navbar logo that was created. Made at [Favicon](https://favicon.io/).

<details>
<summary>Favicon</summary></summary>
<br>
<img src="eliteptpro/docs/readme-images/logo-for-favicon.png">
</details>
<br><br>

### Homepage

Homepage is available to all users but the content differs dependant on wether or not the user is logged in and what user is logged in i.e member, trainer, admin.

<details>
<summary>Homepage Logged Out</summary></summary>
<br>
<img src="eliteptpro/docs/readme-images/homepage-logged-out.png">
</details>
<br><br>
<details>
<summary>Homepage Member Logged In</summary></summary>
<br>
<img src="eliteptpro/docs/readme-images/member-homepage.png">
</details>
<br><br>
<details>
<summary>Homepage Trainer Logged In</summary></summary>
<br>
<img src="eliteptpro/docs/readme-images/trainer-homepage.png">
</details>
<br><br>
<details>
<summary>Homepage Admin Logged In</summary></summary>
<br>
<img src="eliteptpro/docs/readme-images/admin-homepage.png">
</details>
<br><br>

### Modals

Modals are present wherever a delete button is clicked to defend against accidental deletion.

<details>
<summary>Modal</summary></summary>
<br>
<img src="eliteptpro/docs/readme-images/modal.png">
</details>
<br><br>