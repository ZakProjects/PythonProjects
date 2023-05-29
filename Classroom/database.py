import sqlite3


class StudentsDB:
    def start(self):
        con = sqlite3.connect("data.db")
        c = con.cursor()

        # CREATE STUDENTS TABLE
        c.execute("""CREATE TABLE if not exists students (
            id integer,
            name text,
            pic text,
            notes text
            )""")
        c.execute("""CREATE TABLE if not exists sem1 (
            id integer,
            ctrl_1 real,
            ctrl_2 real,
            ctrl_3 real,
            ctrl_4 real,
            ctrl_5 real,
            moyenne real
        )""")
        c.execute("""CREATE TABLE if not exists sem2 (
            id integer,
            ctrl_1 real,
            ctrl_2 real,
            ctrl_3 real,
            ctrl_4 real,
            ctrl_5 real,
            moyenne real
        )""")

        con.commit()
        con.close()
    
    def retrieve_data(self, id):
        # Initiate connection
        con = sqlite3.connect("data.db")
        c = con.cursor()

        # Select data
        c.execute(f"SELECT name, pic, notes FROM students WHERE id = {id}")
        general_info = c.fetchone()
        c.execute(f"SELECT ctrl_1, ctrl_2, ctrl_3, ctrl_4, ctrl_5, moyenne FROM sem1 WHERE id = {id}")
        sem_1 = [str(note) for note in c.fetchone()]
        c.execute(f"SELECT ctrl_1, ctrl_2, ctrl_3, ctrl_4, ctrl_5, moyenne FROM sem2 WHERE id = {id}")
        sem_2 = [str(note) for note in c.fetchone()]

        # Pack data into dict
        data = {"general_info": general_info, "sem_1": sem_1, "sem_2": sem_2}
        return data
    
    def get_means(self):
        # Initiate connection
        con = sqlite3.connect("data.db")
        c = con.cursor()
        # Select data
        c.execute(f"SELECT moyenne FROM sem1")
        sem1 = [moyenne[0] for moyenne in c.fetchall()]
        c.execute(f"SELECT moyenne FROM sem2")
        sem2 = [moyenne[0] for moyenne in c.fetchall()]
        # Create dict that holds means with their names
        c.execute(f"SELECT moyenne FROM sem1")
        result_1 = [item[0] for item in c.fetchall()]
        c.execute(f"SELECT moyenne FROM sem2")
        result_2 = [item[0] for item in c.fetchall()]
        # Get names according to their ids
        c.execute(f"SELECT name FROM students")
        names = [name[0] for name in c.fetchall()]
        result_final_1 = list(zip(names, result_1))
        result_final_2 = list(zip(names, result_2))
        by_names = {'sem1': result_final_1, 'sem2': result_final_2}
        data = {'sem1': sem1, 'sem2': sem2, 'by_names': by_names}
        return data
    
    def change_data(self, id, changes):
        # Initiate connection
        con = sqlite3.connect("data.db")
        c = con.cursor()

        # List different data
        notes = changes[0]
        sem_1 = tuple(changes[1])
        sem_2 = tuple(changes[2])

        # Save changes
        c.execute("UPDATE students SET notes = ? WHERE id = ?", (notes, id))
        c.execute("""UPDATE sem1 SET 
        ctrl_1 = ?,
        ctrl_2 = ?,
        ctrl_3 = ?,
        ctrl_4 = ?,
        ctrl_5 = ?,
        moyenne = ?
        WHERE id = ?
        """, sem_1 + (id, ))
        c.execute("""UPDATE sem2 SET 
        ctrl_1 = ?,
        ctrl_2 = ?,
        ctrl_3 = ?,
        ctrl_4 = ?,
        ctrl_5 = ?,
        moyenne = ?
        WHERE id = ?
        """, sem_2 + (id, ))

        con.commit()
        con.close()

        # Recompute the means
        self.compute_moyennes()

    def compute_moyennes(self):
        # Initiate connection
        con = sqlite3.connect("data.db")
        c = con.cursor()
        # Select data
        c.execute("SELECT ctrl_1, ctrl_2, ctrl_3, ctrl_4, ctrl_5, moyenne FROM sem1")
        notes_1 = [note for note in c.fetchall()]
        c1_1 = [tpl[0] for tpl in notes_1]
        if 0 in c1_1:
            pass
        else:
            m1_1 = round(sum(c1_1)/28, 2)
            c.execute(f"UPDATE moyennes SET moyenne = ? WHERE ctrl = ?", (m1_1,"ctrl1_sem1"))
        c2_1 = [tpl[1] for tpl in notes_1]
        if 0 in c2_1:
            pass
        else:
            m2_1 = round(sum(c2_1)/28, 2)
            c.execute(f"UPDATE moyennes SET moyenne = ? WHERE ctrl = ?", (m2_1,"ctrl2_sem1"))
        c3_1 = [tpl[2] for tpl in notes_1]
        if 0 in c3_1:
            pass
        else:
            m3_1 = round(sum(c3_1)/28, 2)
            c.execute(f"UPDATE moyennes SET moyenne = ? WHERE ctrl = ?", (m3_1,"ctrl3_sem1"))
        c4_1 = [tpl[3] for tpl in notes_1]
        if 0 in c4_1:
            pass
        else:
            m4_1 = round(sum(c4_1)/28, 2)
            c.execute(f"UPDATE moyennes SET moyenne = ? WHERE ctrl = ?", (m4_1,"ctrl4_sem1"))
        c5_1 = [tpl[4] for tpl in notes_1]
        if 0 in c5_1:
            pass
        else:
            m5_1 = round(sum(c5_1)/28, 2)
            c.execute(f"UPDATE moyennes SET moyenne = ? WHERE ctrl = ?", (m5_1,"ctrl5_sem1"))
        c6_1 = [tpl[5] for tpl in notes_1]
        if 0 in c6_1:
            pass
        else:
            m6_1 = round(sum(c6_1)/28, 2)
            c.execute(f"UPDATE moyennes SET moyenne = ? WHERE ctrl = ?", (m6_1,"ctrl6_sem1"))
        # 2EME SEMESTRE
        c.execute("SELECT ctrl_1, ctrl_2, ctrl_3, ctrl_4, ctrl_5, moyenne FROM sem2")
        notes_2 = [note for note in c.fetchall()]
        c1_2 = [tpl[0] for tpl in notes_2]
        if 0 in c1_2:
            pass
        else:
            m1_2 = round(sum(c1_2)/28, 2)
            c.execute(f"UPDATE moyennes SET moyenne = ? WHERE ctrl = ?", (m1_2,"ctrl1_sem2"))
        c2_2 = [tpl[1] for tpl in notes_2]
        if 0 in c2_2:
            pass
        else:
            m2_2 = round(sum(c2_2)/28, 2)
            c.execute(f"UPDATE moyennes SET moyenne = ? WHERE ctrl = ?", (m2_2,"ctrl2_sem2"))
        c3_2 = [tpl[2] for tpl in notes_2]
        if 0 in c3_2:
            pass
        else:
            m3_2 = round(sum(c3_2)/28, 2)
            c.execute(f"UPDATE moyennes SET moyenne = ? WHERE ctrl = ?", (m3_2,"ctrl3_sem2"))
        c4_2 = [tpl[3] for tpl in notes_2]
        if 0 in c4_2:
            pass
        else:
            m4_2 = round(sum(c4_2)/28, 2)
            c.execute(f"UPDATE moyennes SET moyenne = ? WHERE ctrl = ?", (m4_2,"ctrl4_sem2"))
        c5_2 = [tpl[4] for tpl in notes_2]
        if 0 in c5_2:
            pass
        else:
            m5_2 = round(sum(c5_2)/28, 2)
            c.execute(f"UPDATE moyennes SET moyenne = ? WHERE ctrl = ?", (m5_2,"ctrl5_sem2"))
        c6_2 = [tpl[5] for tpl in notes_2]
        if 0 in c6_2:
            pass
        else:
            m6_2 = round(sum(c6_2)/28, 2)
            c.execute(f"UPDATE moyennes SET moyenne = ? WHERE ctrl = ?", (m6_2,"ctrl6_sem2"))

        # Commit and close connection      
        con.commit()
        con.close()
    
    def get_marks(self, ctrl, sem):
        con = sqlite3.connect("data.db")
        c = con.cursor()

        c.execute(f"SELECT ctrl_{ctrl} FROM sem{sem}")
        data = [item[0] for item in c.fetchall()]
        con.close()

        return data

# StudentsDB().get_means()
