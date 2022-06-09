from PIL import Image, ImageFont, ImageDraw
from treti_pokus import board_size


class Obrazek:
    def __init__(self, boardsiz=board_size,  coef=1, invert=False):
        if not isinstance(boardsiz, int) or not isinstance(coef, int) \
                or boardsiz < 0 or coef < 0:
            raise TypeError("Obrazek.__init__: Board size and coef should both be positive integers.")
        self.boardsiz = boardsiz
        self.coef = coef
        self.invert = invert
        self.img = Image.new("RGB", (30*coef*boardsiz, 30*coef*boardsiz), "white")
        self.pixels = self.img.load()
        self.draw = ImageDraw.Draw(self.img)
        self.font = ImageFont.truetype("arial.ttf", coef*20)
        self.drawlines()

    def drawlines(self):
        for i in range(30*self.coef, self.boardsiz*self.coef*30, self.coef*30):  # step 30 for it
            #                                                                   to be row by row, col by col
            for j in range(0, self.boardsiz*self.coef*30):  # every pixel of column
                for k in range(self.coef):  # to make the line wider if coef > 1
                    self.pixels[i + k, j] = (0, 0, 0)
                    self.pixels[j, i + k] = (0, 0, 0)
                    # print(f"{i+k}i+k {j+k}j+k ({k} = k) size {self.img.size}")

    def writetext(self, position, text, size=20):  # position means board position
        text = str(text)
        x, y = position
        if self.invert:
            x, y = y, x
            y = self.boardsiz - y - 1
        x *= self.coef*30
        x += 10
        y = self.boardsiz - y - 1
        y *= self.coef*30
        ImageDraw.Draw(self.img).text((x, y), text, (0, 0, 0), font=ImageFont.truetype("arial.ttf", self.coef*size))

    def addpoint(self, positon, color=(255, 0, 0)):
        x, y = positon
        if self.invert:
            x, y = y, x
            y = self.boardsiz - y - 1
        x, y = x*self.coef*30, y*self.coef*30
        midx, midy = x + self.coef*15, y + self.coef*15
        for i in range(x, x + self.coef*30):
            for j in range(y, y + self.coef*30):
                if (i-midx)**2 + (j-midy)**2 < (self.coef*5)**2:
                    self.pixels[i, j] = color

    def fill(self, position, color=(255, 0, 0)):
        x, y = position
        for i in range(x*30*self.coef + self.coef, x*30*self.coef + 30*self.coef):
            for j in range(y*30*self.coef + self.coef, y*30*self.coef + 30*self.coef):
                self.pixels[i, j] = color

    def save(self, path: str):
        self.img.save(path)

    def show(self):
        self.img.show()


if __name__ == "__main__":
    print(500*"x", "\nname is main")
    b = Obrazek(board_size, coef=1)
    b.fill((1, 1))
    b.show()
