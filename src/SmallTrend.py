# -*- coding:utf-8 -*-
"""
Created on Aug 26, 2013

@author: Filip
"""
import numpy as np
import PyTango as pt
import pyqtgraph as pq
from PyQt4 import QtGui, QtCore
import sys
import time

class SmallTrend(QtGui.QWidget):
	def __init__(self, parent = None):
		QtGui.QWidget.__init__(self,parent)
		
		self.maxDataSize = 2000
		self.xSpan = 200.0
		self.ySpan = 1.0
		self.xScale = self.size().width() / self.xSpan
		self.yScale = self.size().height() / self.ySpan
		
		self.xData = np.zeros(self.maxDataSize)
		self.yData = np.zeros(self.maxDataSize)
		self.xData[0] = time.time()
		self.paintPath = QtGui.QPainterPath(QtCore.QPointF((self.xData[0]-self.xData[0])*self.xScale, self.yData[0]))
		self.xPos = 0
		self.xNum = 1	
# 		self.xData[self.xPos]=time.time()	
# 		for p in range(self.xNum):
# 			index = p + self.xPos
# 			self.paintPath.lineTo((self.xData[self.xPos+p]-self.xData[0])*self.xScale, self.yData[self.xPos+p])
			
		self.curvePen = QtGui.QPen(QtGui.QColor(0x99ccff))
		self.curvePen.setWidthF(1.3)
		self.axisPen = QtGui.QPen(QtGui.QColor(0xffcc66))
		self.axisPen.setWidthF(1.0)
		
		self.setMinimumWidth(200)
		self.setMinimumHeight(200)
				
			
	def updateData(self, xNew, yNew):
		self.xPos += 1
		if self.xPos >= self.maxDataSize:
			self.xPos = 0
		self.xData[self.xPos]=xNew	
		self.yData[self.xPos]=yNew

		self.xNum += 1	
		if self.xNum > self.maxDataSize:
			self.xNum = self.maxDataSize
#		self.paintPath = QtGui.QPainterPath(QtCore.QPointF(self.xData[self.xPos], self.yData[self.xPos]))
		print 'xNum', self.xNum
		self.paintPath = QtGui.QPainterPath(QtCore.QPointF((self.xData[0]-self.xData[0])*self.xScale, self.yData[0]))
		for p in range(self.xNum):
			index = p #+ self.xPos
			print index
			print (self.xData[index]-self.xData[0])*self.xScale
			print self.yData[index]*self.yScale			
			self.paintPath.lineTo((self.xData[index]-self.xData[0])*self.xScale, self.yData[index]*self.yScale)
			
		self.update()
	
	def resizeEvent(self, e):
		self.xScale = self.size().width() / self.xSpan
		self.yScale = self.size().height() / self.ySpan
		print 'In resizeEvent: scale ', self.xScale, self.yScale
		
	def paintEvent(self, e):
		qp = QtGui.QPainter()
		qp.begin(self)
		qp.setRenderHint(QtGui.QPainter.Antialiasing)
		qp.setPen(QtCore.Qt.blue)
		qp.drawPath(self.paintPath)
		qp.end()
		
class TrendTest(QtGui.QWidget):
	def __init__(self, parent = None):
		QtGui.QWidget.__init__(self, parent)

		self.deviceName = 'testfel/gunlaser/finesse'
	
		self.deviceFinesse = pt.DeviceProxy(self.deviceName)

		layout = QtGui.QVBoxLayout(self)
		self.trendWidget = SmallTrend()
		label = QtGui.QLabel(''.join(('Trending ', self.deviceName)))
		layout.addWidget(label)
		layout.addWidget(self.trendWidget)
		
		self.timer = QtCore.QTimer()
		QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.updateData)
		self.timer.start(500)
		
	def updateData(self):
		self.trendWidget.updateData(time.time(), np.random.rand())
		

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	myapp = TrendTest()
	myapp.show()
	sys.exit(app.exec_())	
