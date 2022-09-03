import ursina as urs
import itertools


class Game(urs.Ursina):  # rename
    def __init__(self):
        super().__init__()
        urs.EditorCamera()
        urs.camera.world_position = (0, 0, -15)
        self.model = 'kek2.obj'
        self.load_game()

    def load_game(self):
        self.parent = urs.entity(model=self.model)
        urs.Entity(model=self.model)

    def input(self, key):
        super().input(key)







if __name__ == '__main__':
    app = Game()
    app.run()

