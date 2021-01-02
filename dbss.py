import sqlite3
from sqlite3.dbapi2 import connect
import datetime as dt


class Akun:
    numb = 1

    def __init__(self, nama, id, password) -> None:
        self.__nama = nama
        self.__id = id
        self.__pw = password
        self._tbname = "Akun"

    def get_all(self):
        temp = {"Nama": self.__nama, "ID": self.__id, "PW": self.__pw}
        return temp

    def create_table(self):
        conn = sqlite3.connect("SIAPV3.db")
        conn.execute(
            f"""CREATE TABLE IF NOT EXISTS {self._tbname} (
            ROWID INTEGER PRIMARY KEY NOT NULL,
            USER VARCHAR(50) NOT NULL,
            ID VARCHAR(50) UNIQUE NOT NULL,
            PASSWORD VARCHAR(50) NOT NULL
            )"""
        )
        conn.close()

    def insert(self):
        abs = self.checkNone(self.__id)
        conn = sqlite3.connect("SIAPV3.db")
        # print(abs)
        if abs == True:
            param = (self.__nama, self.__id, self.__pw)
            conn.execute(
                f"""INSERT INTO {self._tbname} (USER,ID,PASSWORD) VALUES (?,?,?)""",
                param,
            )
            conn.commit()
        else:
            print("ALREADY EXIST")
        conn.close()

    def update(self):
        self.read()
        upcol = input("KOLOM YANG DIUPDATE : ").upper()
        sets = input("VALUE UPDATE : ")
        rows = input("ROW UPDATE :")
        query = f"""UPDATE {self._tbname} SET {upcol} = ? WHERE ROWID = ?"""
        conn = sqlite3.connect("SIAPV3.db")
        conn.execute(query, (sets, rows))
        conn.commit()
        conn.close()

    def delete(self):
        conn = sqlite3.connect("SIAPV3.db")
        row = input("BARIS / DATA YANG INGIN DIHAPUS :")
        conn.execute(f"""DELETE FROM {self._tbname} WHERE ROWID = ?""", row)
        conn.commit()
        conn.close()

    def read(self):
        self.get_col()
        conn = sqlite3.connect("SIAPV3.db")
        curs = conn.cursor()
        curs.execute(f"SELECT * FROM {self._tbname}")
        datas = curs.fetchall()
        for item in datas:
            print(f"{item[0]:<15d}{item[1]:<15s}{item[2]:<15s}{item[3]:<15s}")
        conn.close()

    def checkNone(self, what, pw=None):
        conn = sqlite3.connect("SIAPV3.db")
        curs = conn.cursor()
        # whatrow = input("CHECK ROW")
        # valuerow = input("Value Row")
        curs.execute(f"SELECT * FROM {self._tbname} WHERE (ID = ?)", (what,))
        entry = curs.fetchall()

        if len(entry) == 0:
            # print(entry)
            return True
        else:
            # print(entry)
            if pw == None:
                return False
            else:
                curs.execute(
                    f"SELECT * FROM {self._tbname} WHERE (PASSWORD = ?)", (pw,)
                )
                ch = curs.fetchall()
                # print(ch)
                if ch[0][3] == pw:
                    return False
                else:
                    return True

    def get_col(self):
        conn = sqlite3.connect("SIAPV3.db")
        curs = conn.cursor()
        query = f"SELECT * FROM {self._tbname} where 1=0"
        curs.execute(query)
        for item in curs.description:
            print(f"{item[0]:15s}", end="")
        print()


