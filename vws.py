import dbss as db
import os
import datetime as dt
import abc


class Menus:
    @abc.abstractclassmethod
    def __call__(self):
        pass

    @abc.abstractclassmethod
    def choose(self):
        pass


def clear_screen():
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")


class Login:
    def __init__(self, nama, userid, pw) -> None:
        self.__nama = nama
        self.__userid = userid
        self.__pw = pw

        # def __call__(self) -> None:
        a = db.Akun(self.__nama, self.__userid, self.__pw)
        b = db.AkunPengelola(self.__nama, self.__userid, self.__pw)
        self.c = a.checkNone(self.__userid, self.__pw)
        self.d = b.checkNone(self.__userid, self.__pw)
        # print(self.c,self.d)

    def check(self):
        if self.d == False:
            return {"User": True, "Admin": True}
        elif self.c == False and self.d == True:
            return {"User": True, "Admin": False}
        else:
            return {"User": False, "Admin": False}


class MenuUser:
    def __init__(self, acc, uid):
        self._access = acc
        self._uid = uid

    def __call__(self):
        print(f"Your Access : {self._access}")
        a = f"""{(dt.datetime.now()).strftime("%c")}
    Menu :
        1.Pegawai
        2.Absensi
        3.Jam Kerja
        4.Divisi
        5.Log Out
        """
        print(a)
        self.menu = input("Select Menu >")
        self.menus()

    def menus(self):
        if self.menu == "1":
            clear_screen()
            temp = PegawaiMenu(self._access, self._uid)
            temp()
            # pass
        elif self.menu == "2":
            clear_screen()
            temp = AbsensiMenu(self._access, self._uid)
            temp()

            # pass
        elif self.menu == "3":
            clear_screen()
            temp = JamKerjaMenu(self._access, self._uid)
            temp()

            # pass
        elif self.menu == "4":
            clear_screen()
            temp = DivisiMenu(self._access, self._uid)
            temp()
            # pass
        elif self.menu == "5":
            clear_screen()
            return 1
        else:
            print("There no such menu")


class PegawaiMenu(Menus):
    def __init__(self, acc, uid) -> None:
        self._acc = acc
        self._uid = uid

    def __call__(self):
        a = f"""UID : {self._uid}
        {(dt.datetime.now()).strftime("%c")}
        1. Lihat Data Diri
        2. Daftarkan Pegawai
        3. Kembali
        """
        if self._acc == "Admin":
            a += """4. Cari Pegawai (Admin)
        5. Pecat Pegawai (Admin)
        6. Ubah Data Pegawai (Admin)
        7. Tampilkan Seluruh Pegawai"""

        print(a)
        select = input("Selecet One :")
        self.choose(select)

    def choose(self, select):
        if self._acc == "Admin":
            if select == "4":
                uidpeg = input("UID PEGAWAI : ")
                temp_new = db.Pegawai.get_info(uidpeg)
                self()
            elif select == "2":
                nama = input("NAMA PEGAWAI : ")
                nip = input("NIP PEGAWAI : ")
                alamat = input("Alamat PEGAWAI : ")
                noHp = input("Nomor HP PEGAWAI : ")
                uidpeg = input("UID PEGAWAI : ")
                temp_new = db.Pegawai(nama, nip, alamat, noHp, uidpeg)
                temp_new.insert()
                self()

            elif select == "5":
                # nama = input("NAMA PEGAWAI : ")
                # nip = input("NIP PEGAWAI : ")
                # alamat = input("Alamat PEGAWAI : ")
                # noHp = input("Nomor HP PEGAWAI : ")
                # uidpeg = input("UID PEGAWAI : ")
                temp_new = db.Pegawai(None, None, None, None, None)
                temp_new.delete()
                self()
            elif select == "6":
                # nama = input("NAMA PEGAWAI : ")
                # nip = input("NIP PEGAWAI : ")
                # alamat = input("Alamat PEGAWAI : ")
                # noHp = input("Nomor HP PEGAWAI : ")
                # uidpeg = input("UID PEGAWAI : ")
                temp_new = db.Pegawai(None, None, None, None, None)
                temp_new.update()
                self()
            elif select == "7":
                temp_new = db.Pegawai(None, None, None, None, None)
                temp_new.read()
                self()
        elif self._acc == "User":
            if select == "2":
                nama = input("NAMA PEGAWAI : ")
                nip = input("NIP PEGAWAI : ")
                alamat = input("Alamat PEGAWAI : ")
                noHp = input("Nomor HP PEGAWAI : ")
                uidpeg = self._uid
                temp_new = db.Pegawai(nama, nip, alamat, noHp, uidpeg)
                temp_new.insert()
                self()
        if select == "1":
            temp_new = db.Pegawai.get_info(self._uid)
            self()
        elif select == "3":
            feat()


