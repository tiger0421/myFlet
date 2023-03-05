import flet as ft


class GraphProcessing(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.expand = True
        self.columns_name = ""
        self.page = page


    def build(self):
        self.columns_name = [str(i) for i in range(100)]
        self.lv = ft.ListView(expand = 1, spacing = 10, padding = 20)
        self.lv.controls.append(ft.Checkbox(label = "a"))
        self.lv = self.make_cb(self.columns_name)
        column = ft.Row(
                controls = [
                        ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_clicked),
                        self.lv
#                        ft.Container(expand = 1, content = self.lv)
                        ],
                )
        return column

    def make_cb(self, columns_name):
        items = []
        if(len(columns_name)):
            items = [
                        ft.Checkbox(label = name, value = False) for name in columns_name
                    ]
        return ft.ListView(
                    expand = 1,
                    spacing = 10,
                    padding = 20,
                    controls = items,
                )

    def add_clicked(self, e):
        self.lv.controls.append(ft.Text(value = "A"))
        self.page.update()




def main(page: ft.Page):
    def items(count):
        items = []
        for i in range(1, count + 1):
            items.append(
                ft.Container(
                    content=ft.Text(value=str(i)),
                    alignment=ft.alignment.center,
                    width=50,
                    height=50,
                    bgcolor=ft.colors.AMBER,
                    border_radius=ft.border_radius.all(5),
                )
            )
        return items

    gp = GraphProcessing(page)
    t = ft.Text(value = "A")
    view = ft.Row(controls=[
                        gp,
#                        ft.Container(expand =1 , content=gp),
#                        ft.Container(expand =1, content=t),
                        ]
                  )

    page.add(gp)

ft.app(target=main, view=ft.WEB_BROWSER, port=8550)
