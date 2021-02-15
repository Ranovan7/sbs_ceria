from app import SessionLocal
from app import engine
from app.models import Base, User

import typer

cli_app = typer.Typer()


@cli_app.command()
def create_db():
    try:
        Base.metadata.create_all(engine, Base.metadata.tables.values(), checkfirst=True)
        print("DB Created.")
        print("-- note : existing table name is ignored...")
    except Exception as e:
        print(f"Failed at Creating DB : {e}")


@cli_app.command()
def create_admin(username: str):
    password = input("-- password :")
    try:
        db = SessionLocal()

        admin = User(username=username, role=1)
        admin.set_password(password)

        db.add(admin)
        db.commit()

        print(f"Successfully create Admin with username : '{admin.username}'")
    except Exception as e:
        print(f"Failed at Creating Admin : {e}")


@cli_app.command()
def import_master(table: str, filepath: str):
    print(filepath)
    if table == 'sales':
        print(f"Importing {table.title()}")
    elif table == 'antar':
        print(f"Importing {table.title()}")
    elif table == 'supplier':
        print(f"Importing {table.title()}")
    elif table == 'pelanggan':
        print(f"Importing {table.title()}")
    else:
        print("Table not found or not registered.")


if __name__ == "__main__":
    cli_app()
