import sqlite3

def get_connection():
    """Returns a connection object for the application database, 
        with the row factory set to Row so that row data can be referenced using
        either index or column names"""
    connection = sqlite3.connect("data.sqlite")

    # Allow for indexing of rows using either integers or column names
    # See https://docs.python.org/3/library/sqlite3.html#row-objects
    connection.row_factory = sqlite3.Row  

    return connection

def add_person(data):
    """Inserts the given data (must be a list of values) as a new person row.
        The values must correspond to the first name, last name, birthday, email
        phone, address line 1, addres line 2, city, province, country, and postcode
        of a person, in that specific order.
        """
    # TODO: complete this function
    with get_connection() as cnx:
        cursor = cnx.cursor()
        sql = """INSERT INTO person (
            first_name,
            last_name,
            birthday,
            email,
            phone,
            address_line1,
            address_line2,
            city,
            prov,
            country,
            postcode) VALUES (?,?,?,?,?,?,?,?,?,?,?);"""
        return cursor.executemany(sql,[data])

def delete_person(id):
    """Deletes the person with the given id from the person table
        id must be an id that exists in the person table"""
    # TODO: complete this function
    with get_connection() as cnx:
        cursor = cnx.cursor()
        sql = """DELETE FROM person WHERE person_id = (?);"""
        return cursor.execute(sql,[id]).fetchall

# A list of (column name, pretty label) tuples
PERSON_LIST_DISPLAY_FIELDS = ('person_id', 'first_name', 'last_name', 'birthday', 'email', 'phone', 'address')
PERSON_LIST_DISPLAY_FIELD_HEADINGS = ("ID", "First Name", "Last Name", "Birthday", "Email", "Phone", "Address")
def get_people_list(order_by):

    assert order_by in PERSON_LIST_DISPLAY_FIELDS, "The order_by argument must be one of: " + ", ".join(PERSON_LIST_DISPLAY_FIELDS)

    with get_connection() as cnx:
        cursor = cnx.cursor()
        sql = """SELECT person_id, first_name, last_name, birthday, email, phone,
                    address_line1 || '\n' || address_line2 || '\n' || 
                    city || ', ' || prov || ', ' || country || '\n' || postcode as address
                FROM person"""

        if order_by:
            sql += " ORDER BY " + order_by
        
        return cursor.execute(sql).fetchall()

def get_person_ids():
    """Returns a list of the person ids that exist in the database"""
    with get_connection() as cnx:
        cursor = cnx.cursor()
        sql = """SELECT person_id FROM person"""
        return [ row[0] for row in cursor.execute(sql).fetchall() ]
