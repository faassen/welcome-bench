import morepath


class App(morepath.App):
    pass


@App.path('/welcome')
class Welcome(object):
    pass


@App.view(model=Welcome)
def root_default(self, request):
    return "Hello World!"


App.commit()

main = App()
