# -*- coding: utf-8 -*-
import pyodbc
import mysql.connector
from transliterate import translit, get_available_language_codes
import datetime
from datetime import datetime, timedelta
from ldap3 import Server, Connection, ALL, NTLM, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, AUTO_BIND_NO_TLS, SUBTREE
from ldap3.core.exceptions import LDAPCursorError
from sys import argv
import time

def DT():
    DT = datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')
    return DT

db_company = "6" #База
db_company_2 = "1703" #Вентилятор
db_company_3 = "1713"

USE_LOG = True

# скидывает в Файл log.txt
# Выводит всякую информацию на экран, самое важное скидывает в Файл log.txt
def log(*args):
    #datelog = "/var/www/portal/spr/" + datetime.strftime(datetime.now(), '%Y-%m-%d-%H') + ".txt"
    datelog = datetime.strftime(datetime.now(), '%Y-%m-%d-%H') + ".txt"
    if USE_LOG:
        l = open(datelog, 'a', encoding='utf-8')
        print(datetime.now(), *args, file=l)
        l.close()





def my_split(s, seps):
    res = [s]
    for sep in seps:
        s, res = res, []
        for seq in s:
            res += seq.split(sep)
    return res





#lC
def lC(Company,Description):
    if Company == "База":
       ID = 6
       db_name = "zup_base"
       Table_name = "_Reference299"
       row_BD_name = "_Fld25961"
    elif Company == "Вентилятор":
         ID = 8
         db_name = "zup_vent"
         Table_name = "_Reference299"
         row_BD_name = "_Fld25961"
    elif Company == "REM":
         ID = 14
         db_name = "zp-rem3.1"
         Table_name = "_Reference274"
         row_BD_name = "_Fld7078"
    elif Company == "Электродвигатель":
         ID = 7
         db_name = "zp-eldv-3.1"
         Table_name = "_Reference274"
         row_BD_name = "_Fld7077"
    elif Company == "Электромашина":
         ID = 12
         db_name = "zp-rem3.1"
         Table_name = "_Reference274"
         row_BD_name = "_Fld7078"
    elif Company == "Инвертор":
         ID = 10
         db_name = "zp-in3.1"
         Table_name = "_Reference277"
         row_BD_name = "_Fld23394"
    elif Company == "Инстарт":
         ID = 10
         db_name = "zp-in3.1"
         Table_name = "_Reference277"
         row_BD_name = "_Fld23394"
    else:
         print("Не могу заглянуть в 1С - ",Company)
    try:
        lC_cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=ssql;DATABASE=%s;UID=sa;PWD=1qaz!QAZ' % db_name)
        lC_cursor = lC_cnxn.cursor()
        lC_cursor.execute("select _Description,{row_BD_name} as Birthday from {table_name} where _Description like '{Description}%'".format(table_name=Table_name,row_BD_name=row_BD_name,Description=Description))
        lC_row = lC_cursor.fetchone()
        FullName = lC_row[0]
        BDATE = lC_row[1]
        BDDate = BDATE.split(" ")[0]
        Birthdate = BDDate.split("-")
        BDY = int(Birthdate[0]) - 2000
        BDM = int(Birthdate[1])
        BDD = int(Birthdate[2])
        BirthDay = str(BDY)+"-"+str(BDM)+"-"+str(BDD)
    except:
        FullName, BirthDay = "-","-"
    return FullName, BirthDay

#print(lC("База", 'Кобзарев Денис'))

#Portal
Portal_User_List = []
def portal():
    Portal_User_List.clear()
    portal = mysql.connector.connect(user='kobzarev', password='3270881', host='portal-pma.szemo.ru', database='szemo')
    portal_cursor = portal.cursor()
    portal_cursor.execute("SELECT NAME, EMAIL FROM `szemoprt_users` WHERE 1")
    portal_row = portal_cursor.fetchall()
    Portal_User_List.append(portal_row)
    portal.close()
    return portal_row


