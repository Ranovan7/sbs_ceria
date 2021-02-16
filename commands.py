from fastapi import Depends

from app import SessionLocal
from app import engine, db_session
from app.models import Base, User, Sales, Antar, InfoPajak, Supplier, Pelanggan, Obat
from app.schemas import BaseSales, MasterSupplier, MasterPelanggan, BaseObat

import typer
import csv

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
        db.refresh(admin)
        db.close()

        print(f"Successfully create Admin with username : '{admin.username}'")
    except Exception as e:
        print(f"Failed at Creating Admin : {e}")


@cli_app.command()
def import_master(table: str, filepath: str):
    print(f"Importing {table.title()}")

    data = csv2dict(filepath)
    if table == 'sales':
        add_sales(data)
    elif table == 'antar':
        add_antar(data)
    elif table == 'supplier':
        add_supplier(data)
    elif table == 'pelanggan':
        add_pelanggan(data)
    elif table == 'obat':
        add_obat(data)
    else:
        print("Table not found or not registered.")


def csv2dict(filepath: str):
    try:
        with open(filepath, 'r') as data:
            return [d for d in csv.DictReader(data)]
    except Exception as e:
        print(f"Error Occured when reading csv : {e}")
        return None


def insert_data(row):
    db = SessionLocal()
    db.add(row)
    db.commit()
    db.refresh(row)
    db.close()

    return row


def add_sales(sales):
    if not sales:
        print("No Data Found")

    for sale in sales:
        try:
            data = BaseSales(**sale)
            row = Sales(
                kode=data.kode.lower(), nama=data.nama.title(),
                alamat=data.alamat.title(), kota=data.kota.title(),
                telepon=data.telepon, keterangan=data.keterangan.title()
            )
            row = insert_data(row)
            print(f"-- added {row.nama}")
        except Exception as e:
            print(f"Error : {e}")


def add_antar(antars):
    if not antars:
        print("No Data Found")

    for antar in antars:
        try:
            data = BaseSales(**antar)
            row = Antar(
                kode=data.kode.lower(),
                nama=data.nama.title(),
                alamat=data.alamat.title(),
                kota=data.kota.title(),
                telepon=data.telepon,
                keterangan=data.keterangan.title()
            )
            row = insert_data(row)
            print(f"-- added {row.nama}")
        except Exception as e:
            print(f"Error : {e}")


def add_pelanggan(pelanggans):
    if not pelanggans:
        print("No Data Found")

    for pelanggan in pelanggans:
        try:
            data = MasterPelanggan(**pelanggan)

            pajak = InfoPajak(
                npwp=data.npwp,
                ppn=data.ppn_bool(),
                pkp=data.pkp,
                nama=data.nama_pajak,
                alamat=data.alamat_pajak
            )
            pajak = insert_data(pajak)

            db = SessionLocal()
            sales = db.query(Sales).filter(Sales.kode == data.kode_sales.lower()).first()
            db.close()

            row = Pelanggan(
                kode=data.kode.lower(),
                nama=data.nama.title(),
                alamat=data.alamat.title(),
                kota=data.kota.title(),
                telepon=data.telepon,
                keterangan=data.keterangan.title(),
                limits=data.limit_int(),
                toleransi=data.toleransi_int(),
                diskon=data.diskon_float(),
                info_pajak_id=pajak.id,
                sales_id=None if not sales else sales.id
            )
            row = insert_data(row)
            print(f"-- added {row.nama}")
        except Exception as e:
            print(f"Error : {e}")
            print(pelanggan)


def add_supplier(suppliers):
    if not suppliers:
        print("No Data Found")

    for supp in suppliers:
        try:
            data = MasterSupplier(**supp)

            pajak = InfoPajak(npwp=data.npwp)
            pajak = insert_data(pajak)

            row = Supplier(
                kode=data.kode.lower(),
                nama=data.nama.title(),
                alamat=data.alamat.title(),
                kota=data.kota.title(),
                telepon=data.telepon,
                keterangan=data.keterangan.title(),
                info_pajak_id=pajak.id
            )
            row = insert_data(row)
            print(f"-- added {row.nama}")
        except Exception as e:
            print(f"Error : {e}")


def add_obat(obats):
    if not obats:
        print("No Data Found")

    for obat in obats:
        try:
            data = BaseObat(**obat)
            row = Obat(
                nama=data.nama.title(),
                jenis=data.jenis.lower(),
            )
            row = insert_data(row)
            print(f"-- added {row.nama}")
        except Exception as e:
            print(f"Error : {e}")


if __name__ == "__main__":
    cli_app()
