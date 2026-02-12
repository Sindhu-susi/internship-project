from behave import given, when, then
from pages.login_page import LoginPage

EMAIL ="sindhu12.sukumaran@gmail.com"
PASSWORD="CareeristIntern7$"

@when("User logs in with valid credentials")
def step_login(context):
    context.app.login_page.login(EMAIL,PASSWORD)

@when("User clicks on settings")
def step_settings(context):
    context.app.dashboard_page.open_settings()

@when("User opens My clients page")
def step_open(context):
    context.app.dashboard_page.open_my_clients()

@then("Verify my clients page open successfully")
def step_verify_page(context):
    context.app.my_clients_page.verify_page_opened()

@then ("My clients page should contain 7 options")
def step_verify_options(context):
    context.app.my_clients_page.verify_all_options_present()