# Список городов филиалов
City_list = ["Москва", "Новосибирск", "Екатеринбург","Череповец", "Пермь", "Астана", "Воронеж","Малая Вишера"]#,"Ростов-на-Дону"]


#Vent_list = ["Вентилятор_Екатеринбург","Вентилятор_Воронеж","Вентилятор_Новосибирск","Вентилятор_Москва"]
#Eldv_list = ["Электродвигатель_Москва","Электродвигатель_Новосибирск","Электродвигатель_Екатеринбург","Электродвигатель_Череповец","Электродвигатель_Пермь","Электродвигатель_Астана"]
#Basa_list = ["База_М.Вишера"]
#Elmash_list = ["Электромашина_М.Вишера"]
#Inv_list = ["Инвертор_Новосибирск"]

#print(Inv_list[0])
#Астериск
def aster(Request, SipName, Company, i):

    Company_Name = Company.split('_')[0]

    print("[",i,"] Опрос Астериска",Company_Name)

    # АТСки Вентилятор
    #if Company == "Вентилятор_Екатеринбург" :
    #    aster_host = '192.168.21.2'
    #    print("[",i,"] подключился к ", Company)
    if Company == "Вентилятор_Воронеж":
        aster_host = '192.168.20.2'
        print("[",i,"] подключился к ", Company)
    elif Company == "Вентилятор_Новосибирск":
        aster_host = '192.168.30.2'
        print("[",i,"] подключился к ", Company)
    elif Company == "Вентилятор_Москва":
        aster_host = '192.168.22.2'
        print("[",i,"] подключился к ", Company)
    elif Company == "Вентилятор_Санкт-Петербург":
        aster_host = '10.0.40.3'
        print("[",i,"] подключился к ", Company)
    # АТСки База
    elif Company == "База_Малая Вишера":
        aster_host = '192.168.23.2'
        print("[",i,"] подключился к ", Company)
    elif Company == "База_Санкт-Петербург":
        aster_host = '10.0.40.3'
        print("[",i,"] подключился к ", Company)
    # АТСки Электромашина
    elif Company == "Электромашина_Малая Вишера":
        aster_host = '192.168.23.2'
        print("[", i, "] подключился к ", Company)
    elif Company == "Электромашина_Санкт-Петербург":
        aster_host = '10.0.40.6'
        print("[", i, "] подключился к ", Company)
    # АТСки REM
    elif Company == "REM_Санкт-Петербург":
        aster_host = '10.0.40.6'
        print("[", i, "] подключился к ", Company)
    # АТСки Инвертор
    elif Company == "Инвертор_Санкт-Петербург":
        aster_host = '10.0.40.5'
        print("[", i, "] подключился к ", Company)
    elif Company == "Инвертор_Новосибирск":
        aster_host = '192.168.55.2'
        print("[", i, "] подключился к ", Company)
    elif Company == "Инстарт_Санкт-Петербург":
        aster_host = '10.0.40.5'
        print("[", i, "] подключился к ", Company)
    # АТСки Электродвигатель
    elif Company == "Электродвигатель_Новосибирск":
        aster_host = '192.168.53.2'
        print("[", i, "] подключился к ", Company)
    #elif Company == "Электродвигатель_Ростов-на-Дону":
    #    aster_host = '192.168.57.2'
    #    print("[", i, "] подключился к ", Company)
    elif Company == "Электродвигатель_Екатеринбург":
        aster_host = '192.168.54.2'
        print("[", i, "] подключился к ", Company)
    elif Company == "Электродвигатель_Череповец":
        aster_host = '192.168.52.2'
        print("[", i, "] подключился к ", Company)
    elif Company == "Электродвигатель_Пермь":
        aster_host = '192.168.51.2'
        print("[", i, "] подключился к ", Company)
    elif Company == "Электродвигатель_Москва":
        aster_host = '192.168.50.2'
        print("[", i, "] подключился к ", Company)
    elif Company == "Электродвигатель_Астана":
        aster_host = '192.168.31.2'
        print("[", i, "] подключился к ", Company)
    elif Company == "Электродвигатель_Санкт-Петербург":
         aster_host = '10.0.40.4'
         print("[", i, "] подключился к ", Company)
    else:
         aster_host = '10.0.40.3'
         print("[", i, "] Сервер для ",Company," не определен ")

    # Подключаемся к соответствующей АТС
    print("aster_host: ",aster_host,"Request: ", Request)
    aster = mysql.connector.connect(user='kobzarev',
                                    password='3270881',
                                    host=aster_host,
                                    database='asterisk',
                                    charset='utf8')
    aster_cursor = aster.cursor()



    if Request == "Search_SipName":

    # Показываем Номер поиск по SIPNAME
       try:
            print("SipName db request:", SipName)
            aster_cursor.execute("select extension from users  WHERE convert(cast(convert(SIPNAME using latin1) as binary) using utf8) like '{SipName}%'".format(SipName=SipName))
            aster_row = aster_cursor.fetchone()[0]

       except:
           aster_row = ""
           print("[",i,"] АТС отвечает, что Позьзователь" ,SipName," НЕ Найден")
    if Request == "User_List":
    # Показываем
        aster_cursor.execute("select convert(cast(convert(SIPNAME using latin1) as binary) using utf8), extension from users  WHERE extension > 999")
        aster_row = aster_cursor.fetchall()


    return aster_row


