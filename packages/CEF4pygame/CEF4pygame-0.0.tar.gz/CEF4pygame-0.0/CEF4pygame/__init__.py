# from CEF4pygame import CEFpygame,pygame
# browser=CEFpygame(
    # URL='https://youtube.com/',
    # VIEWPORT_SIZE=(800,500)
# )


# pygame.init()
# display_width = 900
# display_height = 600
# display = pygame.display.set_mode((display_width,display_height))
# run=1
# while run:
    # events=pygame.event.get()
    # pygame.key.set_repeat(500,100)
    # keys=pygame.key.get_pressed()
    # alt_pressed=keys[1073742050]
    # ctrl_pressed=keys[1073742048]
    # shift_pressed=keys[pygame.K_LSHIFT]
    # for event in events:
        # if event.type == pygame.QUIT:
            # run=0
        # if event.type == pygame.MOUSEMOTION:
            # browser.motion_at(event.pos[0]-50,event.pos[1]-70,alt=alt_pressed,shift=shift_pressed,control=ctrl_pressed)
        # if event.type == pygame.MOUSEBUTTONDOWN:
            # browser.mousedown_at(event.pos[0]-50,event.pos[1]-70,event.button,alt=alt_pressed,shift=shift_pressed,control=ctrl_pressed)
        # if event.type == pygame.MOUSEBUTTONUP:
            # browser.mouseup_at(event.pos[0]-50,event.pos[1]-70,event.button,alt=alt_pressed,shift=shift_pressed,control=ctrl_pressed)
        # if event.type == pygame.KEYDOWN:
            # browser.keydown(event.key,alt=alt_pressed,shift=shift_pressed,control=ctrl_pressed)
        # if event.type == pygame.KEYUP:
            # browser.keyup(event.key,alt=alt_pressed,shift=shift_pressed,control=ctrl_pressed)
    # display.blit(browser.image, (50,70))
    # pygame.display.update()

import pygame
from cefpython3 import cefpython as cef
import os
import sys
from threading import Thread

Shift=cef.EVENTFLAG_SHIFT_DOWN
Ctrl=cef.EVENTFLAG_CONTROL_DOWN
Alt=cef.EVENTFLAG_ALT_DOWN
keys={
    pygame.K_LSHIFT:16,
    pygame.K_RSHIFT:16,
    1073742048:17,#control
    1073742050:18,#ALT
    1073741881:20,#caps lock
    1073741925:93,#rightclick
    1073742051:91,#command key
    1073741898:36,#home
    1073741901:35,#end
    1073741899:33,#pg up
    1073741902:34,#pg down
    1073741907:144,#num lock
    1073741909:42,#numpad *
    1073741911:43,#numpad +
    1073741910:45,#numpad -
    1073741923:46,#numpad .
    1073741908:47,#numpad /
    1073741922:48,#numpad 0
    1073741913:49,#numpad 1
    1073741914:50,#numpad 2
    1073741915:51,#numpad 3
    1073741916:52,#numpad 4
    1073741917:53,#numpad 5
    1073741918:54,#numpad 6
    1073741919:55,#numpad 7
    1073741920:56,#numpad 8
    1073741921:57,#numpad 9
    1073741912:13,#numpad enter
    1073742086:173,#mute
    1073741882:112,#F1
    1073741883:113,#F2
    1073741884:114,#F3
    1073741885:115,#F4
    1073741886:116,#F5
    1073741887:117,#F6
    1073741888:118,#F7
    1073741889:119,#F8
    1073741890:120,#F9
    1073741891:121,#F10
    1073741892:122,#F11
    1073741893:123,#F12
    1073741894:44,#PrintScreen
    1073741895:145,#Scroll Lock
    1073742082:176,#Next
    1073742083:177,#Prev
    1073742084:178,#Stop
    1073742085:179,#Play/pause
    1073741952:174,#Less volume
    1073741953:175,#More volume
    pygame.K_LEFT:37,
    pygame.K_RIGHT:39,
    pygame.K_UP:38,
    pygame.K_DOWN:40,
}
sys.excepthook = cef.ExceptHook
class LoadHandler(object):
    def OnLoadingStateChange(self, browser, is_loading, **_):
        if not is_loading:
            #sys.stdout.write(os.linesep)
            pass
    def OnLoadError(self, browser, frame, error_code, failed_url, **_):
        if not frame.IsMain():
            return
        cef.PostTask(cef.TID_UI, exit_app, browser)
