from cmu_graphics import *
def onAppStart(app):
    app.lines = 0
    app.width = 400
    app.height = 400
    app.drawHor = True


def redrawAll(app):
    drawLabel(f'{app.lines} lines', 200, 50)
    drawCircle(50, 50, 5)
    drawCircle(350, 350, 5)
    for i in range(app.lines):
        if i == 0:
            drawLine(50 + i*30, 50 + i*30, 50 + i*30 + 30, 50 + i*30)
            continue
        if i%2 == 0:
            drawLine(50 + (i-1)*30, 50 + (i-1)*30, 50 + (i)*30, 50 + (i-1)*30)
        else:
            drawLine(50 + (i-1)*30, 50+ (i-1)*30, 50 + i*30, 50+(i-1)*30)
       

def onKeyPress(app, key):
    if key == '+' and app.lines < 20:
        app.lines += 1
    if key == '-' and app.lines > 0:
        app.lines -= 1

runApp()