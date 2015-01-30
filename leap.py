#!/usr/bin/python2

import Leap, sys
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from time import time

from wmiface import *

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']



    def on_init(self, controller):
        self.currentSwipe = None
        self.swipeCount = 0
        self.minimized = {}
        self.grabbed_window = None
        # self.prev_palm_position
        print('inited')

    def on_connect(self, controller):
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
        # controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        # controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);

        controller.config.set('Gesture.Swipe.MinVelocity', 500)
        controller.config.set('Gesture.Swipe.MinLength', 80)
        print('connected and enabled swipe')

    def on_frame(self, controller):
        frame = controller.frame()
        gestures = frame.gestures()
        if len(gestures):
            for gesture in gestures:
                if gesture.type == Leap.Gesture.TYPE_SWIPE:
                    swipe = SwipeGesture(gesture)
                    # print gesture.id, swipe.direction
                    if gesture.id == self.currentSwipe:
                        self.swipeCount += 1
                        if self.swipeCount == 6:
                            if abs(swipe.direction[0]) > abs(swipe.direction[1]):
                                if swipe.direction[0] > 0:
                                    wmLeftDesktop()
                                    # print 'left'
                                else:
                                    wmRightDesktop()
                                    # print 'right'
                            else:
                                if swipe.direction[1] > 0:
                                    m = self.minimized.get(wmGetCurrentDesktop())
                                    if m:
                                        w = m.pop(0)
                                        wmUnminimize(w)
                                    # print 'up'
                                else:
                                    w = wmGetActiveWindow()
                                    wmMinimize(w)
                                    d = wmGetCurrentDesktop()
                                    if not self.minimized.get(d):
                                        self.minimized[d] = []
                                    self.minimized[d].insert(0, w)
                                    # print 'down'
                    else:
                        self.swipeCount = 1
                    self.currentSwipe = gesture.id
                if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                    tap = ScreenTapGesture(gesture)
                    # print(self.convertCoord(tap.position[0], tap.position[1]))
                    w = wmFindWindowAt(*self.convertCoord(tap.position[0], tap.position[1]))
                    if w:
                        wmActivateWindow(w)
            # print('----------------------------------------------------')
        else:
            self.currentSwipe = None
            self.swipeCount = 0
            # print 'NO'

        for hand in frame.hands:
            if hand.pinch_strength > 0.9:
                if not self.grabbed_window:
                    w = wmFindWindowAt(*self.convertCoord(hand.stabilized_palm_position[0], hand.stabilized_palm_position[1]))
                    if w:
                        wmActivateWindow(w)
                        self.grabbed_window = w
                        self.prev_palm_pos = self.convertCoord(
                            hand.stabilized_palm_position[0],
                            hand.stabilized_palm_position[1])
                else:
                    x, y = self.convertCoord(hand.stabilized_palm_position[0],
                                             hand.stabilized_palm_position[1])
                    dx = x - self.prev_palm_pos[0]
                    dy = y - self.prev_palm_pos[1]
                    self.prev_palm_pos = x, y
                    wmMoveWindowRelatively(self.grabbed_window, dx, dy)
            else:
                self.grabbed_window = None


    def convertCoord(self, xTap, yTap):
        xMin, xMax = -120, 140
        yMin, yMax = 120, 270
        x = float(xTap - xMin) / (xMax - xMin) * 1366
        y = (1 - float(yTap - yMin) / (yMax - yMin)) * 768
        return int(x), int(y)


def main():
    listener = SampleListener()
    controller = Leap.Controller()
    controller.add_listener(listener)
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)


if __name__ == '__main__':
    # wmRightDesktop()
    # print wmFindWindowAt(int(sys.argv[1]), int(sys.argv[2]))
    main()
