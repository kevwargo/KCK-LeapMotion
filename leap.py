#!/usr/bin/python2

import Leap, sys
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

from wmiface import *

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    

    def on_init(self, controller):
        currentSwipe = None
        swipeCount = 0
        print('inited')

    def on_connect(self, controller):
        # controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
        # controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        # controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        print('connected and enabled swipe')

    def on_frame(self, controller):
        frame = controller.frame()
        gestures = frame.gestures()
        if len(gestures):
            for gesture in gestures:
                if gesture.type == Leap.Gesture.TYPE_SWIPE:
                    swipe = SwipeGesture(gesture)
                    if gesture.id == self.currentSwipe:
                        self.swipeCount += 1
                    else:
                        self.swipeCount = 1
                    if self.swipeCount == 6:
                        if swipe.direction[0] > 0:
                            wmLeftDesktop()
                            # print 'right', gesture.id
                        else:
                            wmRightDesktop()
                            # print 'left', gesture.id
                    self.currentSwipe = gesture.id
                if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                    tap = ScreenTapGesture(gesture)
                    # print(self.convertCoord(tap.position[0], tap.position[1]))
                    wmActivateWindow(wmFindWindowAt(*self.convertCoord(tap.position[0], tap.position[1])))
            # print('----------------------------------------------------')
        else:
            self.currentSwipe = None
            self.swipeCount = 0

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
