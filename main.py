from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit
from PyQt6.QtWebEngineCore import QWebEngineHttpRequest, QWebEngineProfile, QWebEngineSettings
from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from path import Path
from sys import argv
import re

HOME = Path(__file__).parent
WEB_VIEW_ALLOWLIST = [
    r"^https://www\.google\.com/.*",
    r"^https://www\.youtube\.com/.*",
    r"^https://www\.youtu\.be/.*",
    # The www is optional
    r"^https://youtube\.com/.*",
    r"^https://youtu\.be/.*",
]

def _(path: str, relative=True) -> Path:
    """
    Construct relative path from HOME
    :param path:
    :return:
    """
    paths = path.split("/")
    cp = HOME if relative else Path()
    for p in paths:
        cp /= p
    return cp


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        loadUi(_("assets/ui/form.ui"), self)
        self.register_ui()
        self.show()

    def register_ui(self):
        self.webView = self.findChild(QWebEngineView, "webView")
        self.urlInput = self.findChild(QLineEdit, "url_input")
        self.goButton = self.findChild(QPushButton, "go_button")

        self.goButton.clicked.connect(self.load_url)
        self.urlInput.returnPressed.connect(self.load_url)
        self.webView.urlChanged.connect(self.on_url_changed)
        self.config_webview(self.webView)

    def load_url(self):
        url = self.urlInput.text()
        self.webView.load(QUrl(url))
        self.urlInput.setText(url)

    def config_webview(self, webview: QWebEngineView):
        wvpp = webview.page().profile()
        wvpps = wvpp.settings()
        wa = QWebEngineSettings.WebAttribute
        wvpp.setHttpAcceptLanguage("en-US,en;q=0.9")
        wvpp.setCachePath(_("webview/cache"))
        wvpp.setHttpCacheMaximumSize(100 * 1024 * 1024) # 100 MB
        wvpp.setHttpCacheType(QWebEngineProfile.HttpCacheType.DiskHttpCache)
        wvpp.setSpellCheckEnabled(False)
        wvpp.setSpellCheckLanguages(["en-US", "en"])
        # Also accept cookies
        wvpp.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies)
        # Set default download path
        wvpp.setDownloadPath(_("webview/downloads"))
        # Set default download directory
        wvpp.setPersistentStoragePath(_("webview/persistentStorage"))
        # Set default local storage path

        def _set_webview_attrs(*attrs: wa):
            for attr in attrs:
                wvpps.setAttribute(attr, True)

        _set_webview_attrs(
            wa.LocalContentCanAccessRemoteUrls,
            wa.LocalContentCanAccessFileUrls,
            wa.LocalStorageEnabled,
            wa.JavascriptEnabled,
            wa.JavascriptCanOpenWindows,
            wa.JavascriptCanAccessClipboard,
            wa.PluginsEnabled,
            wa.ScreenCaptureEnabled,
            wa.WebGLEnabled,
            wa.Accelerated2dCanvasEnabled,
            wa.AutoLoadImages,
            wa.AutoLoadIconsForPage,
            wa.HyperlinkAuditingEnabled,
            wa.SpatialNavigationEnabled,
            wa.ErrorPageEnabled,
            wa.ScrollAnimatorEnabled,
            wa.FullScreenSupportEnabled,
            wa.AllowRunningInsecureContent,
            wa.AllowWindowActivationFromJavaScript,
            wa.ShowScrollBars,
            wa.TouchIconsEnabled,
            wa.FocusOnNavigationEnabled,
            wa.PrintElementBackgrounds,
            wa.PdfViewerEnabled,
        )


        del wvpp, wvpps, wa



    def on_url_changed(self, url: QUrl):
        if url.toString() == "about:blank":
            return
        if not any([re.match(regex, url.toString()) for regex in WEB_VIEW_ALLOWLIST]):
            self.webView.load(QUrl("about:blank"))
            return
        self.urlInput.setText(url.toString())

if __name__ == '__main__':
    app = QApplication(argv)
    window = MainWindow()
    app.exec()
