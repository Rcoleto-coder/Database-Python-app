import ui
import db

def add_person():
    data = ui.dialog("Add Person", (
        "First Name",
        "Last Name",
        ("Birthday (yyyy-mm-dd)", "^\d\d\d\d-\d\d-\d\d$|^$"),
        # NOTE: This regex does not truly match valid email addresses
        # See https://stackoverflow.com/questions/201323/how-can-i-validate-an-email-address-using-a-regular-expression
        ("Email: ", ".*@.*|^$"),
        ("Phone (###-###-####): ", "^\d\d\d-\d\d\d-\d\d\d\d$|^$"),
        "Address line 1",
        "Address line 2",
        "City",
        "Province/State",
        "Country",
        "Post code"
    ))

    db.add_person(data)

def delete_person():
    ids = db.get_person_ids()
    id = int(ui.constrained_input("ID of person to delete: ", ids, "There is no person with that ID" ))

    db.delete_person(id)

def list_people():
    print()
    selection = ui.options("Sort by...", list(zip(db.PERSON_LIST_DISPLAY_FIELDS, db.PERSON_LIST_DISPLAY_FIELD_HEADINGS)))
    data = db.get_people_list(order_by=selection)
    
    print()
    ui.print_heading("People List")
    print()
    ui.table(db.PERSON_LIST_DISPLAY_FIELD_HEADINGS, data)
    
def quit():
    exit(0)


while True:
    ui.menu("Main Menu", (
        ("_List people", list_people),
        ("_Add person", add_person),
        ("_Delete person", delete_person),
        ("_Quit", quit)
    ))