#print(aster("Search_SipName","АбоеваТЮ","Вентилятор_Санкт-Петербург"))
#print(aster("Search_SipName","КобзаревДВ","База_Санкт-Петербург"))

#Сфинкс
Children_List = []
def sphinx(Request="", ID=0):
    Children_List.clear()
    sphinx = mysql.connector.connect(user='spnx', password='spnx', host='10.0.20.23', database='TC-DB-MAIN')
    sphinx.cmd_query("SET NAMES 'utf8';")
    sphinx.cmd_query("SET CHARACTER SET 'utf8';")
    sphinx.cmd_query("SET SESSION collation_connection = 'utf8_general_ci';")
    sphinx_cursor = sphinx.cursor()
    if Request == "Name_From_ID":
       sphinx_cursor.execute("SELECT NAME, ID, Parent_ID FROM PERSONAL WHERE ID = {ID} and STATUS like 'AVAILABLE'".format(ID=int(ID)))
       sphinx_row = sphinx_cursor.fetchone()
    elif Request == "Check_Status":
       sphinx_cursor.execute("SELECT STATUS FROM PERSONAL WHERE NAME like '{Request}%'".format(Request=ID))
       sphinx_row = sphinx_cursor.fetchone()
    elif Request == "Counter_of_People":
       sphinx_cursor.execute("SELECT count(ID) FROM PERSONAL WHERE TYPE LIKE 'EMP' and STATUS like 'AVAILABLE'")
       sphinx_row = sphinx_cursor.fetchone()
    elif Request == "Name_From_Parent_ID":
       sphinx_cursor.execute("SELECT NAME, ID, Parent_ID FROM PERSONAL WHERE TYPE LIKE 'DEP' and  Parent_ID = {Parent_ID}  and STATUS like 'AVAILABLE'".format(Parent_ID=int(ID)))
       sphinx_row = sphinx_cursor.fetchone()
    elif Request == "Position_From_ID":
       sphinx_cursor.execute("SELECT POS FROM PERSONAL WHERE ID = {ID} and STATUS like 'AVAILABLE'".format(ID=int(ID)))
       sphinx_row = sphinx_cursor.fetchone()
    elif Request == "Photo":
        sphinx_cursor.execute("SELECT p.ID FROM PERSONAL per LEFT OUTER JOIN PHOTO p ON per.ID = p.ID where per.ID = {ID}".format(ID=ID))
        sphinx_row = sphinx_cursor.fetchone()
    elif Request == "Children_List":
        sphinx_cursor.execute("SELECT ID,Parent_ID, NAME FROM PERSONAL WHERE TYPE LIKE 'DEP' and Parent_ID = {Parent_ID} and STATUS like 'AVAILABLE'".format(Parent_ID=int(ID)))
        Children_List.append(sphinx_cursor.fetchall())
        sphinx_row = Children_List
    elif Request == "User_List":
        sphinx_cursor.execute("SELECT NAME, ID, Parent_ID FROM PERSONAL WHERE TYPE LIKE 'EMP' and STATUS like 'AVAILABLE' order by NAME ")
        sphinx_row = sphinx_cursor.fetchall()
    else:
        #Счетчик
        sphinx_cursor.execute("SELECT count(ID)  FROM PERSONAL WHERE Parent_ID = {Parent_ID} and STATUS like 'AVAILABLE'".format(Parent_ID=int(ID)))
        sphinx_row = sphinx_cursor.fetchone()

    sphinx.close()
    return sphinx_row

