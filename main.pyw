#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter
from random import randint
from sys import exit
from tkinter.scrolledtext import ScrolledText

import pygame
from pygame.locals import *


def instruction():
    """ 弹出使用说明窗口 """
    wInstruction = tkinter.Tk()  # 创建根窗口对象，
    wInstruction.iconbitmap(default='icon.ico')
    wInstruction.title('使用说明')
    backgroundTxt = '''
        现在，你是X团爸爸，负责一个区域内的外卖订单的接收和餐食快递。你需要通过招募外卖骑手来帮你送餐，赚取快递费。你的任务就是尽可能赚更多的钱。\n
运营规则：
        1. 你的区域一共有81个单位，有的单位是餐馆，大部分单位是食客家。
        2. 骑手每走过一个单位的距离花费30秒。
        3. 以左上角路口为原点，建立平面直角坐标系。行为x坐标，列为y坐标，路口坐标为整数。例如，右下角路口坐标为(7,7),左下角路口坐标为(0,7)。
        4. 你负责的外卖派送区域内，发起的任何订单都必须接收；如果订单发起后，1分30秒内没有派单给现有骑手，则视为拒单，你将被吊销营业执照，运营终止。
        5. 在系统暂停时，鼠标先点击一个商家，再点击一食客处，即算完成从餐馆到食客的订单发起动作。
        6. 开始运营时，你有1000元作为运营资本。
        7. 你必须有骑手才能接单，招聘一位骑手需投资250元，数量不限。系统会适时为你招聘骑手，当然，你也可以随时招聘骑手。
        8. 每个订单从下单时间开始，要求在15分钟内完成服务，否则算超时。满15分钟若没有完成结单，客户会投诉导致立刻罚款50元; 满30分钟若没有完成结单，属于恶意废单，你的职业生涯就此终结。
        9. 完成一单，你能赚10元。
        10. 负债即破产！一旦破产，即刻停止运营，系统盘点每位骑手的接单数、完成数、超时数。\n
        '''
    ins = ScrolledText(wInstruction, font=('等线', 16))  # 定义打字的
    ins.insert(tkinter.INSERT, backgroundTxt)
    ins.config(state=tkinter.DISABLED)
    ins.pack(expand=1, fill='both')  # 组件要用pack方法拿出来
    tkinter.mainloop()  # 生成