class AkunPengelola(Akun):
    def __init__(self, nama, id, password) -> None:
        super().__init__(nama, id, password)
        self._tbname = "Pengelola"

    def insert(self):
        temp = self.get_all()
        # print(temp)
        auth = input("SECURE KEY :")
        if auth == "admin":
            abs = self.checkNone(temp["ID"])
            conn = sqlite3.connect("SIAPV3.db")
            # print(abs)
            if abs == True:
                param = (temp["Nama"], temp["ID"], temp["PW"])
                conn.execute(
                    f"""INSERT INTO {self._tbname} (USER,ID,PASSWORD) VALUES (?,?,?)""",
                    param,
                )
                conn.commit()
            conn.close()

    def update(self):
        temp = self.get_all()
        auth = input("SECURE KEY :")
        if auth == "admin":
            self.read()
            upcol = input("KOLOM YANG DIUPDATE : ").upper()
            sets = input("VALUE UPDATE : ")
            rows = input("ROW UPDATE :")
            query = f"""UPDATE {self._tbname} SET {upcol} = ? WHERE ROWID = ?"""
            conn = sqlite3.connect("SIAPV3.db")
            conn.execute(query, (sets, rows))
            conn.commit()
            conn.close()

    def delete(self):
        get_tbnames()
        tbname = input("select Table :").title()
        auth = input("SECURE KEY :")
        if auth == "admin":
            conn = sqlite3.connect("SIAPV3.db")
            row = input("BARIS / DATA AKUN YANG INGIN DIHAPUS :")
            ans = input(f"YAKIN INGIN MENGHAPUS {row} ?(Y/N)").upper()
            if ans == "Y":
                conn.execute(f"""DELETE FROM {tbname} WHERE ROWID = ?""", row)
            conn.commit()
            conn.close()

    def checkNone(self, what, pw=None):
        conn = sqlite3.connect("SIAPV3.db")
        curs = conn.cursor()
        # whatrow = input("CHECK ROW")
        # valuerow = input("Value Row")
        curs.execute(f"SELECT * FROM {self._tbname} WHERE (ID = ?)", (what,))
        entry = curs.fetchall()
        # print(entry)
        if len(entry) == 0:
            # print(entry)
            return True
        else:
            # print(entry)
            if pw == None:
                return False
            else:
                curs.execute(
                    f"SELECT * FROM {self._tbname} WHERE (PASSWORD = ?)", (pw,)
                )
                ch = curs.fetchall()
                # print(ch)
                if len(ch) != 0 and ch[0][3] == pw:
                    return False
                else:
                    return True


class Pegawai:
    def __init__(self, nama, nip, alamat, nomorHp, uid):
        self.__nip = nip
        self.__nama = nama
        self.__alamat = alamat
        self.__no_HP = nomorHp
        self.__uid = uid
        self._tbname = "Pegawai"

    def create_table(self):
        conn = sqlite3.connect("SIAPV3.db")
        conn.execute(
            f"""CREATE TABLE IF NOT EXISTS {self._tbname} (
            ROWID INTEGER PRIMARY KEY NOT NULL,
            NAMA VARCHAR(50) NOT NULL,
            NIP VARCHAR(50) UNIQUE NOT NULL,
            ALAMAT VARCHAR(50) NOT NULL,
            NOMOR_HP VARCHAR(50) NOT NULL
            UID VARCHAR (50) UNIQUE NOT NULL
            )"""
        )
        conn.close()

    def insert(self):
        abs = self.checkNone(self.__nip)
        conn = sqlite3.connect("SIAPV3.db")
        # print(abs)
        param = (self.__nama, self.__nip, self.__alamat, self.__no_HP, self.__uid)
        if abs == True:
            conn.execute(
                f"""INSERT INTO {self._tbname} (NAMA,NIP,ALAMAT,NOMOR_HP,UID) VALUES (?,?,?,?,?)""",
                param,
            )
        else:
            print("ALREADY EXISTS")
        conn.commit()
        conn.close()

    def update(self):
        self.read()
        upcol = input("KOLOM YANG DIUPDATE : ").upper()
        sets = input("VALUE UPDATE : ")
        rows = input("ROW UPDATE :")
        query = f"""UPDATE {self._tbname} SET {upcol} = ? WHERE ROWID = ?"""
        conn = sqlite3.connect("SIAPV3.db")
        conn.execute(query, (sets, rows))
        conn.commit()
        conn.close()

    def delete(self):
        self.read()
        conn = sqlite3.connect("SIAPV3.db")
        row = input("BARIS / DATA YANG INGIN DIHAPUS :")
        conn.execute(f"""DELETE FROM {self._tbname} WHERE ROWID = ?""", row)
        conn.commit()
        conn.close()

    def read(self):
        self.get_col()
        conn = sqlite3.connect("SIAPV3.db")
        curs = conn.cursor()
        curs.execute(f"SELECT * FROM {self._tbname}")
        datas = curs.fetchall()
        for item in datas:
            print(
                f"{item[0]:<15d}{item[1]:<15s}{item[2]:<15s}{item[3]:<15s}{item[4]:<15s}{item[5]:<15s}"
            )
        conn.close()

    def checkNone(self, what):
        conn = sqlite3.connect("SIAPV3.db")
        curs = conn.cursor()
        # whatrow = input("CHECK ROW")
        # valuerow = input("Value Row")
        curs.execute(f"SELECT * FROM {self._tbname} WHERE (NIP = ?)", (what,))
        entry = curs.fetchall()

        if len(entry) == 0:
            # print(entry)
            return True
        else:
            # print(entry)
            return False

    def get_col(self):
        conn = sqlite3.connect("SIAPV3.db")
        curs = conn.cursor()
        query = f"SELECT * FROM {self._tbname} where 1=0"
        curs.execute(query)
        for item in curs.description:
            print(f"{item[0]:15s}", end="")
        print()

    def get_info(uid):
        conn = sqlite3.connect("SIAPV3.db")
        curs = conn.cursor()
        # check=[nama]
        curs.execute("SELECT ROWID FROM Pegawai WHERE UID = ?", (uid,))
        data = curs.fetchall()
        if len(data) != 0:
            id_get = data[0][0]
            curs.execute(
                "SELECT NAMA,NIP,ALAMAT,NOMOR_HP FROM Pegawai WHERE ROWID = ?",
                (id_get,),
            )
            data = curs.fetchall()
            print(
                f"""
            Nama Pegawai : {data[0][0]}
            NIP          : {data[0][1]}
            Alamat       : {data[0][2]}
            Tanggal Lahir: {data[0][3]}
            """
            )
        else:
            print("DAFTARKAN DIRI ANDA SEBAGAI PEGAWAI")
        conn.close()


