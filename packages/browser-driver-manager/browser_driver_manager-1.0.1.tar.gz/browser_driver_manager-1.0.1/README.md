# browser_driver_manager

用于管理浏览器驱动程序的下载和安装。该类包含了一些方法来获取本地浏览器版本、提取Chrome版本、获取最新版本的驱动程序版本号和下载链接、检查本地安装的Chromedriver版本、检查Chromedriver是否存在、创建下载文件夹、下载和解压缩浏览器驱动程序等功能。

**类属性**

- **download_dir** (str): 存储下载文件的文件夹路径。

**方法**

1. **\_\_init\_\_(self)**:
   初始化 BrowserDriverManager 类并创建下载文件夹。

2. **get_browser_version(self) -> str**:
   获取本地浏览器版本。
   - Returns: 本地浏览器的版本号。
   - Notes: 此方法仅适用于 Windows 操作系统和 Google Chrome 浏览器。

3. **get_chrome_version(self, browser_version: str) -> str**:
   从浏览器版本中提取 Chrome 版本。
   - Args:
       - browser_version (str): 浏览器版本号。
   - Returns: Chrome 版本号。
   - Notes: 此方法假设浏览器版本号遵循标准的 x.y.z 格式。例如，如果浏览器版本为 "94.0.4606.81"，则提取的 Chrome 版本为 "94.0.4606"。

4. **get_latest_version_and_download_url(self, chrome_version: str) -> Tuple[str, str]**:
   根据 Chrome 版本获取最新版本的驱动程序版本号和下载链接。
   - Args:
       - chrome_version (str): Chrome 版本号。
   - Returns: 包含最新版本的驱动程序版本号和对应的下载链接的元组。
   - Notes: 此方法使用 ChromeDriver 的下载链接模板，并将 Chrome 版本号插入其中。例如，如果 Chrome 版本为 "94.0.4606"，则生成的下载链接为 "https://chromedriver.storage.googleapis.com/94.0.4606/chromedriver_win32.zip"。

5. **get_chromedriver_version(self) -> str or None**:
   获取本地安装的 Chromedriver 版本号。
   - Returns: Chromedriver 版本号，如果未找到版本号则返回 None。

6. **check_chromedriver_exists(self) -> bool**:
   检查 Chromedriver 是否存在于下载文件夹中。
   - Returns: 如果 Chromedriver 存在，则返回 True；否则返回 False。

7. **create_download_folder(self) -> str**:
   在当前工作路径下创建下载文件夹路径。
   - Returns: 下载文件夹的路径。
   - Notes: 如果 "download" 文件夹已经存在，则不进行任何操作。

8. **download_Browser(self, download_url: str) -> str**:
   下载 Browser 驱动程序。
   - Args:
       - download_url (str): 下载链接。
   - Returns: 下载的文件路径。
   - Notes: 此方法使用 requests 库下载文件，并将其保存到指定路径。

9. **extract_Browser(self, download_path: str)**:
   解压缩 Browser 驱动程序。
   - Args:
       - download_path (str): 下载的文件路径。
   - Notes: 此方法使用 zipfile 库解压缩下载的文件，并将文件提取到下载文件夹中。

10. **clean_up(self, download_path: str)**:
    清理下载的文件。
    - Args:
        - download_path (str): 下载的文件路径。
    - Notes: 此方法删除下载的文件，以清理不再需要的文件。

11. **download_Browser_for_current_browser(self)**:
    根据本地浏览器版本下载相应版本的 Browser 驱动程序。

