#!usr/bin/evn python
# @-_-@ coding=utf-8 @-_-@

from __future__ import division
import re
from math import sqrt

#自定义余弦定理算法模块

class Similarity(object):
    def __init__(self, target1, target2):
        self.target1 = target1
        self.target2 = target2


    def vector(self):
        self.vdict1 = {}
        self.vdict2 = {}
        for target in re.findall('([a-zA-Z0-9_.&%]+)+', self.target1):
            self.vdict1[target] = self.vdict1.get(target, 0) + 1

        for target in re.findall('([a-zA-Z0-9_.&%]+)+', self.target2):
            self.vdict2[target] = self.vdict2.get(target, 0) + 1
        # print self.vdict1
        # print self.vdict2


    def mix(self):
        for key in self.vdict1:
            self.vdict2[key] = self.vdict2.get(key, 0)
        for key in self.vdict2:
            self.vdict1[key] = self.vdict1.get(key, 0)

        print self.vdict1
        print self.vdict2

    def similar(self):
        self.vector()
        self.mix()
        sum = 0
        for key in self.vdict1:
            sum += self.vdict1[key] * self.vdict2[key]
        A = sqrt(reduce(lambda x,y: x+y, map(lambda x: x*x, self.vdict1.values())))
        B = sqrt(reduce(lambda x,y: x+y, map(lambda x: x*x, self.vdict2.values())))
        return   sum/(A*B)


if __name__ == '__main__':
	t1 = "yumhh in in good people"
	t2 = "yumh in good people"
	t3 = "yumh good in people"
	s = Similarity(t1, t2)
	s2 = Similarity(t2, t3)
	print 't1 * t2: ',s.similar()
	print 't2 * t3: ',s2.similar()

