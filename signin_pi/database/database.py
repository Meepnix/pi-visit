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

    def exec_sql(self, statement):

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

    def exec_sql_fetchone(self, statement):

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

    def check_tables(self, tables: str):

        for table in tables:
            print(table + " : " +
            str(self.check_table_exists(table)))

    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do. Return values are exit codes.


    def check_table_exists(self, tablename: str) -> bool:
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

    def create_tables(self):

        self.exec_sql("""
            CREATE TABLE qrcode (
            id int UNSIGNED NOT NULL AUTO_INCREMENT,
            status varchar(255),
            qrcode varchar(255),
            img_link varchar(255),
            create_date timestamp NOT NULL DEFAULT current_timestamp(),
            update_date timestamp ON UPDATE current_timestamp(),
            PRIMARY KEY (id)
            ) ENGINE = InnoDB;""")

        self.exec_sql("""
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
    
    
    def droptables(self):

        self.exec_sql("""
            DROP TABLE IF EXISTS qrlogs,qrcode;
        """)

    def create_qr_code(self, code):

        self.exec_sql(f"""
        INSERT INTO qrcode (qrcode) 
        VALUES ({code});
        """)

    def add_image_link(self, link, id):

        self.exec_sql(f"""
        UPDATE qrcode
        SET img_link = '{link}'
        WHERE id = {id};
        """)

    def update_qr_code_status(self, status, id):

        self.exec_sql(f"""
        UPDATE qrcode
        SET status = '{status}'
        WHERE id = {id};
        """)
        

    def create_qr_log(self, status, id):

        self.exec_sql(f"""
        INSERT INTO qrlogs (qrcode_id, status) 
        VALUES ({id}, '{status}');
        """)

    def log_qr(self, qrcode, img_link=None):

        result = self.exec_sql_fetchone(f"""
        SELECT id, status FROM qrcode 
        WHERE qrcode = '{qrcode}';
        """)

        if img_link:
            self.add_image_link(img_link, result[0])

        if not result[1] or result[1] == 'OUT':
            self.update_qr_code_status('IN', result[0])
            self.create_qr_log('IN', result[0])

        else:
            self.update_qr_code_status('OUT', result[0])
            self.create_qr_log('OUT', result[0])
        








        


        

            


    