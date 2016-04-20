#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, random
from PyQt4 import QtCore, QtGui

class InfoWindow(QtGui.QDialog):
    def __init__(self):
        super(InfoWindow, self).__init__()

        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)
        self.setWindowTitle('ZASADY GRY')
        # self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(lambda: self.clickExit())

        self.textBrowser = QtGui.QTextBrowser(self)
        tekst = '<b><span style="font-size: 24px">ReflexPy</span></b> jest grą, która polega na zestrzeliwywaniu pojawiających się zielonych okręgów.<br><img src="greenCircle.jpg" /> <br><u>Rozgrywka:</u><br>Użytkownik po wybraniu „Start” z opcji menu przechodzi do okna rozgrywki. Odbywa się ona na planszy podzielonej liniami pionowymi i poziomymi. Okręgi pojawiają się na przecięciach linii. Rozgrywka polega na zestrzeleniu okręgów poprzez kliknięcie na nie kursorem myszy. Po trafieniu naliczane są punkty, których suma wyświetlana jest w lewym dolnym rogu. W razie nietrafienia, bądź po upływie określonego czasu od pojawienia się celu, naliczane są punkty karne. Zdobycie 5 punktów karnych kończy rozgrywkę. <br><br>Projekt i realizacja:<br><i>Krzysztof Makulec 159304</i>'
        self.textBrowser.insertHtml(tekst.decode('UTF8'))

        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.addWidget(self.textBrowser)
        self.verticalLayout.addWidget(self.buttonBox)

    def clickExit(self):
        self.close()


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initMain()

    def initMain(self):

        self.setWindowTitle('ReflexPy')
        self.centrWidget = QtGui.QStackedWidget()
        self.setCentralWidget(self.centrWidget)
        menuWindow = MenuWindow()
        menuWindow.startBtn.clicked.connect(self.startGame)
        menuWindow.infoBtn.clicked.connect(self.showInfo)
        self.centrWidget.addWidget(menuWindow)
        self.statusbar = self.statusBar()
        self.statusbar.setStyleSheet("background-color: #4DBDE3; color: #fff")
        self.statusbar.showMessage("Menu")
        self.setFixedSize(280, 480)

    def startGame(self):

        letsStartGame = GameWindow(self)
        self.centrWidget.addWidget(letsStartGame)
        self.centrWidget.setCurrentWidget(letsStartGame)
        letsStartGame.msg2Statusbar[str].connect(self.statusbar.showMessage)
        self.statusbar.showMessage("0")

    def showInfo(self):
        showInfoWindow = InfoWindow()
        showInfoWindow.exec_()


class MenuWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MenuWindow, self).__init__(parent)
        layout = QtGui.QVBoxLayout()
        self.startBtn = QtGui.QPushButton('START')
        self.startBtn.setStyleSheet("background-color: #4DBDE3; font-size: 50px; color: #fff; border: solid 0px #fff; padding: 10px")
        self.infoBtn = QtGui.QPushButton('ZASADY GRY')
        self.infoBtn.setStyleSheet("background-color: #69E065; font-size: 30px; color: #fff; border: solid 0px #fff; padding: 10px")
        layout.addWidget(self.startBtn)
        layout.addWidget(self.infoBtn)
        self.setLayout(layout)
        self.setFixedSize(280, 480)


