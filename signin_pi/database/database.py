import mariadb
import os
import sys

class database:

    def __init__(self):

        # Connect to MariaDB Platform
        try:
            self.conn = mariadb.connect(
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD'],
            host=os.environ['DB_HOST'],
            port=int(os.environ['DB_PORT']),
            database=os.environ['DB_DATABASE']

            )   
        except mariadb.Error as e:

            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        self.dbcur = self.conn.cursor()

    def execSql(self, statement):

        conn = self.conn
        dbcur = conn.cursor()
        
        try: 
            dbcur.execute(statement)

        except mariadb.Error as e:

            print(f"Error executing sql on MariaDB Platform: {e}")
            sys.exit(1)

        finally:
            conn.commit()
            dbcur.close()

    def execSqlFetchone(self, statement):

        conn = self.conn
        dbcur = conn.cursor()

        try: 
            dbcur.execute(statement)
            return dbcur.fetchone()

        except mariadb.Error as e:

            print(f"Error executing sql on MariaDB Platform: {e}")
            sys.exit(1)
        
        finally:

            dbcur.close()

    def checkTables(self, tables: str):

        for table in tables:
            print(table + " : " +
            str(self.checkTableExists(table)))

    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do. Return values are exit codes.


    def checkTableExists(self, tablename: str) -> bool:
        self.dbcur = self.conn.cursor()
        self.dbcur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
        if self.dbcur.fetchone()[0] == 1:
            self.dbcur.close()
            return True
        self.conn.commit()
        self.dbcur.close()
        return False

    def createTables(self):

        self.execSql("""
            CREATE TABLE qrcode (
            id int UNSIGNED NOT NULL AUTO_INCREMENT,
            status varchar(255),
            qrcode varchar(255),
            img_link varchar(255),
            create_date timestamp NOT NULL DEFAULT current_timestamp(),
            update_date timestamp ON UPDATE current_timestamp(),
            PRIMARY KEY (id)
            ) ENGINE = InnoDB;""")

        self.execSql("""
            CREATE TABLE qrlogs (
            id int UNSIGNED NOT NULL AUTO_INCREMENT,
            qrcode_id int UNSIGNED NOT NULL,
            status varchar(255),
            create_date timestamp NOT NULL DEFAULT current_timestamp(),
            PRIMARY KEY (id),
            CONSTRAINT `fk_qrcode_qrlogs`
                FOREIGN KEY (qrcode_id) REFERENCES qrcode(id)
                ON DELETE CASCADE
                ON UPDATE RESTRICT

            ) ENGINE = InnoDB;""")
    
    
    def dropTables(self):

        self.execSql("""
            DROP TABLE IF EXISTS qrlogs,qrcode;
        """)

    def createQrcode(self, code):

        self.execSql(f"""
        INSERT INTO qrcode (qrcode) 
        VALUES ({code});
        """)

    def addImageLink(self, link, id):

        self.execSql(f"""
        UPDATE qrcode
        SET img_link = '{link}'
        WHERE id = {id};
        """)

    def updateQrcodeStatus(self, status, id):

        self.execSql(f"""
        UPDATE qrcode
        SET status = '{status}'
        WHERE id = {id};
        """)
        

    def createQrlog(self, status, id):

        self.execSql(f"""
        INSERT INTO qrlogs (qrcode_id, status) 
        VALUES ({id}, '{status}');
        """)

    def logQr(self, qrcode, img_link=None):

        result = self.execSqlFetchone(f"""
        SELECT id, status FROM qrcode 
        WHERE qrcode = '{qrcode}';
        """)

        if img_link:
            self.addImageLink(img_link, result[0])

        if not result[1] or result[1] == 'OUT':
            self.updateQrcodeStatus('IN', result[0])
            self.createQrlog('IN', result[0])

        else:
            self.updateQrcodeStatus('OUT', result[0])
            self.createQrlog('OUT', result[0])
        








        


        

            


    