class Divisi:
    def __init__(self, idDivisi, nama):
        self._divId = idDivisi
        self.__namaDivisi = nama
        self._tbname = "Divisi"

    def create_table(self):
        conn = sqlite3.connect("SIAPV3.db")
        conn.execute(
            f"""CREATE TABLE IF NOT EXISTS {self._tbname} (
            ROWID INTEGER PRIMARY KEY NOT NULL,
            ID_DIVISI VARCHAR(50) UNIQUE NOT NULL,
            NAMA_DIVISI VARCHAR(50) NOT NULL
            )"""
        )
        conn.close()

    def insert(self):
        abs = self.checkNone(self._divId)
        conn = sqlite3.connect("SIAPV3.db")
        param = (self._divId, self.__namaDivisi)
        if abs == True:
            conn.execute(
                f"""INSERT INTO {self._tbname} (ID_DIVISI,NAMA_DIVISI) VALUES (?,?)""",
                param,
            )
            conn.commit()
        conn.close()

    def update(self):
        self.read()
        upcol = input("KOLOM YANG DIUPDATE : ").upper()
        sets = input("VALUE UPDATE : ")
        rows = input("ROW UPDATE :")
        query = f"""UPDATE {self._tbname} SET {upcol} = ? WHERE ROWID = ?"""
        conn = sqlite3.connect("SIAPV3.db")
        conn.execute(query, (sets, rows))
        conn.commit()
        conn.close()

    def delete(self):
        conn = sqlite3.connect("SIAPV3.db")
        row = input("BARIS / DATA YANG INGIN DIHAPUS :")
        conn.execute(f"""DELETE FROM {self._tbname} WHERE ROWID = ?""", row)
        conn.commit()
        conn.close()

    def read(self):
        self.get_col()
        conn = sqlite3.connect("SIAPV3.db")
        curs = conn.cursor()
        curs.execute(f"SELECT * FROM {self._tbname}")
        datas = curs.fetchall()
        for item in datas:
            print(f"{item[0]:<15d}{item[1]:<15s}{item[2]:<15s}")
        conn.close()

    def checkNone(self, what):
        conn = sqlite3.connect("SIAPV3.db")
        curs = conn.cursor()
        # whatrow = input("CHECK ROW")
        # valuerow = input("Value Row")
        curs.execute(f"SELECT * FROM {self._tbname} WHERE (ID_DIVISI = ?)", (what,))
        entry = curs.fetchall()
        if len(entry) == 0:
            # print(entry)
            return True
        else:
            # print(entry)
            return False

    def get_col(self):
        conn = sqlite3.connect("SIAPV3.db")
        curs = conn.cursor()
        query = f"SELECT * FROM {self._tbname} where 1=0"
        curs.execute(query)
        for item in curs.description:
            print(f"{item[0]:15s}", end="")
        print()