class GameWindow(QtGui.QWidget):
    GameWidth = 7
    GameHeight = 12
    Speed = 300
    MissLimit = 5
    TimeToNewCircle = 3
    TimeToStayCircle = 10

    msg2Statusbar = QtCore.pyqtSignal(str)

    def __init__(self,parent=None):
        super(GameWindow, self).__init__(parent)
        self.timer = QtCore.QBasicTimer()

        self.setFixedSize(280, 480)
        self.printGrid = [[0 for x in range(self.GameHeight)] for y in range(self.GameWidth)]
        self.printGridLeftTime = [[0 for x in range(self.GameHeight)] for y in range(self.GameWidth)]
        self.timer.start(GameWindow.Speed, self)
        self.countTime = 0
        self.gameScore = 0
        self.gameMiss = 0

    def shapeAt(self, x, y):
        return self.printGrid[x][y]

    def setShapeAt(self, x, y, shape):
        self.printGrid[x][y] = shape

    def squareWidth(self):
        return self.contentsRect().width() / GameWindow.GameWidth

    def squareHeight(self):
        return self.contentsRect().height() / GameWindow.GameHeight

    def paintEvent(self, QPaintEvent):
        painter = QtGui.QPainter(self)
        self.drawBackground(painter)

        for i in range(GameWindow.GameWidth):
            for j in range(GameWindow.GameHeight):
                shape = self.shapeAt(i, j)

                if shape != Tetrominoe.NoShape:
                    self.drawCircle(painter, i * self.squareWidth(), j * self.squareHeight(), shape)

    def drawBackground(self,painter):
        painter.setPen(QtGui.QColor(0xAD, 0xAD, 0xAD))
        for i in range(GameWindow.GameWidth):
            painter.drawLine(i*self.squareWidth()+self.squareWidth()/2, 0, i*self.squareWidth()+self.squareWidth()/2, 480)
        for j in range(GameWindow.GameHeight):
            painter.drawLine(0, j*self.squareHeight()+self.squareHeight()/2, 280, j*self.squareHeight()+self.squareHeight()/2)

    def drawCircle(self, painter, x, y, shape):
        painter.setPen(QtGui.QColor(0x00, 0x00, 0x00))
        painter.setBrush(QtGui.QColor(0x25, 0xEB, 0x1E))
        painter.drawEllipse(x, y, self.squareHeight(), self.squareWidth())


    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            if self.gameMiss < GameWindow.MissLimit:
                self.countTime += 1

                if self.countTime == GameWindow.TimeToNewCircle:
                    x = random.randint(0, GameWindow.GameWidth-1)
                    y = random.randint(0, GameWindow.GameHeight-1)
                    self.setShapeAt(x, y, Tetrominoe.Circle)
                    self.countTime = 0
                    self.update()

                for i in range(0, GameWindow.GameWidth):
                    for j in range(0, GameWindow.GameHeight):
                        if self.printGrid[i][j] == Tetrominoe.Circle:
                            if self.printGridLeftTime[i][j] >= GameWindow.TimeToStayCircle:
                                self.printGrid[i][j] = Tetrominoe.NoShape
                                self.printGridLeftTime[i][j] = 0
                                self.update()
                                self.gameMiss += 1
                            else:
                                self.printGridLeftTime[i][j] += 1
            else:
                self.stopGame()

        else:
            super(GameWindow, self).timerEvent(event)


    def mousePressEvent(self, QMouseEvent):
        posx = int(QMouseEvent.x()/self.squareWidth())
        posy = int(QMouseEvent.y()/self.squareHeight())

        if self.shapeAt(posx,posy) == Tetrominoe.Circle:
            self.printGrid[posx][posy] = Tetrominoe.NoShape
            self.printGridLeftTime[posx][posy] = 0
            self.gameScore += 100
            self.msg2Statusbar.emit(str(self.gameScore))
            self.update()
        else:
            self.gameMiss += 1
            if self.gameMiss == GameWindow.MissLimit:
                self.stopGame()


    def stopGame(self):
        self.timer.stop()
        self.clearBoard()
        self.update()
        self.scoreMessage = 'Twój wynik to: %d' % (self.gameScore)
        reply = QtGui.QMessageBox.information(None,"Wynik", self.scoreMessage.decode('UTF8'),
            QtGui.QMessageBox.Ok)
        if reply == QtGui.QMessageBox.Ok:
            self.deleteLater()
            self.msg2Statusbar.emit("Menu")
            pass


    def clearBoard(self):
        for i in range(0,GameWindow.GameHeight):
            for j in range(0, GameWindow.GameWidth):
                self.printGrid[j][i] = Tetrominoe.NoShape


class Tetrominoe(object):
    NoShape = 0
    Circle = 1


def main():

    app = QtGui.QApplication([])
    reflex = MainWindow()
    reflex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()