# Created by sindh at 2/11/2026
Feature: Verify My Clients Page
# Enter feature name here
  # Enter feature description here

  Scenario:Verify My Clients Options
  Given User opens the main page
  When  User logs in with valid credentials
  And User clicks on settings
  And User opens My clients page
  Then Verify my clients page open successfully
  And My clients page should contain 7 options

    # Enter steps here