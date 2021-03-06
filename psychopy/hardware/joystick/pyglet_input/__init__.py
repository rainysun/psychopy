# ----------------------------------------------------------------------------
# pyglet
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

'''Joystick, tablet and USB HID device support.

This module provides a unified interface to almost any input device, besides
the regular mouse and keyboard support provided by `Window`.  At the lowest
level, `get_devices` can be used to retrieve a list of all supported devices,
including joysticks, tablets, space controllers, wheels, pedals, remote
controls, keyboards and mice.  The set of returned devices varies greatly
depending on the operating system (and, of course, what's plugged in).

At this level pyglet does not try to interpret *what* a particular device is,
merely what controls it provides.  A `Control` can be either a button, whose
value is either ``True`` or ``False``, or a relative or absolute-valued axis,
whose value is a float.  Sometimes the name of a control can be provided (for
example, ``x``, representing the horizontal axis of a joystick), but often
not.  In these cases the device API may still be useful -- the user will have
to be asked to press each button in turn or move each axis separately to
identify them.

Higher-level interfaces are provided for joysticks, tablets and the Apple
remote control.  These devices can usually be identified by pyglet positively,
and a base level of functionality for each one provided through a common
interface.

To use an input device:

1. Call `get_devices`, `get_apple_remote` or `get_joysticks`
   to retrieve and identify the device.
2. For low-level devices (retrieved by `get_devices`), query the devices
   list of controls and determine which ones you are interested in.  For
   high-level interfaces the set of controls is provided by the interface.
3. Optionally attach event handlers to controls on the device.
4. Call `Device.open` to begin receiving events on the device.  You can
   begin querying the control values after this time; they will be updated
   asynchronously.
5. Call `Device.close` when you are finished with the device (not needed
   if your application quits at this time).

To use a tablet, follow the procedure above using `get_tablets`, but note that
no control list is available; instead, calling `Tablet.open` returns a
`TabletCanvas` onto which you should set your event handlers.

:since: pyglet 1.2

'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import sys

from base import Device, Control, RelativeAxis, AbsoluteAxis, \
                 Button, Joystick, AppleRemote, Tablet
from base import DeviceException, DeviceOpenException, DeviceExclusiveException

_is_epydoc = hasattr(sys, 'is_epydoc') and sys.is_epydoc

def get_apple_remote(display=None):
    '''Get the Apple remote control device.

    The Apple remote is the small white 6-button remote control that
    accompanies most recent Apple desktops and laptops.  The remote can only
    be used with Mac OS X.

    :Parameters:
        `display` : `Display`
            Currently ignored.

    :rtype: `AppleRemote`
    :return: The remote device, or ``None`` if the computer does not support
        it.
    '''
    return None

if _is_epydoc:
    def get_devices(display=None):
        '''Get a list of all attached input devices.

        :Parameters:
            `display` : `Display`
                The display device to query for input devices.  Ignored on Mac
                OS X and Windows.  On Linux, defaults to the default display
                device.

        :rtype: list of `Device`
        '''

    def get_joysticks(display=None):
        '''Get a list of attached joysticks.

        :Parameters:
            `display` : `Display`
                The display device to query for input devices.  Ignored on Mac
                OS X and Windows.  On Linux, defaults to the default display
                device.

        :rtype: list of `Joystick`
        '''

    def get_tablets(display=None):
        '''Get a list of tablets.

        This function may return a valid tablet device even if one is not
        attached (for example, it is not possible on Mac OS X to determine if
        a tablet device is connected).  Despite returning a list of tablets,
        pyglet does not currently support multiple tablets, and the behaviour
        is undefined if more than one is attached.

        :Parameters:
            `display` : `Display`
                The display device to query for input devices.  Ignored on Mac
                OS X and Windows.  On Linux, defaults to the default display
                device.

        :rtype: list of `Tablet`
        '''
else:
    def get_tablets(display=None):
        return []

    if sys.platform == 'linux2':
        from x11_xinput import get_devices as xinput_get_devices
        from x11_xinput_tablet import get_tablets
        from evdev import get_devices as evdev_get_devices
        from evdev import get_joysticks
        def get_devices(display=None):
            return (evdev_get_devices(display) +
                    xinput_get_devices(display))
    elif sys.platform in ('cygwin', 'win32'):
        from directinput import get_devices, get_joysticks
        try:
            from wintab import get_tablets
        except:
            pass
    elif sys.platform == 'darwin':
        from pyglet import options as pyglet_options
        from darwin_hid import get_devices, get_joysticks, get_apple_remote