class JamKerja:
    def __init__(self, jamName, jamin, jamout) -> None:
        self._JamName = jamName
        self.__jamMasuk = jamin
        self.__jamPulang = jamout
        self._tbname = "JamKerja"

    def create_table(self):
        conn = sqlite3.connect("SIAPV3.db")
        conn.execute(
            f"""CREATE TABLE IF NOT EXISTS {self._tbname} (
            ROWID INTEGER PRIMARY KEY NOT NULL,
            JAM_NAME VARCHAR (50) UNIQUE NOT NULL,
            JAM_MASUK VARCHAR(50) NOT NULL,
            JAM_PULANG VARCHAR(50) NOT NULL
            )"""
        )
        conn.close()

    def insert(self):
        abs = self.checkNone(self._JamName)
        conn = sqlite3.connect("SIAPV3.db")
        param = (self._JamName, self.__jamMasuk, self.__jamPulang)
        # print(param)
        # print(abs)
        if abs == True:
            conn.execute(
                f"""INSERT INTO {self._tbname} (JAM_NAME,JAM_MASUK,JAM_PULANG) VALUES (?,?,?)""",
                param,
            )
        conn.commit()
        conn.close()

    def update(self):
        self.read()
        upcol = input("KOLOM YANG DIUPDATE : ").upper()
        sets = input("VALUE UPDATE : ")
        rows = input("ROW UPDATE :")
        query = f"""UPDATE {self._tbname} SET {upcol} = ? WHERE ROWID = ?"""
        conn = sqlite3.connect("SIAPV3.db")
        conn.execute(query, (sets, rows))
        conn.commit()
        conn.close()

    def delete(self):
        conn = sqlite3.connect("SIAPV3.db")
        row = input("BARIS / DATA YANG INGIN DIHAPUS :")
        conn.execute(f"""DELETE FROM {self._tbname} WHERE ROWID = ?""", row)
        conn.commit()
        conn.close()

    def read(self):
        self.get_col()
        conn = sqlite3.connect("SIAPV3.db")
        curs = conn.cursor()
        curs.execute(f"SELECT * FROM {self._tbname}")
        datas = curs.fetchall()
        for item in datas:
            print(f"{item[0]:<15d}{item[1]:<15s}{item[2]:<15s}{item[3]:<15s}")
        conn.close()

    def checkNone(self, what):
        conn = sqlite3.connect("SIAPV3.db")
        curs = conn.cursor()
        # whatrow = input("CHECK ROW")
        # valuerow = input("Value Row")
        curs.execute(f"SELECT * FROM {self._tbname} WHERE (JAM_NAME = ?)", (what,))
        entry = curs.fetchall()

        if len(entry) == 0:
            # print(entry)
            return True
        else:
            # print(entry)
            return False

    def get_col(self):
        conn = sqlite3.connect("SIAPV3.db")
        curs = conn.cursor()
        query = f"SELECT * FROM {self._tbname} where 1=0"
        curs.execute(query)
        for item in curs.description:
            print(f"{item[0]:15s}", end="")
        print()

    def match(self, jam, hari="Normal"):
        conn = sqlite3.connect("SIAPV3.db")
        curs = conn.cursor()
        query = f"SELECT JAM_MASUK FROM {self._tbname} WHERE JAM_NAME = ?"
        curs.execute(query, (hari,))
        data = curs.fetchall()
        # print(data)
        for item in data:
            # print(item[0])
            if jam > item[0]:
                return "Terlambat"
            elif jam < item[0]:
                return "Lebih awal"
            else:
                return "Tepat Waktu"
        conn.close()