class RenderHandler(object):
    def __init__(self,VIEWPORT_SIZE):
        self.OnPaint_called = False
        self.VIEWPORT_SIZE = VIEWPORT_SIZE
    def GetViewRect(self, rect_out, **_):
        rect_out.extend([0, 0, self.VIEWPORT_SIZE[0], self.VIEWPORT_SIZE[1]])
        return True

    def OnPaint(self, browser, element_type, paint_buffer, **_):
        if self.OnPaint_called:
            #sys.stdout.write(".")
            #sys.stdout.flush()
            pass
        else:
            self.OnPaint_called = True
        if element_type == cef.PET_VIEW:
            buffer_string = paint_buffer.GetBytes(mode="rgba",origin="top-left")
            browser.SetUserData("OnPaint.buffer_string", buffer_string)
        else:
            raise Exception("Unsupported element_type in OnPaint")
class CEFpygame():
    def __init__(self,URL="https://google.com/",VIEWPORT_SIZE=(900, 600)):
        assert cef.__version__ >= "57.0", "CEF Python v57.0+ required to run this"
        self.VIEWPORT_SIZE=VIEWPORT_SIZE
        print(self.VIEWPORT_SIZE)
        settings = {
            "windowless_rendering_enabled": True,
            'context_menu':{
                "enabled":True,
                "navigation":True,
                "view_source":True,
                "external_browser":False,
                "inspect_element_at":True,
                "print":True,
                "devtools":True
            }
        }
        switches = {
            # GPU acceleration is not supported in OSR mode, so must disable
            # it using these Chromium switches (Issue #240 and #463)
            "disable-gpu": "",
            "disable-gpu-compositing": "",
            "disable-threaded-scrolling": "",
            # Tweaking OSR performance by setting the same Chromium flags
            # as in upstream cefclient (Issue #240).
            "enable-begin-frame-scheduling": "",
            "disable-surfaces": "",  # This is required for PDF ext to work
        }
        browser_settings = {
            "windowless_frame_rate": 30,  # Default frame rate in CEF is 30
        }
        cef.Initialize(settings=settings, switches=switches)
        parent_window_handle = 0
        window_info = cef.WindowInfo()
        window_info.SetAsOffscreen(parent_window_handle)
        self.browser = cef.CreateBrowserSync(window_info=window_info,settings=browser_settings,url=URL)
        self.browser.SetClientHandler(LoadHandler())
        self.browser.SetClientHandler(RenderHandler(VIEWPORT_SIZE))
        self.browser.SendFocusEvent(True)
        self.browser.WasResized()
    def get_screenshot(self):
        cef.MessageLoopWork()
        buffer_string = self.browser.GetUserData("OnPaint.buffer_string")
        if not buffer_string:
            #raise Exception("buffer_string is empty, OnPaint never called?")
            buffer_string=b'\xff\x00\x00\xff'*(self.VIEWPORT_SIZE[0]*self.VIEWPORT_SIZE[1])
        return buffer_string
    @property
    def image(self):
        cef.MessageLoopWork()
        buffer_string = self.browser.GetUserData("OnPaint.buffer_string")
        if not buffer_string:
            #raise Exception("buffer_string is empty, OnPaint never called?")
            buffer_string=b'\x00\x00\x33\xff'*(self.VIEWPORT_SIZE[0]*self.VIEWPORT_SIZE[1])
        return pygame.image.frombuffer(buffer_string,(self.VIEWPORT_SIZE[0],self.VIEWPORT_SIZE[1]),'RGBA')
    def exit_app(self):
        self.browser.CloseBrowser()
        #cef.QuitMessageLoop()
    def click_at(self,x,y,button=1,alt=False,shift=False,control=False):
        modifiers=(Alt if alt else 0)|(Shift if shift else 0)|(Ctrl if control else 0)
        if button==1:
            self.browser.SendMouseClickEvent(x,y,cef.MOUSEBUTTON_LEFT,False,1,modifiers)
            self.browser.SendMouseClickEvent(x,y,cef.MOUSEBUTTON_LEFT,True,1,modifiers)
        if button==3:
            self.browser.SendMouseClickEvent(x,y,cef.MOUSEBUTTON_RIGHT,False,1,modifiers)
            self.browser.SendMouseClickEvent(x,y,cef.MOUSEBUTTON_RIGHT,True,1,modifiers)
        #print('Click!')
    def mousedown_at(self,x,y,button=1,alt=False,shift=False,control=False):
        modifiers=(Alt if alt else 0)|(Shift if shift else 0)|(Ctrl if control else 0)
        if button==1:self.browser.SendMouseClickEvent(x,y,cef.MOUSEBUTTON_LEFT,False,1,modifiers)
        if button==3:self.browser.SendMouseClickEvent(x,y,cef.MOUSEBUTTON_RIGHT,False,1,modifiers)
        if button==4:self.browser.SendMouseWheelEvent(0, 0,x,y*.5,modifiers)
        if button==5:self.browser.SendMouseWheelEvent(0, 0,x,-y*.5,modifiers)
        #print('Mousedown!',button)
    def mouseup_at(self,x,y,button=1,alt=False,shift=False,control=False):
        modifiers=(Alt if alt else 0)|(Shift if shift else 0)|(Ctrl if control else 0)
        if button==1:self.browser.SendMouseClickEvent(x,y,cef.MOUSEBUTTON_LEFT,True,1,modifiers)
        if button==3:self.browser.SendMouseClickEvent(x,y,cef.MOUSEBUTTON_RIGHT,True,1,modifiers)
        #if button==4:self.browser.SendMouseWheelEvent(0, 0,x,y*.5,modifiers)
        #if button==5:self.browser.SendMouseWheelEvent(0, 0,x,-y*.5,modifiers)
        #print('Mouseup!',button)
    def motion_at(self,x,y,alt=False,shift=False,control=False):
        modifiers=(Alt if alt else 0)|(Shift if shift else 0)|(Ctrl if control else 0)
        self.browser.SendMouseMoveEvent(x,y,False,modifiers=modifiers)
    def keyup(self,key,alt=False,shift=False,control=False):
        if key>10000:
            key=keys[key]
        key_event = {
            "type": cef.KEYEVENT_KEYUP,
            "windows_key_code": key,
            "character": key,
            "unmodified_character": key,
            "modifiers": (Alt if alt else 0)|(Shift if shift else 0)|(Ctrl if control else 0)
        }
        try:
            self.browser.SendKeyEvent(key_event)
        except:pass
        #print(key)
    def keydown(self,key,alt=False,shift=False,control=False):
        if key>10000:
            key=keys[key]
        key_event = {
            "type": cef.KEYEVENT_KEYDOWN,
            "windows_key_code": key,
            "native_key_code": key,
            "character": 0,
            "unmodified_character": 0,
            "modifiers": (Alt if alt else 0)|(Shift if shift else 0)|(Ctrl if control else 0)
        }
        try:
            self.browser.SendKeyEvent(key_event)
        except:pass
        key_event = {
            "type": cef.KEYEVENT_CHAR,
            "windows_key_code": key,
            "character": key,
            "unmodified_character": key,
            "modifiers": (Alt if alt else 0)|(Shift if shift else 0)|(Ctrl if control else 0)
        }
        try:
            self.browser.SendKeyEvent(key_event)
        except:pass
        #print(key)
def get_screenshot(browser):
    buffer_string = browser.GetUserData("OnPaint.buffer_string")
    if not buffer_string:
        raise Exception("buffer_string is empty, OnPaint never called?")
    return buffer_string
def exit_app(browser):
    browser.CloseBrowser()
    cef.QuitMessageLoop()