#
# Author: Bo Maryniuk <bo@suse.de>
#
# Copyright (c) 2013 Bo Maryniuk. All Rights Reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     1. Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#
#     2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
#     3. The name of the author may not be used to endorse or promote products
#     derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY BO MARYNIUK "AS IS" AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import sys

class CLIProgressWidget:
    def __init__(self, items, width=None, out=sys.stderr):
        self.items = items # Items to itemize
        self.width = width and width or 100
        self.out = out
        self._cursor = 0

        # How widget looks like
        self.cfg_prefix = "|"
        self.cfg_suffix = "|"
        self.cfg_label_prefix = "<"
        self.cfg_label_suffix = ">"
        self.cfg_done = "#"
        self.cfg_todo = "."


    def _render(self):
        """
        Render current state of the widget.
        """
        completed = int(round((self._cursor / float(self.items)) * self.width))
        clabel = int(round((self._cursor / float(self.items)) * 100))
        label = "%s%s%%%s" % (self.cfg_label_prefix, clabel, self.cfg_label_suffix)
        r = [self.cfg_prefix]

        if completed - len(label) < len(label):
            r.append(label + (self.cfg_todo * (self.width - len(label))))
        else:
            r.append((self.cfg_done * (completed - len(label))) + label)
            if len(r[-1]) < self.width:
                r.append(self.cfg_todo * (self.width - len(r[-1])))
        r.append(self.cfg_suffix)

        return ''.join(r)


    def next(self):
        """
        Move to the next item.
        """
        self._cursor += 1
        self.out.write("\r" + self._render())
        self.out.flush()


    def finish(self):
        """
        Remove the widget (clear).
        """
        self.out.write("\r" + (" " * (self.width + 2)))
        self.out.flush()


    def finished(self):
        return self._cursor == self.items


    def reset(self):
        self._cursor = 0
        self.out.write("\r" + self._render())
        self.out.flush()


# Simple test
if __name__ == '__main__':
    import time
    speed = 0.1
    for v in [2, 5, 8, 10, 15, 25, 123]:
        print "Testing value", v
        progress = CLIProgressWidget(v, width=80)
        progress.reset()
        time.sleep(speed)
        while not progress.finished():
            progress.next()
            time.sleep(speed)
        progress.finish()
        print "\r",
