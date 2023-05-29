from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from database import StudentsDB

Builder.load_file("rangees.kv")
Builder.load_file("main.kv")
Builder.load_file("student.kv")
Builder.load_file("statistics.kv")


class Classroom(ScreenManager):
    pass


class ClassroomApp(App):
    def on_start(self):
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)
    
    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            screen = self.root.current
            if screen == "main":
                return False
            elif screen in [f"rangee {i}" for i in range(1, 4)] + ["profile_page", 'statistics']:
                self.root.current = "main"
                return True

    def build(self):
        # create/start DB
        self.db = StudentsDB()
        self.db.start()

        return Classroom()

    def select_column(self, id):
        self.root.current = f'rangee {id}'
    
    def profile_page(self, id):
        self.update_profile_page(id)
        self.root.ids.profile_page._id = id
        self.root.current = 'profile_page'
    
    def previous(self, id):
        if id > 1:
            self.profile_page(id - 1)
        else:
            self.profile_page(28)


    def update_profile_page(self, id):
        # Get data from db
        data = self.db.retrieve_data(id)
        # Select variables
        profile_page = self.root.ids.profile_page
        name = profile_page.ids._name_field
        profile_pic = profile_page.ids._profile_pic
        notes = profile_page.ids._notes
        # 1 er Semestre
        ctrl1_sem1 = profile_page.ids._ctrl1_sem1
        ctrl2_sem1 = profile_page.ids._ctrl2_sem1
        ctrl3_sem1 = profile_page.ids._ctrl3_sem1
        ctrl4_sem1 = profile_page.ids._ctrl4_sem1
        ctrl5_sem1 = profile_page.ids._ctrl5_sem1
        m1 = profile_page.ids._m1
        # 2 eme Semestre
        ctrl1_sem2 = profile_page.ids._ctrl1_sem2
        ctrl2_sem2 = profile_page.ids._ctrl2_sem2
        ctrl3_sem2 = profile_page.ids._ctrl3_sem2
        ctrl4_sem2 = profile_page.ids._ctrl4_sem2
        ctrl5_sem2 = profile_page.ids._ctrl5_sem2
        m2 = profile_page.ids._m2

        # Apply changes based on retrieved data
        name.text = data["general_info"][0]
        profile_pic.pic = data["general_info"][1]
        notes.text = data["general_info"][2]
        # 1 er Semestre
        ctrl1_sem1.text = data["sem_1"][0]
        ctrl1_sem1.foreground_color = (1-(round(float(ctrl1_sem1.text) , 2)*0.03),0.2+round(float(ctrl1_sem1.text) , 2)*0.03, 0)
        ctrl2_sem1.text = data["sem_1"][1]
        ctrl2_sem1.foreground_color = (1-(round(float(ctrl2_sem1.text) , 2)*0.03),0.2+round(float(ctrl2_sem1.text) , 2)*0.03, 0)
        ctrl3_sem1.text = data["sem_1"][2]
        ctrl3_sem1.foreground_color = (1-(round(float(ctrl3_sem1.text) , 2)*0.03),0.2+round(float(ctrl3_sem1.text) , 2)*0.03, 0)
        ctrl4_sem1.text = data["sem_1"][3]
        ctrl4_sem1.foreground_color = (1-(round(float(ctrl4_sem1.text) , 2)*0.03),0.2+round(float(ctrl4_sem1.text) , 2)*0.03, 0)
        ctrl5_sem1.text = data["sem_1"][4]
        ctrl5_sem1.foreground_color = (1-(round(float(ctrl5_sem1.text) , 2)*0.03),0.2+round(float(ctrl5_sem1.text) , 2)*0.03, 0)
        m1.text = f"Moyenne : {data['sem_1'][5]}"
        m1.color = (0.9-(round(float(data['sem_1'][5]) , 2)*0.03),0.2+round(float(data['sem_1'][5]) , 2)*0.03, 0)
        # 2 eme Semestre
        ctrl1_sem2.text = data["sem_2"][0]
        ctrl1_sem2.foreground_color = (1-(round(float(ctrl1_sem2.text) , 2)*0.03),0.2+round(float(ctrl1_sem2.text) , 2)*0.03, 0)
        ctrl2_sem2.text = data["sem_2"][1]
        ctrl2_sem2.foreground_color = (1-(round(float(ctrl2_sem2.text) , 2)*0.03),0.2+round(float(ctrl2_sem2.text) , 2)*0.03, 0)
        ctrl3_sem2.text = data["sem_2"][2]
        ctrl3_sem2.foreground_color = (1-(round(float(ctrl3_sem2.text) , 2)*0.03),0.2+round(float(ctrl3_sem2.text) , 2)*0.03, 0)
        ctrl4_sem2.text = data["sem_2"][3]
        ctrl4_sem2.foreground_color = (1-(round(float(ctrl4_sem2.text) , 2)*0.03),0.2+round(float(ctrl4_sem2.text) , 2)*0.03, 0)
        ctrl5_sem2.text = data["sem_2"][4]
        ctrl4_sem2.foreground_color = (1-(round(float(ctrl4_sem2.text) , 2)*0.03),0.2+round(float(ctrl4_sem2.text) , 2)*0.03, 0)
        m2.text = f"Moyenne : {data['sem_2'][5]}"
        m2.color = (0.9-(round(float(data['sem_2'][5]) , 2)*0.03),0.2+round(float(data['sem_2'][5]) , 2)*0.03, 0)
    
    def confirm_changes(self, id):
        # Get data from UI
        profile_page = self.root.ids.profile_page
        notes = profile_page.ids._notes.text
        # 1 er semestre
        ctrl1_sem1 = profile_page.ids._ctrl1_sem1.text
        ctrl2_sem1 = profile_page.ids._ctrl2_sem1.text
        ctrl3_sem1 = profile_page.ids._ctrl3_sem1.text
        ctrl4_sem1 = profile_page.ids._ctrl4_sem1.text
        ctrl5_sem1 = profile_page.ids._ctrl5_sem1.text
        notes_1 = [float(note) for note in [ctrl1_sem1, ctrl2_sem1, ctrl3_sem1, ctrl4_sem1, ctrl5_sem1]
                if float(note) != 0]
        if len(notes_1) > 1:
            m1 = str(round(sum(notes_1)/len(notes_1), 2))
        else:
            m1 = "00.00"
        
        # 2 eme semestre
        ctrl1_sem2 = profile_page.ids._ctrl1_sem2.text
        ctrl2_sem2 = profile_page.ids._ctrl2_sem2.text
        ctrl3_sem2 = profile_page.ids._ctrl3_sem2.text
        ctrl4_sem2 = profile_page.ids._ctrl4_sem2.text
        ctrl5_sem2 = profile_page.ids._ctrl5_sem2.text
        notes_2 = [float(note) for note in [ctrl1_sem2, ctrl2_sem2, ctrl3_sem2, ctrl4_sem2, ctrl5_sem2]
                if float(note) != 0]
        if len(notes_2) > 1:
            m2 = str(round(sum(notes_2)/len(notes_2), 2))
        else:
            m2 = "00.00"
        # Pack data in dicts
        sem_1 = [ctrl1_sem1, ctrl2_sem1, ctrl3_sem1, ctrl4_sem1, ctrl5_sem1, m1]
        sem_2 = [ctrl1_sem2, ctrl2_sem2, ctrl3_sem2, ctrl4_sem2, ctrl5_sem2, m2]

        changes = [notes, sem_1, sem_2]
        self.db.change_data(id, changes)
        self.update_profile_page(id)

    def stats(self):
        self.statistics = self.root.ids.statistics
        self.statistics.initiate()
        self.root.current = 'statistics'


if __name__ == "__main__":
    ClassroomApp().run()
