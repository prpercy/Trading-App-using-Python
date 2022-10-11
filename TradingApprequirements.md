
Trading App
Requirements Specification
Document

Pravin Patil
Liset Lopez
William Wolfenbarger
Esteban Lopen
Jorge Villacreses
10/08/2022


Revisions


Version
Primary Author(s)
Description of Version
Date Completed
First Draft
Team
Created sample template

10/08/2022


Review & Approval

Requirements Document Approval History
Approving Party
Version Approved
Signature
Date



 
Requirements Document Review History
Reviewer
Version Reviewed
Signature
Date


Contents


1. Introduction	3
1.1 Introduction	3
1.2 Scope of this Document	3
2. General Description	3
2.1 Product Functions	3
2.2 User Problem Statement	3
2.3 General Constraints	3
3. Functional Requirements	3
3.1 User creation and maintenance	3
3.2 Trade S&P 500 stocks	4
3.3 Perform portfolio simulation	4
3.4 Evaluate risk metrics	4
4. Interface Requirements	4
4.1 User Interfaces	4
5. Performance Requirements	4
6. Other non-functional attributes	4
6.1 Security	4
6.2 Compatibility	5
6.3 Reliability	5
6.4 Maintainability	5
6.6 Extensibility	5
7. Preliminary Use Case Models and Sequence Diagrams	5
7.1 Use Case Model	5
7.2 Sequence Diagrams	6
7.2.1 Create User	6
8. Appendices	7
8.1 xxx	7


1. Introduction
1.1 Introduction
The purpose of this document is to define and describe the requirements of the project and to spell out the system’s functionality and its constraints.

1.2 Scope of this Document
Goal is to cover all topics learned through Module 1 to 7 and incorporate our learning as part of project implementation.
Scope of this document is “Trading App’ that’s being developed by Project Team.

2. General Description
2.1 Product Functions
User would be able to trade stocks, perform portfolio analysis and generate relevant reports.

2.2 User Problem Statement
Users would like to have a trading platform, that not only allows him/her to trade the stocks, but also perform portfolio or name specific analysis and generate various useful reports.

2.3 General Constraints
In absence of formal GUI, the app needs to use command line interface. Additionally, app would, for now, use SQL lite database.
3. Functional Requirements
3.1 User creation and maintenance
Create User or sign up
For new user, sign up is mandatory. Input for the sign up would be ‘user name’ and ‘password’. If ‘user name’ already exists then the user would be prompted to input new user name.
Sign in
For a recurring user, user can sign in. User will enter ‘user name’ and ‘password’. If credentials are correct (checked against user credentials stored in database during sign up process), allow user to login into the app system.
Delete or deactivate user profile
User can deactivate user profile using deactivate account functionality.
Update user fund
Add amount with which user can trade. Amount must be integer only. Also allow user to update the amount. It will be officially named as “available fund to trade”.
3.2 Trade S&P 500 stocks
Buy stock
Buy single name stock if “available funds to trade” allows it to do so. Update the available funds to trade once user buys the stock.
Sell stock
Sell single name stock if it was already purchased (if user owns it). If user does not own it, throw an error that “No long position in the stock to sell”. In case, the sell goes through, improve the “available funds to trade” by proceeds of sell.

3.3 Perform portfolio simulation
Perform portfolio monte carlo simulation
Plot the simulation paths
Generate pie chart for sector weighting
3.4 Evaluate risk metrics
Calculate and present sharpe ratio for single name stocks or portfolio
Calculate and present beta for single name stocks or portfolio
Calculate and present variance/covariance for the stocks
Calculate and present Alpha relative to S&P 500

4. Interface Requirements
4.1 User Interfaces


4.1.1 GUI: Not available in this version
4.1.2 CLI: Use command line interface.
4.1.3 API: Use Nasdaq or Alpaca API
4.1.4 Database: Use SQL Lite database 


5. Performance Requirements
Trading App should have reasonable performance. Too much delay will make app unusable and undesirable.


6. Other non-functional attributes
6.1 Security

All user names and passwords are stored in database and should not be accessible to other users.
6.2 Compatibility

This system will be compatible with any computer that has Microsoft Office Professional 2007 or later installed (whether PC or Mac)
6.3 Reliability

Reliability is one of the key attributes of the system. Back-ups will be made regularly so that restoration with minimal data loss is possible in the event of unforeseen events. The system will also be thoroughly tested by all team members to ensure reliability.
6.4 Maintainability

The system shall be maintained by Project 1 Team.

6.6 Extensibility
The system shall be designed and documented in such a way that anybody with an understanding of Python shall be able to extend the system to fit their needs with the team’s basic instructions.


7. Appendices
7.1 xxx  
