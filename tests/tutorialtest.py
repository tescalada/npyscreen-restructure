from npyscreen.app import App
import npyscreen.form as form


class MyEmployeeForm(form.Form):
    def after_editing(self):
        self.parent_app.NEXT_ACTIVE_FORM = None

    def create(self):
        self.my_name = self.add(form.TitleText, name='Name')
        self.my_department = self.add(form.TitleSelectOne,
                                      scroll_exit=True,
                                      max_height=3,
                                      name='Department',
                                      values=['Department 1',
                                              'Department 2',
                                              'Department 3'])
        self.my_date = self.add(form.TitleDateCombo, name='Date Employed')


class MyApplication(App):
    def on_start(self):
        self.add_form('MAIN', MyEmployeeForm, name='New Employee')
        # A real application might define more forms here.......

if __name__ == '__main__':
    TestApp = MyApplication().run()

