# austinDB
![image](https://raw.githubusercontent.com/austinkilduff/austinDB/main/austinDB.png)

Installing system packages, setting up SQL databases, and adding 10 more imports to your project is for chumps. What's an ORM? Who cares. Let's just use JSON files for our databases.


## Usage

A basic database can be setup with a table like this:

    import austinDB
    db = austinDB.Database("my_database.json")
    db.create_table("dogs", ["name", "age", "breed"])
    dogs = db.read_table("dogs")

Create a row like this:

    dogs.create(["Mose", 1, "Aussie mix"])

Read all matching rows in any of the following ways:

    dogs.read() # For all rows
    dogs.read(["name"]) # For all names
    dogs.read(["breed"], ["name"], [(lambda name: name == "Mose")]) # For all breeds where name is Mose
    dogs.read(["breed"], ["name", "age"], [(lambda name: name == "Mose"), (lambda age: age < 5)]) # Multiple conditions!

Update a row like this:

    dogs.update(["age"], [2], ["name"], [(lambda name: name == "Mose")]) # Update age to 2

Delete a row like this:

    dogs.delete(["name"], [(lambda name: name == "Mose")]) # Bye Mose!

Tables can be pretty-printed like this:

    dogs.print()

Tables can be dropped like this:

    db.delete_table("dogs")

You can do cool stuff like this too:

    db.create_table("dogs", ["name", "owner_name"])
    dogs = db.read_table("dogs")
    dogs.create(["Mose", "Austin"])
    dogs_result = dogs.read(["owner_name"], ["name"], [(lambda name: name == "Mose")])
    mose_owner = dogs_result[0][0] # 0th row, 0th field

    db.create_table("owners", ["name", "favorite_color"])
    owners = db.read_table("owners")
    owners.create(["Austin", "orange"])
    owners_result = owners.read(["favorite_color"], ["name"], [(lambda name: name == mose_owner)])
    favorite_color = owners_result[0][0] # Gets us "orange"!

So intuitive! Why would you do it any other way?