def testing():
    pass
    # class Hari:
    #     def __init__(self, idhari, namahari):
    #         self._idHari = idhari
    #         self.__namaHari = namahari
    #         self._tbname = "Hari"

    #     def create_table(self):
    #         conn = sqlite3.connect("SIAPV3.db")
    #         conn.execute(
    #             f"""CREATE TABLE IF NOT EXISTS {self._tbname} (
    #             ROWID INTEGER PRIMARY KEY NOT NULL,
    #             IDHARI VARCHAR(50) UNIQUE NOT NULL,
    #             NAMAHARI VARCHAR(50) NOT NULL,
    #             KETERANGAN VARCHAR(50) NOT NULL
    #             )"""
    #         )
    #         conn.close()

    #     def insert(self):
    #         abs = self.checkNone(self._idHari)
    #         conn = sqlite3.connect("SIAPV3.db")
    #         # print(abs)
    #         param = (self._idHari, self.__namaHari)
    #         if abs == True:
    #             conn.execute(
    #                 f"""INSERT INTO {self._tbname} (IdHari,NamaHari) VALUES (?,?)""",
    #                 param,
    #             )
    #         else:
    #             print("ALREADY EXISTS")
    #         conn.commit()
    #         conn.close()

    #     def update(self):
    #         self.read()
    #         upcol = input("KOLOM YANG DIUPDATE : ").upper()
    #         sets = input("VALUE UPDATE : ")
    #         rows = input("ROW UPDATE :")
    #         query = f"""UPDATE {self._tbname} SET {upcol} = ? WHERE ROWID = ?"""
    #         conn = sqlite3.connect("SIAPV3.db")
    #         conn.execute(query, (sets, rows))
    #         conn.commit()
    #         conn.close()

    #     def delete(self):
    #         conn = sqlite3.connect("SIAPV3.db")
    #         row = input("BARIS / DATA YANG INGIN DIHAPUS :")
    #         conn.execute(f"""DELETE FROM {self._tbname} WHERE ROWID = ?""", row)
    #         conn.commit()
    #         conn.close()

    #     def read(self):
    #         self.get_col()
    #         conn = sqlite3.connect("SIAPV3.db")
    #         curs = conn.cursor()
    #         curs.execute(f"SELECT * FROM {self._tbname}")
    #         datas = curs.fetchall()
    #         for item in datas:
    #             print(f"{item[0]:<15d}{item[1]:<15s}{item[2]:<15s}{item[3]:<15s}")
    #         conn.close()

    #     def checkNone(self, what):
    #         conn = sqlite3.connect("SIAPV3.db")
    #         curs = conn.cursor()
    #         # whatrow = input("CHECK ROW")
    #         # valuerow = input("Value Row")
    #         curs.execute(f"SELECT * FROM {self._tbname} WHERE (IdHari = ?)", (what,))
    #         entry = curs.fetchall()

    #         if len(entry) == 0:
    #             # print(entry)
    #             return True
    #         else:
    #             # print(entry)
    #             return False

    #     def get_col(self):
    #         conn = sqlite3.connect("SIAPV3.db")
    #         curs = conn.cursor()
    #         query = f"SELECT * FROM {self._tbname} where 1=0"
    #         curs.execute(query)
    #         for item in curs.description:
    #             print(f"{item[0]:15s}", end="")
    #         print()


class Presensi:
    nmr = 0

    def __init__(self, user, tanggal, jam, status) -> None:
        self.__nomor = self.nmr + 1
        self.__user = user
        self.__tanggal = tanggal
        self.__jam = jam
        self.__status = status
        self._tbname = "Presensi"

    def create_table(self):
        conn = sqlite3.connect("SIAPV3.db")
        conn.execute(
            f"""CREATE TABLE IF NOT EXISTS {self._tbname} (
            ROWID INTEGER PRIMARY KEY NOT NULL,
            NOMOR  VARCHAR(50) UNIQUE NOT NULL,
            USER VARCHAR(50)  NOT NULL,
            TANGGAL VARCHAR(50)  NOT NULL,
            JAM VARCHAR(50) NOT NULL,
            STATUS VARCHAR(50) NOT NULL
            )"""
        )
        conn.close()

    def insert(self):
        abs = self.checkNone(self.__nomor)
        conn = sqlite3.connect("SIAPV3.db")
        while abs == False:
            self.__nomor += 1
            abs = self.checkNone(self.__nomor)
        # print(abs)
        param = (self.__nomor, self.__user, self.__tanggal, self.__jam, self.__status)
        if abs == True:
            conn.execute(
                f"""INSERT INTO {self._tbname} (NOMOR,USER,TANGGAL,JAM,STATUS) VALUES (?,?,?,?,?)""",
                param,
            )
        else:
            print("ALREADY EXISTS")
        conn.commit()
        conn.close()

    def update(self):
        self.read()
        upcol = input("KOLOM YANG DIUPDATE : ").upper()
        sets = input("VALUE UPDATE : ")
        rows = input("ROW UPDATE :")
        query = f"""UPDATE {self._tbname} SET {upcol} = ? WHERE ROWID = ?"""
        conn = sqlite3.connect("SIAPV3.db")
        conn.execute(query, (sets, rows))
        conn.commit()
        conn.close()

    def delete(self):
        self.read()
        conn = sqlite3.connect("SIAPV3.db")
        row = input("BARIS / DATA YANG INGIN DIHAPUS :")
        conn.execute(f"""DELETE FROM {self._tbname} WHERE ROWID = ?""", row)
        conn.commit()
        conn.close()

    def read(self):
        self.get_col()
        conn = sqlite3.connect("SIAPV3.db")
        curs = conn.cursor()
        curs.execute(f"SELECT * FROM {self._tbname}")
        datas = curs.fetchall()
        for item in datas:
            print(
                f"{item[0]:<15d}{item[1]:<15s}{item[2]:<15s}{item[3]:<15s}{item[4]:<15s}{item[5]:<15s}"
            )
        conn.close()

    def checkNone(self, what):
        conn = sqlite3.connect("SIAPV3.db")
        curs = conn.cursor()
        # whatrow = input("CHECK ROW")
        # valuerow = input("Value Row")
        curs.execute(f"SELECT * FROM {self._tbname} WHERE (NOMOR = ?)", (what,))
        entry = curs.fetchall()

        if len(entry) == 0:
            # print(entry)
            return True
        else:
            # print(entry)
            return False

    def get_col(self):
        conn = sqlite3.connect("SIAPV3.db")
        curs = conn.cursor()
        query = f"SELECT * FROM {self._tbname} where 1=0"
        curs.execute(query)
        for item in curs.description:
            print(f"{item[0]:15s}", end="")
        print()

    nmr += 1