#print(sphinx("Children_List",0)[0][i][2])
#print(sphinx("Check_Sum",6))

#print(sphinx("Chack_Status","Кобзарев"))



def read_db(name):

    conn = mysql.connector.connect(user='kobzarev', password='3270881', host='portal-pma.szemo.ru', database='dbuser')
    cursor = conn.cursor()

    cursor.execute("SELECT sphynx_name,last_update FROM users WHERE sphynx_name like '{name}%'".format(name=name))
    cursor_row = cursor.fetchone()

    return cursor_row




def check_db(tel):
    conn = mysql.connector.connect(user='kobzarev', password='3270881', host='portal-pma.szemo.ru', database='dbuser')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE telnum_1 = {tel}".format(tel=int(tel)))
    cursor_row = cursor.fetchone()
    print("check_db(tel) id: ",cursor_row)
    return cursor_row


def check_time(time, pass_min=30):
    import datetime as dt
    time_left = dt.datetime.today() - time
    #print("time left:", time_left)
    if time_left > dt.timedelta(minutes=pass_min):
       time_refresh = 1
    else:
        time_refresh = 0
    return int(time_refresh)


def how_many_tasks_created(name):
    db_name = "sd"


    print(name)
    try:
        cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=ssql;DATABASE=%s;UID=sa;PWD=1qaz!QAZ' % db_name)
        sql_text = "SELECT count(u.Id) as counter FROM [User] u LEFT JOIN [Task] t ON t.CreatorId = u.id where u.name like '{name}%'".format(name=name)
        cursor = cnxn.cursor()
        cursor.execute(sql_text)
        cursor_row = cursor.fetchone()[0]
    except:
        cursor_row = 0
    print("Количество заявоко за все время: ",cursor_row)
    return cursor_row



def update_db_controls(value1):
    conn = mysql.connector.connect(user='kobzarev', password='3270881', host='portal-pma.szemo.ru', database='dbuser')
    cursor = conn.cursor()
    cursor.execute(
        """
          UPDATE controls
          SET
            value=:contr_val
          
        """, {
            'contr_val': value1

             })
    conn.commit()

def AD(name):
    server_name = '10.0.20.3'
    user_name = 'ad_reader'
    password = 'REAd_P@sw0rd'
    server = Server(server_name, get_info=ALL)
    conn = Connection(server, user='{}\\{}'.format('szemo', user_name), password=password, authentication=NTLM,auto_bind=True)
    try:
        conn.search('dc=szemo,dc=ru', '(&(objectclass=person)(name={}))'.format(str(name)), attributes=['mail'])
        result = conn.entries[0].entry_to_ldif()
        result = result.split(' ')[-6]
        mail = result.splitlines()[0]
    except:
        mail = "no_mail"
    return mail
    #print(format_string.format(str(e.name), str(e.logonCount), str(e.lastLogon)[:19], str(e.accountExpires)[:19], desc))