class AbsensiMenu(Menus):
    def __init__(self, acc, uid) -> None:
        self._acc = acc
        self._uid = uid
        self._jam = ""

    def __call__(self):
        a = f"""UID : {self._uid}
        {(dt.datetime.now()).strftime("%c")}
        1. Absen
        2. Kembali"""
        if self._acc == "Admin":
            a += """
        3. Hapus Presensi (Admin)
        4. Ubah Data Presensi (Admin)
        5. Tampilkan Presensi"""

        print(a)
        select = input("Selecet One :")
        self.choose(select)

    def choose(self, select):
        if self._acc == "Admin":
            if select == "3":
                temp_new = db.Presensi(None, None, None, None)
                temp_new.delete()
                self()
            elif select == "4":
                temp_new = db.Presensi(None, None, None, None)
                temp_new.update()
                self()
            elif select == "5":
                temp_new = db.Presensi(None, None, None, None)
                temp_new.read()
                self()
        if select == "1":
            tanggal = dt.datetime.now().strftime("%x")
            jam = dt.datetime.now().strftime("%H.%M")
            st = db.JamKerja(None, None, None).match(jam)
            temp_new = db.Presensi(self._uid, tanggal, jam, st)
            temp_new.insert()
            self()
        elif select == "2":
            feat()


class JamKerjaMenu(Menus):
    def __init__(self, acc, uid) -> None:
        self._acc = acc
        self._uid = uid

    def __call__(self):
        a = f"""UID : {self._uid}
        {(dt.datetime.now()).strftime("%c")}
        1. Lihat Jam Kerja
        2. Kembali"""
        if self._acc == "Admin":
            a += """
        3. Hapus Jam 
        4. Ubah Data Presensi
        5. Tambah Jam"""

        print(a)
        select = input("Selecet One :")
        self.choose(select)

    def choose(self, select):
        if self._acc == "Admin":
            if select == "3":
                temp_new = db.JamKerja(None, None, None)
                temp_new.delete()
                self()
            elif select == "4":
                temp_new = db.JamKerja(None, None, None)
                temp_new.update()
                self()
            elif select == "5":
                jamname = input("NAMA JAM : ")
                jammasuk = input("JAM MASUK (Hours.Min) : ")
                jamout = input("JAM PULANG (Hours.Min) : ")
                temp_new = db.JamKerja(jamname, jammasuk, jamout)
                temp_new.insert()
                self()
        if select == "1":
            st = db.JamKerja(None, None, None)
            # temp_new = db.Presensi(self._uid,tanggal,jam,st)
            st.read()
            self()
        elif select == "2":
            feat()


class DivisiMenu(Menus):
    def __init__(self, acc, uid) -> None:
        self._acc = acc
        self._uid = uid

    def __call__(self):
        a = f"""UID : {self._uid}
        {(dt.datetime.now()).strftime("%c")}
        1. Lihat Divisi
        2. Kembali"""
        if self._acc == "Admin":
            a += """
        3. Hapus Divisi
        4. Ubah Data Divisi
        5. Tambah Divisi"""

        print(a)
        select = input("Selecet One :")
        self.choose(select)

    def choose(self, select):
        if self._acc == "Admin":
            if select == "3":
                temp_new = db.Divisi(None, None)
                temp_new.delete()
                self()
            elif select == "4":
                temp_new = db.Divisi(None, None)
                temp_new.update()
                self()
            elif select == "5":
                idDivisi = input("ID DIVISI : ")
                nama = input("NAMA DIVISI : ")
                temp_new = db.Divisi(idDivisi, nama)
                temp_new.insert()
                self()
        if select == "1":
            temp_new = db.Divisi(None, None)
            # temp_new = db.Presensi(self._uid,tanggal,jam,st)
            temp_new.read()
            self()
        elif select == "2":
            feat()


def menu():
    log = ""
    reg = ""
    print("=" * 10)
    print(
        """ WELCOME
    1. Log In
    2. Register
    3. Exit """
    )
    print("=" * 10)
    select = input("SELECT >> ")
    if select == "1":
        # pass
        nama = input("Nama :")
        userid = input("User ID :")
        pw = input("PW :")
        log = Login(nama, userid, pw).check()
        # print(log)
        if log["Admin"] == True:
            return ("Admin", userid)
        elif log["User"] == True and log["Admin"] == False:
            return ("User", userid)
        else:
            print("Login Failed")
            return menu()
    elif select == "2":
        nama = input("Nama :")
        userid = input("User ID :")
        pw = input("PW :")
        reg = db.Akun(nama, userid, pw)
        reg.insert()
        # print(reg.checkNone(userid))
        if reg.checkNone(userid) == False:
            print("Register Successfull")
        else:
            print("ALREADY EXIST")
        return menu()
    elif select == "3":
        clear_screen()
        print("THANK YOU")
        input("PRESS ANYTHING TO END")
        return 0
    else:
        print("No Such Menu. Try Again")


while True:
    acc = menu()
    # print(acc)
    if acc == None:
        pass
    elif type(acc) == int or acc[0] != "User" and acc[0] != "Admin":
        print("Program Ends")
        break
    else:
        feat = MenuUser(acc[0], acc[1])
        feat()