def get_tbnames():
    con = sqlite3.connect("SIAPV3.db")
    curs = con.cursor()
    curs.execute('SELECT name from sqlite_master where type= "table"')
    # print(curs.fetchall())
    data = curs.fetchall()
    for i in data:
        for j in i:
            print(j, end=" | ")
    print()


def testing():
    pass
    # if __name__ == "__main__":
    # print("AKUN")
    # akun1 = Akun("User", "user01", "001")
    # akun1.create_table()
    # akun1.insert()
    # # akun1.update()
    # # akun1.delete()
    # akun1.read()
    # print("*" * 60)
    # print("AKUN PENGELOLA")
    # akun2 = AkunPengelola("Admin", "admin", "admin")
    # akun2.create_table()
    # # akun2.insert()
    # # akun2.update()
    # akun2.delete()
    # akun2.read()
    # print("*" * 60)
    # print("PEGAWAI")
    # peg = Pegawai("Budur", "7088", "Al-Hilal", "08xxx")
    # peg.create_table()
    # peg.insert()
    # # peg.update()
    # # peg.delete()
    # peg.read()
    # # peg.delete()
    # print("*" * 60)
    # print("DIVISI")
    # div = Divisi("DIV01", "NGANGGUR")
    # div.create_table()
    # div.insert()
    # # div.update()
    # # div.delete()
    # div.read()
    # print("*" * 60)
    # print("JAM KERJA")
    # jam = JamKerja(
    #     "Masuk",
    #     dt.datetime.strptime("08.00", "%H.%M").time().strftime("%H.%M"),
    #     dt.datetime.strptime("16.00", "%H.%M").time().strftime("%H.%M"),
    # )
    # jam.create_table()
    # jam.insert()
    # # jam.update()
    # # jam.delete()
    # jam.read()
    # print("*" * 60)
    # print("HARI")
    # hari = Hari("day1", "Senin")
    # hari.create_table()
    # hari.insert()
    # # hari.update()
    # # hari.delete()
    # hari.read()
    # print("*" * 60)
    # print("PRESENSI")
    # presen = Presensi(
    #     "S01", "user01", dt.datetime.strptime("07.30", "%H.%M").time().strftime("%H.%M")
    # )
    # presen.create_table()
    # presen.insert()
    # # presen.update()
    # # presen.delete()
    # presen.read()
    # get_tbnames()

    # dt.datetime.str
    # tgl = dt.datetime.now().strftime("%x")
    # jm = dt.datetime.now().strftime("%H.%M")
    # st = JamKerja(None,None,None).match(jm)
    # pre = Presensi('budi02',tgl,jm,st)
    # pre.create_table()
    # pre.insert()
    # stats = JamKerja(None,None,None).match()
    # print(stats)