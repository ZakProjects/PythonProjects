from kivy.uix.screenmanager import Screen
from database import StudentsDB
import matplotlib.pyplot as plt
import numpy as np
from backend_kivyagg import FigureCanvasKivyAgg

class Statistics(Screen):
    def initiate(self):
        self.general_info()
        self.moyennes()
        self.classements()
    
    def general_info(self):
        db = StudentsDB()
        moyennes = db.get_means()
        # 1 er Semestre
        sem1 = [moyenne for moyenne in moyennes['sem1'] if moyenne != 0]
        if len(sem1) > 0:
            m_1 = round(sum(sem1)/len(sem1), 2)
            plus_m_1 = [moyenne for moyenne in sem1 if moyenne >= m_1]
            perplus_1 = round((len(plus_m_1)/len(sem1)) * 100, 2)
            minus_m_1 = [moyenne for moyenne in sem1 if moyenne < m_1]
            perminus_1 = round((len(minus_m_1)/len(sem1)) * 100, 2)
            print(perplus_1)
            self.ids.general_info.ids.sem1.text = f"[color=#3b3a39]o [u]Semestre I:[/color][/u] [color=#cf2929] {perminus_1}% [/color] - {m_1} - [color=#2a9e20] {perplus_1}%[/color]"
        else:
            self.ids.general_info.ids.sem1.text = "[color=#3b3a39]o [u]Semestre I:[/color][/u] [color=#cf2929] 00.00% [/color] - 00.00 - [color=#2a9e20] 00.00%[/color]"
        # 2 eme Semestre
        sem2 = [moyenne for moyenne in moyennes['sem2'] if moyenne != 0]
        if len(sem2) > 0:
            m_2 = round(sum(sem2)/len(sem2), 2)
            plus_m_2 = [moyenne for moyenne in sem2 if moyenne >= m_2]
            perplus_2 = round((len(plus_m_2)/len(sem2)) * 100, 2)
            minus_m_2 = [moyenne for moyenne in sem2 if moyenne < m_2]
            perminus_2 = round((len(minus_m_2)/len(sem2)) * 100, 2)
            self.ids.general_info.ids.sem2.text = f"[color=#3b3a39]o [u]Semestre I:[/color][/u] [color=#cf2929] {perminus_2}% [/color] - {m_2} - [color=#2a9e20] {perplus_2}%[/color]"
        else:
            self.ids.general_info.ids.sem2.text = "[color=#3b3a39]o [u]Semestre II:[/color][/u] [color=#cf2929] 00.00% [/color] - 00.00 - [color=#2a9e20] 00.00%[/color]"
        
    def moyennes(self):
        # Prepare the Interface
        if len(self.ids.moyennes.ids.plot.children) > 0:
            self.ids.moyennes.ids.plot.clear_widgets()
        db = StudentsDB()
        # Semestre I
        lm_11 = [item for item in db.get_marks(1, 1) if item != 0]
        lm_21 = [item for item in db.get_marks(2, 1) if item != 0]
        lm_31 = [item for item in db.get_marks(3, 1) if item != 0]
        lm_41 = [item for item in db.get_marks(4, 1) if item != 0]
        lm_51 = [item for item in db.get_marks(5, 1) if item != 0]
        lm_1 = [lm_11, lm_21, lm_31, lm_41, lm_51]
        m_1 = []
        for element in lm_1:
            if len(element) > 0:
                m_1.append(round(sum(element)/len(element), 2))
            else:
                m_1.append(0.15)
        # Semestre II
        lm_12 = [item for item in db.get_marks(1, 2) if item != 0]
        lm_22 = [item for item in db.get_marks(2, 2) if item != 0]
        lm_32 = [item for item in db.get_marks(3, 2) if item != 0]
        lm_42 = [item for item in db.get_marks(4, 2) if item != 0]
        lm_52 = [item for item in db.get_marks(5, 2) if item != 0]
        lm_2 = [lm_12, lm_22, lm_32, lm_42, lm_52]
        m_2 = []
        for element in lm_2:
            if len(element) > 0:
                m_2.append(round(sum(element)/len(element), 2))
            else:
                m_2.append(0.15)

        self.ids.moyennes.ids.plot.add_widget(self.bar_chart([1, 2, 3, 4, 5], 0.4, m_1, m_2))
    
    def bar_chart(self, x, w, m_1, m_2):
        fig = plt.figure()
        bar1 = np.arange(len(x))
        bar2 = [w+i for i in bar1]
        plt.bar(bar1, m_1, w, label="Semestre I", figure=fig)
        plt.bar(bar2, m_2, w, label="Semestre II", figure=fig)
        for i, v in enumerate(m_1):
            if v == 0.15:
                plt.text(i, v, str(0.0), ha='center', figure=fig)
            else:
                plt.text(i, v, str(v), ha='center', figure=fig)
        for i, v in enumerate(m_2):
            if v == 0.15:
                plt.text(i+w, v, str(0.0), ha='center', figure=fig)
            else:
                plt.text(i+w, v, str(v), ha='center', figure=fig)
        plt.ylabel("Moyennes", figure=fig)
        plt.xlabel("Contrôles", figure=fig)
        plt.xticks(bar1+w/2, x, figure=fig)
        plt.legend()
        fig.patch.set_facecolor('#cdd1e4')
        return FigureCanvasKivyAgg(fig)
    
    def classements(self):
        db = StudentsDB()
        data = db.get_means()['by_names']
        sorted_sem1 = sorted(data['sem1'], key=lambda x: x[1], reverse=True)
        sorted_sem2 = sorted(data['sem2'], key=lambda x: x[1], reverse=True)
        top_10_1 = sorted(sorted_sem1[:10], key=lambda x: x[1])
        top_10_1_notes = sorted([item[1] for item in top_10_1])
        top_10_2 = sorted(sorted_sem2[:10], key=lambda x: x[1])
        top_10_2_notes = sorted([item[1] for item in top_10_2])
        print(top_10_2_notes)
        bad_10_1 = sorted_sem1[18:]
        bad_10_1_notes = [item[1] for item in bad_10_1]
        bad_10_2 = sorted_sem2[18:]
        bad_10_2_notes = [item[1] for item in bad_10_2]
        # Graph Top 10 Sem I
        y = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        if len(self.ids.classement_1.children) > 1:
            self.ids.classement_1.ids.container.clear_widgets()
        self.ids.classement_1.ids.container.add_widget(self.graph_hbar(y, top_10_1_notes,
                (0.7, 0.2, 0.3), "Classement Des 10 Premiers Elèves: Semestre I", "Moyenne", "Elève", top_10_1))
        # Graph Top 10 Sem II
        if len(self.ids.classement_2.children) > 1:
            self.ids.classement_2.ids.container.clear_widgets()
        self.ids.classement_2.ids.container.add_widget(self.graph_hbar(y, top_10_2_notes,
                (0.7, 0.2, 0.3), "Classement Des 10 Premiers Elèves: Semestre II", "Moyenne", "Elève", top_10_2))
        # Graph Bad 10 Sem I
        if len(self.ids.classement_3.children) > 1:
            self.ids.classement_3.ids.container.clear_widgets()
        self.ids.classement_3.ids.container.add_widget(self.graph_hbar(y, bad_10_1_notes,
                (0.7, 0.2, 0.3), "Classement Des 10 Derniers Elèves: Semestre I", "Moyenne", "Elève", bad_10_1))
        # Graph Bad 10 Sem II
        if len(self.ids.classement_4.children) > 1:
            self.ids.classement_4.ids.container.clear_widgets()
        self.ids.classement_4.ids.container.add_widget(self.graph_hbar(y, bad_10_2_notes,
                (0.7, 0.2, 0.3), "Classement Des 10 Derniers Elèves: Semestre II", "Moyenne", "Elève", bad_10_2))
        
    
    def graph_hbar(self, y, w, color, title, xl, yl, names):
        fig = plt.figure()
        plt.xlabel(xl, figure=fig)
        plt.ylabel(yl, figure=fig)
        plt.title(title)
        plt.barh(y, w, color=color, figure=fig)
        for i, v in enumerate(names):
            plt.text(0.2, y[i], v[0], figure=fig)
            plt.text(w[i], y[i], str(w[i]), figure=fig)
        fig.patch.set_facecolor('#cdd1e4')
        return FigureCanvasKivyAgg(fig, size_hint=(1, 1))

