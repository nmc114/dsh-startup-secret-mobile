import sys, time, json
import gi
gi.require_version('Gtk','3.0')
gi.require_version('WebKit2','4.1')
from gi.repository import Gtk, WebKit2, GLib

W = int(sys.argv[1]); H = int(sys.argv[2]); URL = sys.argv[3]; OUT = sys.argv[4]; WAIT = float(sys.argv[5])
JS = sys.argv[6] if len(sys.argv) > 6 else ''

win = Gtk.Window()
win.set_default_size(W, H)
win.set_resizable(False)
view = WebKit2.WebView()
win.add(view)
win.show_all()
win.resize(W, H)

state = {'done': False}

def snap():
    if JS:
        view.run_javascript(JS, None, None, None)
    GLib.timeout_add(int(WAIT*1000), do_snap)
    return False

def do_snap():
    view.get_snapshot(WebKit2.SnapshotRegion.VISIBLE, WebKit2.SnapshotOptions.NONE, None, on_snapshot, None)
    return False

def on_snapshot(webview, result, data):
    try:
        surf = webview.get_snapshot_finish(result)
        surf.write_to_png(OUT)
        print('SNAP', OUT, surf.get_width(), surf.get_height())
    except Exception as e:
        print('ERR', e)
    Gtk.main_quit()

def on_load(view, event):
    if event == WebKit2.LoadEvent.FINISHED:
        GLib.timeout_add(int(WAIT*1000), do_snap)
        if JS:
            GLib.timeout_add(200, lambda: view.run_javascript(JS, None, None, None))

view.connect('load-changed', on_load)
view.load_uri(URL)
GLib.timeout_add(30000, Gtk.main_quit)
Gtk.main()
