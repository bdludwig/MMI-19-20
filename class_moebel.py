class moebel():
    def __init__(self):
        pass


class oberschrank(moebel):

     def statusWiedergeben(self):
         print('Ich bin voll.')

class unterschrank(moebel):

    def statusWiedergeben(self):
        print('Der Mülleimer ist so voll wie der Oberschrank')
