# I got this from https://www.youtube.com/watch?v=xV3gH1JZew4

from direct.showbase.ShowBase import ShowBase

class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        grassBlock = loader.loadModel('untitled.glb')
        grassBlock.reparentTo(render)

game = MyGame()
game.run()