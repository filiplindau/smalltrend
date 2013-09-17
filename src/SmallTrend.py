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
		self.bkgColor = QtGui.QColor(0x000000)
		self.axisColor = QtGui.QColor(0xffcc66)
		self.crvColor = QtGui.QColor(0x99ccff)
		
		QtGui.QWidget.__init__(self,parent)
		
		self.maxDataSize = 20000
		self.xSpan = 50.0
		self.ySpan = 1.5
 		self.axisOffset = 10
		self.xScale = (self.size().width() - self.axisOffset*2) / self.xSpan		
		self.yScale = (self.size().height() - self.axisOffset*2) / self.ySpan

		
		
		self.xData = np.zeros(self.maxDataSize)
		self.yData = np.zeros(self.maxDataSize)
		self.xData[0] = time.time()
		self.paintPath = QtGui.QPainterPath(QtCore.QPointF((self.xData[0]-self.xData[0])*self.xScale, self.yData[0]))
		self.dataPoly = QtGui.QPolygonF()
		self.dataPoly.append(QtCore.QPointF(self.width()-self.axisOffset,self.height()-self.axisOffset))
#		self.dataPoly.append(QtCore.QPointF(self.xSpan,0))
		print self.dataPoly.at(0)
		print self.dataPoly.at(1)
		self.xPos = 0
		self.xNum = 1	
# 		self.xData[self.xPos]=time.time()	
# 		for p in range(self.xNum):
# 			index = p + self.xPos
# 			self.paintPath.lineTo((self.xData[self.xPos+p]-self.xData[0])*self.xScale, self.yData[self.xPos+p])
			
		self.curvePen = QtGui.QPen(self.crvColor)
		self.curvePen.setWidthF(1.3)
		crvFillColor = self.crvColor
#		crvFillColor = QtGui.QColor(0x3399ff)
		crvFillColor.setAlphaF(0.5)
		self.curveBrush = QtGui.QBrush(crvFillColor)
		self.curveBrush.setStyle = QtCore.Qt.SolidPattern
		self.axisPen = QtGui.QPen(self.axisColor)
		self.axisPen.setWidthF(1.5)
		self.axisBrush = QtGui.QBrush()
		self.axisBrush.setStyle = QtCore.Qt.NoBrush
		self.axisFont = QtGui.QFont('Segoe UI', 8)
		self.axisFont = QtGui.QFont('calibri', 8)
		self.axisFontHeight = QtGui.QFontMetricsF(self.axisFont).height()
		
		self.setMinimumWidth(50)
		self.setMinimumHeight(40)
		self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
		p = self.palette()
		p.setColor(self.backgroundRole(), self.bkgColor)
		self.setPalette(p)
		self.setAutoFillBackground(True)

		self.axisRect = QtCore.QRectF(10.0, 10.0, self.size().width(), self.size().height())		
		self.viewRect = QtCore.QRectF(0,-0.01,self.xSpan,2*self.ySpan)
		
		
				
			
	def updateData(self, xNew, yNew):
		self.xPos += 1
		if self.xPos >= self.maxDataSize:
			self.xPos = 0
		self.xData[self.xPos]=xNew	
		self.yData[self.xPos]=yNew

		self.xNum += 1	
		if self.xNum > self.maxDataSize:
			self.xNum = self.maxDataSize

		self.dataPoly.replace(self.dataPoly.count()-1, QtCore.QPointF(self.width()-self.axisOffset-(xNew - self.xData[0])*self.xScale, self.height()-self.axisOffset-yNew*self.yScale))
		self.dataPoly.append(QtCore.QPointF(self.width()-self.axisOffset-(xNew - self.xData[0])*self.xScale, self.height()-self.axisOffset))


		self.update()


	def paintEvent(self, e):
		print "In paintEvent:"
#		print rect.x(), rect.y()
 		right = self.width()-2*self.axisOffset
 		bottom = self.height()-2*self.axisOffset
 		painter = QtGui.QPainter()
 		painter.begin(self)
  		painter.setWorldMatrixEnabled(False)
  		painter.setRenderHint(QtGui.QPainter.Antialiasing, True)  	
  		painter.setPen(self.curvePen)
  		painter.setBrush(self.curveBrush)
  		painter.drawPolygon(self.dataPoly)
  		painter.setPen(self.axisPen)
  		painter.setBrush(self.axisBrush)
  		painter.setFont(self.axisFont)
  		painter.drawRect(self.axisOffset, self.axisOffset, right, bottom)
  		painter.drawText(self.axisOffset+2, bottom+self.axisOffset-2, str(self.xSpan))
  		s = str(self.ySpan)
  		painter.drawText(right-QtGui.QFontMetricsF(self.axisFont).width(s)+8, self.axisOffset+self.axisFontHeight-3, s)
 		painter.end()
		
	
	def resizeEvent(self, e):
		self.xScale = (self.size().width() - self.axisOffset*2) / self.xSpan		
		self.yScale = (self.size().height() - self.axisOffset*2) / self.ySpan
		print 'In resizeEvent: scale ', self.xScale, self.yScale
		print 'Extents: ', self.size().width(), self.size().height() 
		self.dataPoly = QtGui.QPolygonF()
		self.dataPoly.append(QtCore.QPointF(self.width() - self.axisOffset,self.height() - self.axisOffset))
#		self.dataPoly.append(QtCore.QPointF(self.xSpan,0))
		for ind in range(self.xData.shape[0]-1):
			self.dataPoly.append(QtCore.QPointF(self.width()-self.axisOffset-(self.xData[ind+1] - self.xData[0])*self.xScale, self.height()-self.axisOffset-self.yData[ind+1]*self.yScale))
		self.dataPoly.append(QtCore.QPointF(self.width()-self.axisOffset-(self.xData[-1] - self.xData[0])*self.xScale, self.height()-self.axisOffset))
		
		

		
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
		self.timer.start(200)
		
	def updateData(self):
		self.trendWidget.updateData(time.time(), np.random.rand())
		

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	myapp = TrendTest()
	myapp.show()
	sys.exit(app.exec_())	