#print(AD('Кобзарев Денис Владимирович'))

def departament_tree():
    tree_general = []
    tree_top = []
    tree_top.clear()
    tree_general.clear()

    counter = int(len(sphinx("Children_List", 0)[0]))-1
    # print("counter:", counter, sphinx("Children_List", 0)[0][0][2])
    y = 0
    while y < counter:

        tree_general.append(sphinx("Children_List", 0)[0][y])
        y = y + 1
    #print(tree_general)

    counter_tree_top = int(len(tree_general))
    #print(counter_tree_top)

    for tree_genersl_single in tree_general:
        #if
        ID = tree_genersl_single[0]
        Name_top = sphinx("Children_List", ID)[0]
        #print("! ----------- ",len(Name_top))
        i = 0
        while i < len(Name_top)-1:

            #print(tree_genersl_single, "! ----------- ", Name_top[i][2])
            tree_all = [str(tree_genersl_single[2])+"_"+str(Name_top[i][2])]
            tree_top.append(tree_all)
            i = i + 1

    return tree_top



#print(departament_tree())

def write_db(str_sphynx_id, str_sphynx_parent_id, str_sphynx_filial_name, str_sphynx_name, str_sphynx_position,str_sphynx_photo, str_birthday, str_telnum_1, str_mail,str_Sort_Index, tasks_counter):
    # Чистка от NULL
    if str_sphynx_position is None:
        str_sphynx_position = "-"

    conn = mysql.connector.connect(user='kobzarev', password='3270881', host='portal-pma.szemo.ru', database='dbuser')
    cursor = conn.cursor()
    sql = "INSERT INTO users (sphynx_id, sphynx_parent_id, sphynx_filial_name,sphynx_name, sphynx_position,sphynx_photo, birthday, telnum_1, mail,Sort_Index,last_update,tasks_counter) " \
          "VALUES (%s, %s,%s, %s,%s, %s,%s, %s, %s,%s,%s,%s)"
    val = [
          (str_sphynx_id, str_sphynx_parent_id, str_sphynx_filial_name, str_sphynx_name, str_sphynx_position,str_sphynx_photo, str_birthday, str_telnum_1, str_mail,str_Sort_Index,DT(),tasks_counter),
          ]
    cursor.executemany(sql, val)
    print("Запись добавлена!")
    conn.commit()

#print(write_db(1,1,1,1,1,0,"1984-05-06",1,AD('Кобзарев Денис Владимирович')))

def sorting_index(name,position=""):
    Name = name.split(' ')
    if position == "":
        Index = 1000
    else:
        position = str(position)
        Position = position.split(' ')
        i = -1
        if Name[0] == "Русских" and Name[1] == "Вячеслав":
            Index = 1
        elif Name[i] == "Мацнев" or Name[i] == "Великанов":
            Index = 1
        else:
            while i < len(Position) - 1:
                if Position[i] == "Генеральный":
                    Index = 2
                elif Position[i] == "Офис-менеджер":
                    Index = 3
                elif Position[i] == "Заместитель":
                    Index = 4
                elif Position[i] == "Руководитель" or Position[i] == "Начальник":
                    Index = 5
                else:
                    Index = 100
                i = i + 1

    return Index

#print(sorting_index("Евзрезов Владимир Викторович","Руководитель направления"))

def do_you_have_a_space(string):
    if ' ' in string:
       status = True
    else:
       status = False
    return status
#print(do_you_have_a_space("asdasd"))