def run(surface, colorDict):
    """ 游戏主体 """

    class man(pygame.sprite.Sprite):
        """ 单个骑手类 """

        def __init__(self, rightHeadedImage, initialPos):
            pygame.sprite.Sprite.__init__(self)
            self.rightHeadedImage = rightHeadedImage
            self.leftHeadedImage = pygame.transform.flip(
                self.rightHeadedImage, True,
                False)  # surface翻转，第一个要翻转的surface，第二个水平翻转，第三个垂直翻转
            self.upHeadedImage = pygame.transform.rotate(
                self.rightHeadedImage, 90)  # 逆时针旋转角度
            self.downHeadedImage = pygame.transform.flip(
                self.upHeadedImage, False, True)
            self.__initialPos__ = initialPos
            self.speed = 2
            self.direction = right
            self.pos = self.__initialPos__  # 怎么 通过精灵类等它动了以后来确定位置？
            self.rect = self.rightHeadedImage.get_rect()
            self.rect.topleft = (
                (houseLen + roadLen) * self.pos[0] + (houseLen + 2),
                (houseLen + roadLen) * self.pos[1] + (houseLen + 2))
            self.index = len(manList) + 1
            self.destinationList = [
            ]  # 目标点由近到远的排列,是一个列表有两个数据，第一个是坐标，第二个是对应的订单唯一序号
            self.doingList = []
            self.doNumber = 0
            self.finishNumber = 0
            self.overTimeNumber = 0
            self.manInfoTxt = infoFont.render(
                u'骑手%d  位于：(%.1f,%.1f)  接单数：%d  完成数：%d  超时数：%d' %
                (self.index, self.pos[0], self.pos[1], self.doNumber,
                 self.finishNumber, self.overTimeNumber), True, (0, 0, 0))
            self.infoRect = Rect(
                725 + 12,
                210 + (self.index - 1) * (self.manInfoTxt.get_height() + 5),
                550, self.manInfoTxt.get_height())

        def decideDirection(self):
            """ 如果到达home，即完成一单返回真 """
            arriveHome = False
            if self.destinationList[0][0][0] == 0:
                if self.pos[0] != 0:
                    if self.pos[0] % 1 != 0:
                        self.direction = left
                    else:
                        if self.destinationList[0][0][1] > self.pos[1] + 1:
                            self.direction = down
                        elif self.destinationList[0][0][1] < self.pos[1] + 1:
                            self.direction = up
                        else:
                            self.direction = left
                else:
                    if self.destinationList[0][0][1] >= self.pos[1] + 1:
                        self.direction = down
                    elif self.pos[1] == self.destinationList[0][0][1] - 0.5:
                        if self.arrive() is True:
                            self.decideDirection()
                        else:
                            arriveHome = True
                    else:
                        self.direction = up
            elif self.destinationList[0][0][0] == 8:
                if self.pos[0] != 7:
                    if self.pos[0] % 1 != 0:
                        self.direction = right
                    else:
                        if self.destinationList[0][0][1] > self.pos[1] + 1:
                            self.direction = down
                        elif self.destinationList[0][0][1] < self.pos[1] + 1:
                            self.direction = up
                        else:
                            self.direction = right
                else:
                    if self.destinationList[0][0][1] >= self.pos[1] + 1:
                        self.direction = down
                    elif self.pos[1] == self.destinationList[0][0][1] - 0.5:
                        if self.arrive() is True:
                            self.decideDirection()
                        else:
                            arriveHome = True
                    else:
                        self.direction = up
            else:
                if self.pos[0] not in (self.destinationList[0][0][0],
                                       self.destinationList[0][0][0] - 1):
                    if self.pos[0] > self.destinationList[0][0][0]:
                        if self.pos[1] % 1 != 0 and self.pos[
                                1] > self.destinationList[0][0][1]:
                            self.direction = up
                        elif self.pos[1] % 1 != 0 and self.pos[
                                1] < self.destinationList[0][0][1]:
                            self.direction = down
                        elif self.pos[1] % 1 == 0:
                            self.direction = left
                    else:
                        if self.pos[1] % 1 != 0 and self.pos[
                                1] > self.destinationList[0][0][1]:
                            self.direction = up
                        elif self.pos[1] % 1 != 0 and self.pos[
                                1] < self.destinationList[0][0][1]:
                            self.direction = down
                        elif self.pos[1] % 1 == 0:
                            self.direction = right
                else:
                    if self.pos[1] >= self.destinationList[0][0][1]:
                        self.direction = up
                    elif self.pos[1] == self.destinationList[0][0][1] - 0.5:
                        if self.arrive() is True:
                            self.decideDirection()
                        else:
                            arriveHome = True
                    else:
                        self.direction = down
            if arriveHome is True:
                return True
            else:
                return False

        def update(self):
            if self.destinationList != []:
                if self.direction == right:
                    self.rect.left += self.speed
                elif self.direction == left:
                    self.rect.left -= self.speed
                elif self.direction == up:
                    self.rect.top -= self.speed
                elif self.direction == down:
                    self.rect.top += self.speed

        def infoUpdate(self):
            self.pos = [
                (self.rect.topleft[0] - (houseLen + 2)) / (houseLen + roadLen),
                (self.rect.topleft[1] - (houseLen + 2)) / (houseLen + roadLen)
            ]
            self.manInfoTxt = infoFont.render(
                u'骑手%d  位于：(%.1f,%.1f)  接单数：%d  完成数：%d  超时数：%d' %
                (self.index, self.pos[0], self.pos[1], self.doNumber,
                 self.finishNumber, self.overTimeNumber), True, (0, 0, 0))
            surface.fill(colorDict['CadetBlue3'], rect=self.infoRect)
            surface.blit(self.manInfoTxt, self.infoRect.topleft)

        def arrive(self):
            """ 骑手到达目标点时进行操作,如果到的是cafe返回真，反之返回假 """
            orderIndex = self.destinationList[0][1] - 1
            if houseRect[self.destinationList[0][0][0]][
                    self.destinationList[0][0]
                [1]][1] == cafe and orderList[orderIndex].cafeArrived is False:
                self.doingList.append(orderList[orderIndex])
                waitForList.remove(orderList[orderIndex])
                orderList[orderIndex].cafeArrived = True
                orderList[orderIndex].approachBy = self.index
                self.doNumber += 1
                if ontheWayAnalysis(self, orderList[orderIndex].consumer,
                                    orderIndex + 1):
                    pass
                else:
                    if [orderList[orderIndex].consumer,
                            orderIndex + 1] not in self.destinationList:
                        self.destinationList.append(
                            [orderList[orderIndex].consumer, orderIndex + 1])
                for theMan in manList:
                    while [orderList[orderIndex].cafe,
                           orderIndex + 1] in theMan.destinationList:
                        theMan.destinationList.remove(
                            [orderList[orderIndex].cafe, orderIndex + 1])
                return True
            elif houseRect[self.destinationList[0][0][0]][
                    self.destinationList[0][0]
                [1]][1] == home and orderList[orderIndex].cafeArrived is True:
                self.finishNumber += 1
                orderList[orderIndex].done = True
                orderList[orderIndex].doneBy = self.index
                if orderList[orderIndex] in self.doingList:
                    self.doingList.remove(orderList[orderIndex])
                self.destinationList.remove(
                    [orderList[orderIndex].consumer, orderIndex + 1])
                return False

    class order:
        def __init__(self, cafePos, consumerPos, orderTime, orderNumber):
            self.cafe = cafePos
            self.consumer = consumerPos
            self.time = orderTime
            self.index = orderNumber
            self.delay = False
            self.cafeArrived = False
            self.done = False
            self.approachBy = 0
            self.doneBy = 0
            self.waitFor = 0

    def lackOfMoney():
        """ 弹出没钱不能招聘窗口 """
        win = tkinter.Tk()  # 创建根窗口对象，
        win.iconbitmap(default='icon.ico')
        win.title('提示')
        label = tkinter.Label(
            win, text='招聘一个骑手需要250元，但你现在资金不足！', font=('楷体', 16))
        label.pack()
        win.mainloop()

    def gameover(cause):
        surface.fill((122, 197, 205), Rect(722 + 12, 0, 558, 150))
        exiTxt = employFont.render(u'退出系统', True, (0, 0, 0))
        exitRect = Rect(1060 + 12, 30, 184, 60)
        surface.fill(colorDict['lightGoldenRod2'], rect=exitRect)
        surface.blit(exiTxt,
                     (exitRect.topleft[0] + 20, exitRect.topleft[1] + 10))
        if cause == 'overTime':
            overTimeTxt = [
                pygame.font.Font('Deng.ttf', 20).render(
                    u'您有订单30分钟未送达，', True, (0, 0, 0)),
                pygame.font.Font('Deng.ttf', 20).render(
                    u'运营资格被取消！', True, (0, 0, 0))
            ]
            for i in range(len(overTimeTxt)):
                surface.blit(overTimeTxt[i], (730 + 12, 17 + i * 40))
        elif cause == 'minusMoney':
            minusMoneyTxt = pygame.font.Font('Deng.ttf', 50).render(
                u'您已破产！', True, (0, 0, 0))
            surface.blit(minusMoneyTxt, (760 + 12, 35))
        return 'gameOver'

    def ontheWayAnalysis(theMan, position, orderIndex):
        """ 对单个骑手和某一点的顺路分析,如果在路上就插点到目标点队列,并返回真否则假 """

        def posInComparation(nowPos, des, position):
            """ in返回1,同向但距离长返回0，不同向返回-1 """
            vectorNow_Des, vectorNow_Pos = (des[0] - nowPos[0],
                                            des[1] - nowPos[1]), (
                                                position[0] - nowPos[0],
                                                position[1] - nowPos[1]
                                            )  # 通过向量判断是否顺路
            if vectorNow_Des[0] * vectorNow_Pos[0] > 0 and vectorNow_Des[
                    1] * vectorNow_Pos[1] > 0:  # 方向在所围区域里面
                if abs(vectorNow_Des[0]) >= abs(vectorNow_Pos[0]) and abs(
                        vectorNow_Des[1]) >= abs(vectorNow_Pos[1]):  # 在里面
                    return 1
                else:
                    return 0
            elif vectorNow_Pos[1] == 0:  # 到可能position是横的
                if abs(vectorNow_Des[0]) > abs(vectorNow_Pos[0]):
                    return 1
                else:
                    return 0
            elif vectorNow_Pos[0] == 0:
                if vectorNow_Des[0] == 0:
                    if abs(vectorNow_Des[1]) >= abs(vectorNow_Pos[1]):
                        return 1
                    else:
                        return 0
                else:
                    if abs(vectorNow_Des[1]) > abs(vectorNow_Pos[1]):
                        return 1
                    else:
                        return 0
            else:
                return -1

        def roadxy2housexy(theMan, destination):
            """ 把骑手所在的道路位置坐标转化成对应的单位坐标 """
            if destination[0][1] > theMan.pos[
                    1]:  # 骑手在的横路能对应上下两个单位，当已有目标点在对应上单位以下时，骑手对应单位选取上单位
                return (theMan.pos[0] // 1 + 1, theMan.pos[1])
            else:
                return (theMan.pos[0] // 1 + 1, theMan.pos[1] + 1)

        # 把骑手到第一个目标的拿出来。。。
        if theMan.pos[0] > theMan.pos[0] // 1:  # 骑手在横路上 （通过地板除实现实数的向下取整）
            manPos = roadxy2housexy(theMan, theMan.destinationList[0])
            if posInComparation(manPos, theMan.destinationList[0][0],
                                position) == 1:
                if [position, orderIndex] not in theMan.destinationList:
                    theMan.destinationList.insert(
                        theMan.destinationList.index(
                            theMan.destinationList[0]), [position, orderIndex])
                return True
        else:  # 骑手在纵路或路口，把xy对调后转化为上一情况进行比较
            theMan.pos.reverse()
            theMan.destinationList[0][0].reverse()
            position.reverse()
            manPos = roadxy2housexy(theMan, theMan.destinationList[0])
            if posInComparation(manPos, theMan.destinationList[0][0],
                                position) == 1:
                theMan.pos.reverse()
                theMan.destinationList[0][0].reverse()
                position.reverse()
                if [position, orderIndex] not in theMan.destinationList:
                    theMan.destinationList.insert(
                        theMan.destinationList.index(
                            theMan.destinationList[0]), [position, orderIndex])
                return True
            else:
                theMan.pos.reverse()
                theMan.destinationList[0][0].reverse()
                position.reverse()
        for destination in theMan.destinationList:
            if theMan.destinationList.index(destination) == len(
                    theMan.destinationList) - 1:  # 最后一个没了 过
                break
            else:
                nextDes = theMan.destinationList[
                    theMan.destinationList.index(destination) + 1]
                if theMan.destinationList.index(destination) == len(
                        theMan.destinationList) - 2:  # 倒数第二个，即最后一个，考虑外延的情况
                    if posInComparation(destination[0], nextDes[0],
                                        position) == 1:
                        if [position,
                                orderIndex] not in theMan.destinationList:
                            theMan.destinationList.insert(
                                theMan.destinationList.index(nextDes),
                                [position, orderIndex])
                    elif posInComparation(destination[0], nextDes[0],
                                          position) == 0:
                        if [position,
                                orderIndex] not in theMan.destinationList:
                            theMan.destinationList.append(
                                [position, orderIndex])
                elif posInComparation(destination[0], nextDes[0],
                                      position) == 1:  # 一般情况，只有在里面
                    if [position, orderIndex] not in theMan.destinationList:
                        theMan.destinationList.insert(
                            theMan.destinationList.index(nextDes),
                            [position, orderIndex])
        return False

    def arrivalRoadxy(buildingxy):
        """ 传入建筑物的坐标，返回他上下左右位置的道路坐标 """
        return [[buildingxy[0] - 0.5, buildingxy[1] - 1],
                [buildingxy[0] - 0.5, buildingxy[1]],
                [buildingxy[0] - 1, buildingxy[1] - 0.5],
                [buildingxy[0], buildingxy[1] - 0.5]]

    staticRect = Rect(734, 0, 1280 + 12 - 732, 732)
    lineRect = Rect(732, 0, 2, 732)
    nowTime = 0
    money = 1000
    orderNumber = 0
    home, cafe = 0, 1  # 定义了每个方格的状态，1为cafe，0为home
    houseLen, roadLen = 60, 24
    roadRect = [[
        Rect(houseLen + (houseLen + roadLen) * i, 0, roadLen, 732)
        for i in range(8)
    ],
                [
                    Rect(0, houseLen + (houseLen + roadLen) * i, 732, roadLen)
                    for i in range(8)
                ]]  # 第二级0为竖路1为横路的集合
    houseRect = [[[
        Rect(y * (houseLen + roadLen), x * (houseLen + roadLen), houseLen,
             houseLen), 0
    ] for x in range(9)] for y in range(9)]  # 单位矩阵二维数组，先x后y,坐标从0，0开始
    homeImg, cafeImg = pygame.image.load('home.bmp').convert_alpha(
    ), pygame.image.load('cafe.bmp').convert_alpha()
    runImg, pauseImg = pygame.image.load('run.png'), pygame.image.load(
        'pause.png')
    moneyFont, infoFont, employFont = pygame.font.Font(
        'Deng.ttf', 24), pygame.font.Font('Deng.ttf', 18), pygame.font.Font(
            'Deng.ttf', 36)
    controlRect = Rect(829 + 12, 20, 80, 80)
    employTxt = employFont.render(u'招聘骑手', True, (0, 0, 0))
    employRect = Rect(1009 + 12, 30, 184, 60)
    exiTxt = employFont.render(u'退出系统', True, (0, 0, 0))
    exitRect = Rect(1060 + 12, 30, 184, 60)
    surface.fill((colorDict['Snow']))
    surface.fill(colorDict['CadetBlue3'], rect=staticRect)
    surface.fill((0, 0, 0), rect=lineRect)
    surface.fill(colorDict['lightGoldenRod1'], rect=employRect)
    surface.blit(runImg, controlRect.topleft)
    surface.blit(employTxt,
                 (employRect.topleft[0] + 20, employRect.topleft[1] + 10))
    for x in range(9):
        for y in range(9):
            pygame.draw.rect(surface, colorDict['AntiqueWhite2'],
                             houseRect[x][y][0])
    for i in range(3):  # 合理随机挑选cafe
        for j in range(3):
            for k in range(randint(1, 2)):
                x, y = i * 3 + randint(0, 2), j * 3 + randint(
                    0, 2)  # 把81个坐标画成9个小区域，关系如左所示
                if houseRect[x][y][1] == cafe:
                    continue
                else:
                    houseRect[x][y][1] = cafe
    for x in range(9):  # 填上建筑图案
        for y in range(9):
            if houseRect[x][y][1] == home:
                surface.blit(homeImg, (houseRect[x][y][0].topleft[0] + 5,
                                       houseRect[x][y][0].topleft[1] +
                                       8))  # 把家放到横偏移5，纵偏移8，cafe偏移均为5
            else:
                surface.blit(cafeImg, (houseRect[x][y][0].topleft[0] + 5,
                                       houseRect[x][y][0].topleft[1] + 5))
    clock = pygame.time.Clock()
    manList = []
    left, right, up, down = 'left', 'right', 'up', 'down'
    orderList = []  # 发起的订单的集合
    waitForList = []
    running, pause = 1, 0  # 定义运行状态和暂停操作状态
    runCondition = pause
    selectCafe, selectHome = 1, 0  # 定义选择餐厅和选择食客状态
    selection = selectCafe
    while True:
        # 时间和金钱定义模块
        if runCondition == running:
            nowTime += clock.tick_busy_loop(42)
        moneyTxt = moneyFont.render(u'现有资金：{}元'.format(money), True, (0, 0, 0))
        moneyRect = Rect(730 + 12, 150, 240, moneyTxt.get_height())
        surface.fill(colorDict['CadetBlue3'], rect=moneyRect)
        surface.blit(moneyTxt,
                     (moneyRect.topleft[0] + 5, moneyRect.topleft[1]))
        realTime = nowTime * 3 / 100  # 3/12.5运行一秒走两分钟，3/25时运行一秒走一分钟，我不知道为什么
        timeTxt = moneyFont.render(
            u'运营时间：%d时%.2d分%.2d秒' % (realTime // 3600, (realTime % 3600) // 60,
                                     (realTime % 3600) % 60), True, (0, 0, 0))
        timeRect = Rect(1000 + 12, 150, 270, timeTxt.get_height())
        surface.fill(colorDict['CadetBlue3'], rect=timeRect)
        surface.blit(timeTxt, timeRect.topleft)
        # 动作响应部分
        for event in pygame.event.get():
            if event.type == QUIT:  # 定义退出动作
                pygame.quit()
                exit()
            if runCondition == running:
                if event.type == MOUSEBUTTONDOWN:
                    if controlRect.collidepoint(event.pos):
                        surface.fill(colorDict['CadetBlue3'], rect=controlRect)
                        surface.blit(runImg, controlRect.topleft)
                        runCondition = pause
            elif runCondition == 'gameOver':
                if exitRect.collidepoint(pygame.mouse.get_pos()):
                    surface.fill(colorDict['lightGoldenRod2'], rect=exitRect)
                    surface.blit(
                        exiTxt,
                        (exitRect.topleft[0] + 20, exitRect.topleft[1] + 10))
                elif exitRect.collidepoint(pygame.mouse.get_pos()) == 0:
                    surface.fill(colorDict['lightGoldenRod1'], rect=exitRect)
                    surface.blit(
                        exiTxt,
                        (exitRect.topleft[0] + 20, exitRect.topleft[1] + 10))
                if event.type == MOUSEBUTTONDOWN and exitRect.collidepoint(
                        event.pos):
                    surface.fill(colorDict['lightGoldenRod3'], rect=exitRect)
                    surface.blit(
                        exiTxt,
                        (exitRect.topleft[0] + 20, exitRect.topleft[1] + 10))
                    pygame.quit()
                    exit()
            elif runCondition == pause:
                if employRect.collidepoint(pygame.mouse.get_pos()):
                    surface.fill(colorDict['lightGoldenRod2'], rect=employRect)
                    surface.blit(employTxt, (employRect.topleft[0] + 20,
                                             employRect.topleft[1] + 10))
                elif employRect.collidepoint(pygame.mouse.get_pos()) == 0:
                    surface.fill(colorDict['lightGoldenRod1'], rect=employRect)
                    surface.blit(employTxt, (employRect.topleft[0] + 20,
                                             employRect.topleft[1] + 10))
                if event.type == MOUSEBUTTONDOWN:
                    if controlRect.collidepoint(event.pos):  # 点开始，动画开始
                        surface.fill(colorDict['CadetBlue3'], rect=controlRect)
                        surface.blit(pauseImg, controlRect.topleft)
                        runCondition = running
                    elif employRect.collidepoint(event.pos):  # 点招聘
                        surface.fill(
                            colorDict['lightGoldenRod3'], rect=employRect)
                        surface.blit(employTxt, (employRect.topleft[0] + 20,
                                                 employRect.topleft[1] + 10))
                        if money >= 250:
                            money -= 250
                            manList.append(
                                man(
                                    pygame.image.load(
                                        'man.bmp').convert_alpha(),
                                    [3.5, 3]), )
                            surface.blit(manList[-1].rightHeadedImage,
                                         manList[-1].rect.topleft)
                            if waitForList != []:
                                manList[-1].destinationList.append([
                                    waitForList[-1].cafe, waitForList[-1].index
                                ])
                        else:
                            lackOfMoney()
                if True:
                    for x in range(9):
                        for y in range(9):
                            if selection == selectCafe and houseRect[x][y][
                                    1] == cafe:
                                if houseRect[x][y][0].collidepoint(
                                        pygame.mouse.get_pos()):
                                    pygame.draw.rect(
                                        surface, colorDict['AntiqueWhite3'],
                                        houseRect[x][y][0])
                                    surface.blit(
                                        cafeImg,
                                        (houseRect[x][y][0].topleft[0] + 5,
                                         houseRect[x][y][0].topleft[1] + 5))
                                elif houseRect[x][y][0].collidepoint(
                                        pygame.mouse.get_pos()) == 0:
                                    pygame.draw.rect(
                                        surface, colorDict['AntiqueWhite2'],
                                        houseRect[x][y][0])
                                    if houseRect[x][y][1] == cafe:
                                        surface.blit(cafeImg, (
                                            houseRect[x][y][0].topleft[0] + 5,
                                            houseRect[x][y][0].topleft[1] + 5))
                                if event.type == MOUSEBUTTONDOWN:  # 点餐厅，开始下单
                                    if houseRect[x][y][0].collidepoint(
                                            event.pos):
                                        pygame.draw.rect(
                                            surface,
                                            colorDict['AntiqueWhite4'],
                                            houseRect[x][y][0])
                                        surface.blit(cafeImg, (
                                            houseRect[x][y][0].topleft[0] + 5,
                                            houseRect[x][y][0].topleft[1] + 5))
                                        cafePos = [x, y]
                                        selection = selectHome
                                if event.type == MOUSEBUTTONUP:
                                    if houseRect[x][y][0].collidepoint(
                                            event.pos):
                                        pygame.draw.rect(
                                            surface,
                                            colorDict['AntiqueWhite3'],
                                            houseRect[x][y][0])
                                        surface.blit(cafeImg, (
                                            houseRect[x][y][0].topleft[0] + 5,
                                            houseRect[x][y][0].topleft[1] + 5))
                            elif selection == selectHome and houseRect[x][y][
                                    1] == home:
                                if houseRect[x][y][0].collidepoint(
                                        pygame.mouse.get_pos()):
                                    pygame.draw.rect(
                                        surface, colorDict['AntiqueWhite3'],
                                        houseRect[x][y][0])
                                    surface.blit(
                                        homeImg,
                                        (houseRect[x][y][0].topleft[0] + 5,
                                         houseRect[x][y][0].topleft[1] + 8))
                                elif houseRect[x][y][0].collidepoint(
                                        pygame.mouse.get_pos()) == 0:
                                    pygame.draw.rect(
                                        surface, colorDict['AntiqueWhite2'],
                                        houseRect[x][y][0])
                                    if houseRect[x][y][1] == home:
                                        surface.blit(homeImg, (
                                            houseRect[x][y][0].topleft[0] + 5,
                                            houseRect[x][y][0].topleft[1] + 8))
                                if event.type == MOUSEBUTTONDOWN:  # 点食客，下单完成
                                    if houseRect[x][y][0].collidepoint(
                                            event.pos):
                                        pygame.draw.rect(
                                            surface,
                                            colorDict['AntiqueWhite4'],
                                            houseRect[x][y][0])
                                        surface.blit(homeImg, (
                                            houseRect[x][y][0].topleft[0] + 5,
                                            houseRect[x][y][0].topleft[1] + 8))
                                        consumerPos = [x, y]
                                        orderNumber += 1
                                        orderList.append(
                                            order(cafePos, consumerPos,
                                                  realTime, orderNumber))
                                        waitForList.append(orderList[-1])
                                        newOrder = 1
                                        for theMan in manList:
                                            if len(theMan.destinationList
                                                   ) == 0:  # 有没事干的，新单给他
                                                orderList[
                                                    -1].waitFor = theMan.index
                                                theMan.destinationList.append([
                                                    waitForList[-1].cafe,
                                                    waitForList[-1].index
                                                ])
                                                newOrder = 0
                                                break
                                        for theMan in manList:
                                            if newOrder == 0:
                                                break
                                            elif theMan.destinationList != []:
                                                if ontheWayAnalysis(  # 找到一个在路上的，新单给他
                                                        theMan,
                                                        orderList[-1].cafe,
                                                        orderList[-1].index):
                                                    orderList[
                                                        -1].waitFor = theMan.index
                                                    break
                                                elif theMan.index == len(
                                                        manList
                                                ):  # 直到最后一个如果还不在他的路上 也给他
                                                    theMan.destinationList.append(
                                                        [
                                                            waitForList[-1].
                                                            cafe,
                                                            waitForList[-1].
                                                            index
                                                        ])
                                                    orderList[
                                                        -1].waitFor = theMan.index
                                                    break
                                if event.type == MOUSEBUTTONUP:
                                    if houseRect[x][y][0].collidepoint(
                                            event.pos):
                                        pygame.draw.rect(
                                            surface,
                                            colorDict['AntiqueWhite2'],
                                            houseRect[x][y][0])
                                        surface.blit(homeImg, (
                                            houseRect[x][y][0].topleft[0] + 5,
                                            houseRect[x][y][0].topleft[1] + 8))
                                        selection = selectCafe
        clock.tick_busy_loop(30)  # 设置帧率30
        for x in manList:
            x.infoUpdate()
        if runCondition == running:
            if money < 0:
                runCondition = gameover('minusMoney')
            for i in (0, 1):
                for j in range(8):
                    surface.fill(colorDict['Snow'], rect=roadRect[i][j])
            for theMan in manList:
                if (theMan.pos[0] % 1 == 0.5 and theMan.pos[1] % 1 == 0) or (
                        theMan.pos[0] % 1 == 0
                        and theMan.pos[1] % 1 == 0.5):  # 到达路中间
                    for anOrder in waitForList:
                        if theMan.pos in arrivalRoadxy(
                                anOrder.cafe) and anOrder.cafeArrived is False:
                            theMan.doingList.append(anOrder)
                            theMan.doNumber += 1
                            anOrder.approachBy = theMan.index
                            anOrder.cafeArrived = True
                            waitForList.remove(anOrder)
                            for anMan in manList:
                                while [anOrder.cafe,
                                       anOrder.index] in anMan.destinationList:
                                    anMan.destinationList.remove(
                                        [anOrder.cafe, anOrder.index])
                            if theMan.destinationList != []:
                                if ontheWayAnalysis(theMan, anOrder.consumer,
                                                    anOrder.index):
                                    pass
                                elif [anOrder.consumer, anOrder.index
                                      ] not in theMan.destinationList:
                                    theMan.destinationList.append(
                                        [anOrder.consumer, anOrder.index])
                            elif [anOrder.consumer,
                                  anOrder.index] not in theMan.destinationList:
                                theMan.destinationList.append(
                                    [anOrder.consumer, anOrder.index])
                    for anOrder in waitForList:
                        if theMan.destinationList != []:
                            if ontheWayAnalysis(theMan, anOrder.cafe,
                                                anOrder.index):
                                anOrder.waitFor = theMan.index
                if (theMan.destinationList != [] and
                    ((theMan.pos[0] % 0.5 == 0 and theMan.pos[1] % 1 == 0) or
                     (theMan.pos[0] % 1 == 0 and theMan.pos[1] % 0.5 == 0))
                    ) or (theMan.pos[0] % 1 == 0
                          and theMan.pos[1] % 1 == 0):  # 要走
                    if theMan.decideDirection() is True:
                        money += 10
                if theMan.direction == right:  # 这四个是向不同方向动骑手
                    theMan.update()
                    surface.blit(theMan.rightHeadedImage, theMan.rect)
                elif theMan.direction == left:
                    theMan.update()
                    surface.blit(theMan.leftHeadedImage, theMan.rect)
                elif theMan.direction == up:
                    theMan.update()
                    surface.blit(theMan.upHeadedImage, theMan.rect)
                elif theMan.direction == down:
                    theMan.update()
                    surface.blit(theMan.downHeadedImage, theMan.rect)
                for doingThing in theMan.doingList:
                    if realTime - doingThing.time > 15 * 60 and doingThing.delay is False:
                        money -= 50
                        doingThing.delay = True
                        theMan.overTimeNumber += 1
                    elif realTime - doingThing.time > 30 * 60:
                        runCondition = gameover('overTime')
            for theMan in manList:
                if theMan.destinationList == [] and waitForList != []:
                    theMan.destinationList.append(
                        [waitForList[-1].cafe, waitForList[-1].index])
                    waitForList[-1].waitFor = theMan.index
        pygame.display.update()


def main():
    pygame.init()
    background = pygame.display.set_mode(
        (1280 + 12, 732), 0,
        32)  # 第一个为元祖，代表分辨率（必须）；第二个是一个标志位，如果不用什么特性，就指定0；第三个为色深
    pygame.display.set_caption('外卖派单模拟系统')
    icon = pygame.image.load('icon.jpg')  # 加载图像
    pygame.display.set_icon(icon)
    titleFont = pygame.font.Font('Deng.ttf', 64)  # 默认路径是在当前cd下，而不是py文件所在位置！
    buttonFont = pygame.font.Font('Deng.ttf', 48)
    tittle = titleFont.render(u"外卖派单模拟系统", True, (255, 255, 255))  # 新建一段文字
    colorDict = {
        'lightGoldenRod1': (255, 236, 139),
        'lightGoldenRod2': (238, 220, 130),
        'lightGoldenRod3': (205, 190, 112),
        'CadetBlue3': (122, 197, 205),
        'Snow': (238, 233, 233),
        'AntiqueWhite2': (238, 223, 204),
        'AntiqueWhite3': (205, 192, 176),
        'AntiqueWhite4': (139, 131, 120),
        'DarkSlateGray': (47, 79, 79)
    }
    start = buttonFont.render(u'开始', True, (0, 0, 0))
    startRect = Rect(640 - 125 + 6, 300, 250, 80)
    instruct = buttonFont.render(u'使用说明', True, (0, 0, 0))
    instructRect = Rect(640 - 125 + 6, 450, 250, 80)
    background.fill(colorDict['CadetBlue3'])  # 给指定的surface填rgb色
    background.blit(tittle, (390 + 6, 140))  # 把对象画到surface上
    pygame.draw.rect(background, colorDict['lightGoldenRod1'],
                     startRect)  # 第一个在谁上面画矩形，第二个颜色，第三个是Rect tuple，含左上角和右下角坐标
    pygame.draw.rect(background, colorDict['lightGoldenRod1'], instructRect)
    background.blit(start, (593 + 6, 315))
    background.blit(instruct, (543 + 6, 467))
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:  # 定义退出动作
                pygame.quit()
                exit()
        if startRect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(background, colorDict['lightGoldenRod2'],
                             startRect)
            background.blit(start, (593 + 6, 315))
        elif startRect.collidepoint(pygame.mouse.get_pos()) == 0:
            pygame.draw.rect(background, colorDict['lightGoldenRod1'],
                             startRect)
            background.blit(start, (593 + 6, 315))
        if instructRect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(background, colorDict['lightGoldenRod2'],
                             instructRect)
            background.blit(instruct, (543 + 6, 467))
        elif instructRect.collidepoint(pygame.mouse.get_pos()) == 0:
            pygame.draw.rect(background, colorDict['lightGoldenRod1'],
                             instructRect)
            background.blit(instruct, (543 + 6, 467))
        if pygame.mouse.get_pressed() == (1, 0, 0):  # 分别为左中右
            if startRect.collidepoint(
                    pygame.mouse.get_pos()):  # 返回的是1和0，不是bool:(
                pygame.draw.rect(background, colorDict['lightGoldenRod3'],
                                 startRect)
                background.blit(start, (593 + 6, 315))
                run(background, colorDict)
            elif instructRect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(background, colorDict['lightGoldenRod3'],
                                 instructRect)
                background.blit(instruct, (543 + 6, 467))
                instruction()
        pygame.display.update()  # 刷新屏幕


if __name__ == "__main__":
    main()
