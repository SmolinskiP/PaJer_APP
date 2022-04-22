from sql.db_data_functions import Get_SQL_Data, conn

def Prepare_SQL_akcje(rights):
    if rights == 777:
        table = Get_SQL_Data("_action", "action")
    else:
        if rights == 5:
            sql_query = "SELECT action FROM _action WHERE id IN (1, 2, 3, 4)"
        get_sql = conn.cursor()
        get_sql.execute(sql_query)
        prepare_table = get_sql.fetchall()
        table = []
        for item in prepare_table:
            table.append(item[0])
    return table

def Prepare_SQL_departments(rights):
    if rights == 777:
        table = Get_SQL_Data("_dzial", "dzial")
    else:
        if rights <= 13:
            sql_query = "SELECT dzial FROM _dzial WHERE id = " + str(rights)
        get_sql = conn.cursor()
        get_sql.execute(sql_query)
        prepare_table = get_sql.fetchall()
        table = []
        for item in prepare_table:
            table.append(item[0])
    return table

def Prepare_SQL_stanowiska(rights):
    if rights == 777:
        table = Get_SQL_Data("_stanowisko", "stanowisko")
    else:
        if rights == 5:
            sql_query = "SELECT stanowisko FROM _stanowisko WHERE id IN (23, 35, 36, 44, 54, 55, 60)"
        get_sql = conn.cursor()
        get_sql.execute(sql_query)
        prepare_table = get_sql.fetchall()
        table = []
        for item in prepare_table:
            table.append(item[0])
    return table

def Prepare_SQL_miasta(rights):
    if rights == 777:
        table = Get_SQL_Data("_lokalizacja", "miasto")
    else:
        if rights == 5:
            sql_query = "SELECT miasto FROM _lokalizacja WHERE id IN (1)"
        get_sql = conn.cursor()
        get_sql.execute(sql_query)
        prepare_table = get_sql.fetchall()
        table = []
        for item in prepare_table:
            table.append(item[0])
    return table

def Prepare_SQL_teamleaders(rights):
    if rights in (5, 777):
        table = Get_SQL_Data("_team", "teamleader")
    else:
        if rights == 5:
            sql_query = "SELECT teamleader FROM _team WHERE id IN (1)"
        get_sql = conn.cursor()
        get_sql.execute(sql_query)
        prepare_table = get_sql.fetchall()
        table = []
        for item in prepare_table:
            table.append(item[0])
    return table