def main():
    # Получаем количество пользователей из сфинкса
    users = sphinx("User_List", "")
    print(users)
    len_user = len(users)
    print("Всего найдено ",len_user)
    for i in range(0,len_user):
        print('users[i][0] ',users[i][0])
        Sph_Name = str(users[i][0]).replace("!","").split(" ")
        print("Sph_Name:",Sph_Name)



        if len(Sph_Name) > 2 and Sph_Name[0] != "Гостевые пропуска" and Sph_Name[0] != "Уволенные" and Sph_Name[0] != "Уборщицы":
            print("Sph_Name[0] >"+str(Sph_Name[0].replace(" ",""))+"<")
            if Sph_Name[0].replace(" ","") == "":

                Sph_SipName = Sph_Name[1] + Sph_Name[2][0:1] + Sph_Name[3][0:1]
                how_many_tasks_created_counter = how_many_tasks_created(Sph_Name[1] +" "+ Sph_Name[2])
                print("tasks_created_counter ", Sph_Name[1] + " " + Sph_Name[2], how_many_tasks_created_counter)
            else:

                Sph_SipName = Sph_Name[0] + Sph_Name[1][0:1] + Sph_Name[2][0:1]
                how_many_tasks_created_counter = how_many_tasks_created(Sph_Name[0] + " " + Sph_Name[1])
                print("tasks_created_counter ", Sph_Name[0] + " " + Sph_Name[1],how_many_tasks_created_counter)
            print("Sph_SipName: ",Sph_SipName)
            Position = sphinx("Position_From_ID", int(sphinx("User_List")[i][1]))[0]
            print("Position: ",Position)
            User_Name = sphinx("User_List")[i][0]
            print("User_Name: ",User_Name)
            Mail = AD(User_Name)
            print("Mail: ",Mail)
            Company_Tree = sphinx("Name_From_ID", sphinx("User_List")[i][2])
            print("Company_Tree: ",Company_Tree)
            Sort_Index = sorting_index(User_Name, Position)
            print("Sort_Index: ",Sort_Index)

            if User_Name == "Кобзарев Денис Владимирович":
                print("                                                       -=-=-=-=-=-=-=-", User_Name,"-=-=-=-=-=-=-=-=")
            else:
                print("[", i, "][", Company_Tree, "-", User_Name, "]")

            # Узнаем название компании
            if int(Company_Tree[2]) > 0:
                Company_Tree_1 = sphinx("Name_From_ID", Company_Tree[2])
                if int(Company_Tree_1[2]) > 0:
                    Company_Tree_2 = sphinx("Name_From_ID", Company_Tree_1[2])
                    if int(Company_Tree_2[2]) > 0:
                        Company_Tree_3 = sphinx("Name_From_ID", Company_Tree_2[2])
                        print("-------[", i, "]-------[", Company_Tree_3, "]----------------3---------")
                    else:
                        Company_Name = Company_Tree_2[0]
                else:
                    Company_Name = Company_Tree_1[0]
            else:
                Company_Name = Company_Tree[0]

            print("real Company_Name: ",Company_Name)


            # Определяем Город
            # Если PerentID > 0
            if int(Company_Tree[2]) > 0:
                # Выевляем пренадлежность пользователя к филиалам по списку городов
                for City_Name in City_list:
                    print("[", i, "]>0   ", "[", i, "]", City_Name, Company_Tree)
                    # Если город найден в списке, то филиала
                    if City_Name == str(Company_Tree[0]):
                        print("[", i, "] YES", Company_Name, City_Name)
                        # Собираем полное наименование Города и компании
                        Company_Full_Name = Company_Name + "_" + City_Name
                        print("[", i, "] --Филиал---", Company_Full_Name, "------>", User_Name, Company_Name,City_Name)
                        break
                    # если нет то Питер
                    else:
                        print("[", i, "] NO")
                        City_Name = "Санкт-Петербург"
                        print("[", i, "] -----------  ЭТО НЕ ФИЛИАЛ", Company_Tree[0])
                        print("[", i, "] 0>>  -  Company_Name", Company_Name)
                        Company_Full_Name = Company_Name + "_" + City_Name
                        print("[", i, "] ----Питер-->>-->", User_Name, Company_Name, Company_Full_Name)
            else:
                # Присваиваем город и компанию без лишних дерганий
                City_Name = "Санкт-Петербург"
                Company_Name = sphinx("Name_From_ID", sphinx("User_List")[i][2])[0]
                print("[", i, "] 0  -  Company_Name", Company_Name)
                Company_Full_Name = Company_Name + "_" + City_Name
                print("[", i, "] ----Питер---->", User_Name, Company_Name, Company_Full_Name)
                # print("Company_Full_Name:",Company_Full_Name)

            try:
                print("Запрос в сфинкс:", Sph_SipName, "Company_Full_Name: ", Company_Full_Name,"i:", i)
                TelNum = aster("Search_SipName", Sph_SipName, Company_Full_Name, i)
            except:
                TelNum = 0
                print("[", i, "] Не могу вытянуть Номер Телефона")

            #### ОТКЛЮЧЕНО ПО ТРЕБОВАНИЮ ПОЛЬЗОВАТЕЛЕЙ
            #try:
            #    Birthday = lC(Company_Name, User_Name)[1]
            #except:
            print("[", i, "] Не могу вытянуть ДР", Company_Name)
            Birthday = "1111-11-11"

            ID_Photo = sphinx("Photo", sphinx("User_List")[i][1])[0]
            if ID_Photo:
                ID_Photo = sphinx("Photo", sphinx("User_List")[i][1])[0]
            else:
                ID_Photo = 0

            print("[", i, "] Потенциал! ", User_Name, Mail, 'Должность:', Position, "(", TelNum,")", "Компания:", Company_Full_Name, " ID Фотки:", ID_Photo)
            Company_Filial_Name = Company_Full_Name.split("_")
            # print(i,Company_Filial_Name[0],Company_Filial_Name[1])

            print("TelNumTelNumTelNum:", TelNum)

            if TelNum:
                print("[", i, "] Номер телефона:", TelNum)

                if read_db(User_Name):
                    # Запись найдена
                    # Проверяем прошло ли 30 минут
                    print("[", i, "] Запись существует")
                    if check_time(read_db(User_Name)[1]) > 0:
                        print("[", i, "] Запуск обновления. Проверка статуса:")
                        if sphinx("Check_Status", User_Name)[0] != "AVAILABLE":
                            print("[", i, "] Вырублен")
                        else:
                            print("[", i, "] Активен")
                    else:
                        print("[", i, "] Время еще не пришло")
                else:
                    #pass

                    print("Пробуем добавить новую запись...: ",Company_Tree[1], Company_Filial_Name[0], Company_Filial_Name[1], User_Name,Position, ID_Photo, Birthday, TelNum, Mail, Sort_Index,how_many_tasks_created_counter)
                    print("[", i, "] Пробуем добавить новую запись...: ", write_db(Company_Tree[1], Company_Filial_Name[0], Company_Filial_Name[1], User_Name,Position, ID_Photo, Birthday, TelNum, Mail, Sort_Index,how_many_tasks_created_counter))
            else:
                print("[", i,"]                                                              [Номер телефона отсутствует, идем дальше]")
                pass

        else:
            print("====>", Sph_Name,"[",print(len(Sph_Name)),"]")




def clear_db():
    conn = mysql.connector.connect(user='kobzarev', password='3270881', host='portal-pma.szemo.ru', database='dbuser')
    cursor = conn.cursor()
    sql = "DELETE FROM `users`"
    cursor.execute(sql)
    #print("Все Записи удалены!")
    conn.commit()



#print(read_db("Кобзаоев"))

clear_db()

print("Засыпаем на 10 секунд")
#time.sleep(10)
print("Начинаем создавать справочник")
main()

#print(lC("База", 'Кобзарев Денис'))

#AtS_P@ssw0rd


#print(sphinx("User_List"))
#i = 0
#while i < len(sphinx("User_List"))-1:

 #   if sphinx("User_List")[i][0] == "Кобзарев Денис Владимирович":
  #     print("Y",sphinx("User_List")[i][0])
   # else:
    #    pass
   # i = i + 1