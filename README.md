# Reception Company In-processing Questionnaire Application
![Link to logo](https://github.com/CrissyMichelle/In-processingQuestionnaire/blob/main/static/images/ReceptionCompanyLogo.png)
![Link to site](https://replco-in-processing.onrender.com)

## Prototype demo web app for capturing newly arrived personnel data
1. Service members arrive on-island and meet Reception Company Cadre at the airport.
2. Instead of analog pen-and-paper documentation, users of the app fill out forms on their smartphones or tablets.

## Features
1. Users create, read, update, and delete useful information in the backend database.
2. Three types of users, incoming, cadre, and gaining-unit representatives, inherit from the base User type.
3. Passcodes send users emails with spreadsheets containing rows of backend data.
4. A messages area encourages discussion among users of the site by allowing the posting and viewing of blog-style commentary.
5. Another button allows incoming users to privately post After Action Review comments directly to the database.
6. An area with useful phone numbers and addressess provides walking directions from the front gate to Reception Company by leveraging the Google Maps API.
7. A search bar allows for quick lookup of users based on rank and last name, DODID, or gaining unit UIC.
   
## Technology Stack
1. Postgresql for the backend database
2. SQLAlchemy for the object relational mapper
3. Flask web-framework for the server-side functionality (Python)
   1. Flask-WTForms features heavily since the app mainly exists as an automation for collecting data
   2. Jinja2 for templating and rendering of HTML files
   3. Flask-Mail, Pandas, and openxl accomplish the sending of spreadsheets by email, in conjunction with SendGrid
4. JavaScript accomplishes some nifty tricks such as auto-populating report date based on arrival date, and enabling filtering and mapping functionality of the search bar. Cooperating asynchronously with the Google Maps API also depends heavily on JS.
5. CSS styles depend mainly on bootstrap 4.3.1, in conjunction with some jQuery and Font Awesome.

## Important Cybersecurity Considerations
1. The application incorportates basic BCrypt password hashing and vanilla WTForms CSRF protection.
2. As a prototype the app demonstrates capability for ingesting the necessary data for in-processing.
3. Future progress requires robust safeguarding of PII and Authority to Operate approvals.
4. Not intended for use in production. TESTING DATA ONLY. Use at your own risk.

### Contact
crissymichelle@proton.me