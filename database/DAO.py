from database.DB_connect import DBConnect
from model.state import State


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """select distinct year(s.datetime) as year
                from sighting s 
                order by year(s.`datetime`) desc """

        cursor.execute(query)

        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getAllShapes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """select distinct s.shape 
                from sighting s
                order by s.shape """

        cursor.execute(query)

        for row in cursor:
            result.append(row["shape"])

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getAllNodes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """select *
                from state """

        cursor.execute(query)

        for row in cursor:
            result.append(State(**row))

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getNumSightings(year, shape, idMap):
        conn = DBConnect.get_connection()



        cursor = conn.cursor(dictionary=True)

        query = """select st.id, count(distinct si.id) as num
                from state st
                join sighting si on st.id = si.state 
                where si.shape = %s and year(si.`datetime`) = %s
                group by st.id """

        cursor.execute(query, (shape, year))

        for row in cursor:
            idMap[row["id"]].numSightings = row["num"]

        cursor.close()
        conn.close()

    @staticmethod
    def getAllEdges(idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """select distinct n.state1, n.state2 
                from neighbor n
                where n.state1 < n.state2 """

        cursor.execute(query)

        for row in cursor:
            result.append((
                idMap[row["state1"]],
                idMap[row["state2"]]
            ))

        cursor.close()
        conn.close()
        return result
