import json
import re
from time import sleep

import chromedriver_autoinstaller
import cloudscraper
import requests
from bs4 import BeautifulSoup
from lk21 import Bypass
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from bot.config import *
from bot.helpers.functions import api_checker
from bot.modules.regex import is_sendcm_folder_link


async def androiddatahost(url):
    dom = await api_checker()
    api = f"{dom}/direct"
    resp = requests.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "androiddatahost", "url": url})
        res = resp.json()
    except BaseException:
        return "Emily API Unresponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


async def anonfiles(url):
    try:
        return Bypass().bypass_anonfiles(url)
    except BaseException:
        return "Could not Generate Direct Link for your AnonFiles Link :("


async def antfiles(url):
    try:
        return Bypass().bypass_antfiles(url)
    except BaseException:
        return "Could not Generate Direct Link for your AntFiles Link :("


async def artstation(url):
    dom = await api_checker()
    api = f"{dom}/direct"
    resp = requests.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "artstation", "url": url})
        res = resp.json()
    except BaseException:
        return "Emily API Unresponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


async def bunkr_cyber(url):
    count = 1
    dl_msg = ""
    resp = requests.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    link_type = "Bunkr" if "bunkr.is" in url else "CyberDrop"
    try:
        soup = BeautifulSoup(resp.content, "html.parser")
        if link_type == "Bunkr":
            if "stream.bunkr.is" in url:
                return url.replace("stream.bunkr.is/v", "media-files.bunkr.is")
            json_data_element = soup.find("script", {"id": "__NEXT_DATA__"})
            json_data = json.loads(json_data_element.string)
            files = json_data["props"]["pageProps"]["files"]
            for file in files:
                item_url = "https://media-files.bunkr.is/" + file["name"]
                item_url = item_url.replace(" ", "%20")
                dl_msg += f"<b>{count}.</b> <code>{item_url}</code><br>"
                count += 1
        else:
            items = soup.find_all("a", {"class": "image"})
            for item in items:
                item_url = item["href"]
                item_url = item_url.replace(" ", "%20")
                dl_msg += f"<b>{count}.</b> <code>{item_url}</code><br>"
                count += 1
        fld_msg = f"Your provided {link_type} link is of Folder and I've Found {count - 1} files in the Folder."
        fld_msg += f"I've generated Direct Links for all the files.<br><br>"
        return fld_msg + dl_msg
    except BaseException:
        return f"Could not Generate Direct Link for your {link_type} Link :("


async def dropbox(url):
    return url.replace("dropbox.com", "dl.dropboxusercontent.com")


async def dropbox2(url):
    return url.replace("?dl=0", "?dl=1")


async def fembed(url):
    try:
        dl_url = Bypass().bypass_fembed(url)
        count = len(dl_url)
        lst_link = [dl_url[i] for i in dl_url]
        dl_url = lst_link[count - 1]
        return dl_url
    except BaseException:
        return "Could not Generate Direct Link for your FEmbed Link :("


async def fichier(url):
    regex = r"^([http:\/\/|https:\/\/]+)?.*1fichier\.com\/\?.+"
    gan = re.match(regex, url)
    if not gan:
        return "The link you entered is wrong!"
    req = requests.post(url)
    if req.status_code == 404:
        return "File not found/The link you entered is wrong!"
    soup = BeautifulSoup(req.content, "lxml")
    if soup.find("a", {"class": "ok btn-general btn-orange"}) is not None:
        dl_url = soup.find("a", {"class": "ok btn-general btn-orange"})["href"]
        if dl_url is None:
            return "Unable to generate Direct Link for 1fichier!"
        else:
            return dl_url
    elif len(soup.find_all("div", {"class": "ct_warn"})) == 3:
        str_2 = soup.find_all("div", {"class": "ct_warn"})[-1]
        if "you must wait" in str(str_2).lower():
            numbers = [int(word) for word in str(str_2).split() if word.isdigit()]
            if not numbers:
                return "1fichier is on a limit. Please wait a few minutes/hour."
            else:
                return f"1fichier is on a limit. Please wait {numbers[0]} minute."
        elif "protect access" in str(str_2).lower():
            return f"This link requires a password!\n\n<b>This link requires a password!</b>"
        else:
            print(str_2)
            return "Error trying to generate Direct Link from 1fichier!"
    elif len(soup.find_all("div", {"class": "ct_warn"})) == 4:
        str_1 = soup.find_all("div", {"class": "ct_warn"})[-2]
        str_3 = soup.find_all("div", {"class": "ct_warn"})[-1]
        if "you must wait" in str(str_1).lower():
            numbers = [int(word) for word in str(str_1).split() if word.isdigit()]
            if not numbers:
                return "1fichier is on a limit. Please wait a few minutes/hour."
            else:
                return f"1fichier is on a limit. Please wait {numbers[0]} minute."
        elif "bad password" in str(str_3).lower():
            return "The password you entered is wrong!"
        else:
            return "Error trying to generate Direct Link from 1fichier!"
    else:
        return "Error trying to generate Direct Link from 1fichier!"


async def filesIm(url):
    try:
        return Bypass().bypass_filesIm(url)
    except BaseException:
        return "Could not Generate Direct Link for your FilesIm Link :("


async def github(url):
    dom = await api_checker()
    api = f"{dom}/direct"
    resp = requests.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "github", "url": url})
        res = resp.json()
    except BaseException:
        return "Emily API Unresponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


async def gdbot(url):
    dom = await api_checker()
    api = f"{dom}/direct"
    resp = requests.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "gdbot", "url": url})
        res = resp.json()
    except BaseException:
        return "Emily API Unresponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


async def gofile(url):
    dom = await api_checker()
    api = f"{dom}/direct"
    resp = requests.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "gofile", "url": url})
        res = resp.json()
    except BaseException:
        return "Emily API Unresponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


async def hxfile(url):
    try:
        return Bypass().bypass_filesIm(url)
    except BaseException:
        return "Could not Generate Direct Link for your HXFile Link :("


async def krakenfiles(url):
    dom = await api_checker()
    api = f"{dom}/direct"
    resp = requests.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "krakenfiles", "url": url})
        res = resp.json()
    except BaseException:
        return "Emily API Unresponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


async def letsupload(url):
    try:
        return Bypass().bypass_url(url)
    except BaseException:
        return "Could not Generate Direct Link for your LetsUpload Link :("


async def linkpoi(url):
    try:
        return Bypass().bypass_linkpoi(url)
    except BaseException:
        return "Could not Generate Direct Link for your Linkpoi Link :("


async def mdisk(url):
    dom = await api_checker()
    api = f"{dom}/direct"
    resp = requests.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "mdisk", "url": url})
        res = resp.json()
    except BaseException:
        return "Emily API Unresponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


async def mdisk_mpd(url):
    dom = await api_checker()
    api = f"{dom}/direct"
    resp = requests.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "mdisk_mpd", "url": url})
        res = resp.json()
    except BaseException:
        return "Emily API Unresponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


async def mediafire(url):
    dom = await api_checker()
    api = f"{dom}/direct"
    resp = requests.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "mediafire", "url": url})
        res = resp.json()
    except BaseException:
        return "Emily API Unresponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


async def megaup(url):
    dom = await api_checker()
    api = f"{dom}/direct"
    resp = requests.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "megaup", "url": url})
        res = resp.json()
    except BaseException:
        return "Emily API Unresponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


async def mirrored(url):
    try:
        return Bypass().bypass_mirrored(url)
    except BaseException:
        return "Could not Generate Direct Link for your Mirrored Link :("


async def osdn(url):
    dom = await api_checker()
    api = f"{dom}/direct"
    resp = requests.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "osdn", "url": url})
        res = resp.json()
    except BaseException:
        return "Emily API Unresponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


async def pandafile(url):
    dom = await api_checker()
    api = f"{dom}/direct"
    resp = requests.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "pandafile", "url": url})
        res = resp.json()
    except BaseException:
        return "Emily API Unresponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


async def pixeldrain(url):
    dom = await api_checker()
    api = f"{dom}/direct"
    resp = requests.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "pixeldrain", "url": url})
        res = resp.json()
    except BaseException:
        return "Emily API Unresponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


async def pixl(url):
    resp = requests.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    try:
        currentpage = 1
        settotalimgs = True
        totalimages = ""
        soup = BeautifulSoup(resp.content, "html.parser")
        if "album" in url and settotalimgs:
            totalimages = soup.find("span", {"data-text": "image-count"}).text
            settotalimgs = False
        thmbnailanchors = soup.findAll(attrs={"class": "--media"})
        links = soup.findAll(attrs={"data-pagination": "next"})
        try:
            url = links[0].attrs["href"]
        except BaseException:
            url = None
        count = 1
        ddl_msg = ""
        for ref in thmbnailanchors:
            imgdata = requests.get(ref.attrs["href"])
            if not imgdata.status_code == 200:
                sleep(3)
                continue
            imghtml = BeautifulSoup(imgdata.text, "html.parser")
            downloadanch = imghtml.find(attrs={"class": "btn-download"})
            currentimg = downloadanch.attrs["href"]
            ddl_msg += f"<b>{count}.</b> <code>{currentimg}</code><br>"
            count += 1
        currentpage += 1
        fld_msg = f"Your provided Pixl.is link is of Folder and I've Found {count - 1} files in the folder.<br>"
        fld_msg += f"I've generated Direct Links for all the files.<br><br>"
        return fld_msg + ddl_msg
    except BaseException:
        return "Could not Generate Direct Link for your Pixl.is Link :("


async def reupload(url):
    try:
        return Bypass().bypass_reupload(url)
    except BaseException:
        return "Could not Generate Direct Link for your ReUpload Link :("


async def sbembed(url):
    try:
        dl_url = Bypass().bypass_sbembed(url)
        count = len(dl_url)
        lst_link = [dl_url[i] for i in dl_url]
        dl_url = lst_link[count - 1]
        return dl_url
    except BaseException:
        return "Could not Generate Direct Link for your SBEmbed Link :("


async def sendcm(url):
    res = requests.get(url)
    if res.status_code == 404:
        return "File not found/The link you entered is wrong!"
    base_url = "https://send.cm/"
    client = cloudscraper.create_scraper(allow_brotli=False)
    hs = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    }
    is_sendcm_folder = is_sendcm_folder_link(url)
    if is_sendcm_folder:
        done = False
        msg = ""
        page_no = 0
        while not done:
            page_no += 1
            resp = client.get(url)
            soup = BeautifulSoup(resp.content, "lxml")
            table = soup.find("table", id="xfiles")
            files = table.find_all("a", class_="tx-dark")
            for file in files:
                file_url = file["href"]
                resp2 = client.get(file_url)
                scrape = BeautifulSoup(resp2.text, "html.parser")
                inputs = scrape.find_all("input")
                file_id = inputs[1]["value"]
                file_name = re.findall("URL=(.*?) - ", resp2.text)[0].split("]")[1]
                parse = {"op": "download2", "id": file_id, "referer": url}
                resp3 = client.post(
                    base_url, data=parse, headers=hs, allow_redirects=False
                )
                dl_url = resp3.headers["Location"]
                dl_url = dl_url.replace(" ", "%20")
                msg += f"File Name: {file_name}<br>File Link: {file_url}<br>Download Link: {dl_url}<br>"
                pages = soup.find("ul", class_="pagination")
                if pages is None:
                    done = True
                else:
                    current_page = pages.find(
                        "li", "page-item actived", recursive=False
                    )
                    next_page = current_page.next_sibling
                    if next_page is None:
                        done = True
                    else:
                        url = base_url + next_page["href"]
        return msg
    else:
        resp = client.get(url)
        scrape = BeautifulSoup(resp.text, "html.parser")
        inputs = scrape.find_all("input")
        file_id = inputs[1]["value"]
        file_name = re.findall("URL=(.*?) - ", resp.text)[0].split("]")[1]
        parse = {"op": "download2", "id": file_id, "referer": url}
        resp2 = client.post(base_url, data=parse, headers=hs, allow_redirects=False)
        dl_url = resp2.headers["Location"]
        dl_url = dl_url.replace(" ", "%20")
        return (
            f"File Name: {file_name}\n File Link: {url}\n Download Link: {dl_url}\n\n"
        )


async def solidfiles(url):
    dom = await api_checker()
    api = f"{dom}/direct"
    resp = requests.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "solidfiles", "url": url})
        res = resp.json()
    except BaseException:
        return "Emily API Unresponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


async def sfile(url):
    dom = await api_checker()
    api = f"{dom}/direct"
    resp = requests.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "sfile", "url": url})
        res = resp.json()
    except BaseException:
        return "Emily API Unresponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


async def sourceforge(url):
    dom = await api_checker()
    api = f"{dom}/direct"
    resp = requests.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "sourceforge", "url": url})
        res = resp.json()
    except BaseException:
        return "Emily API Unresponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


async def sourceforge2(url):
    return f"{url}" + "?viasf=1"


async def streamlare(url):
    dom = await api_checker()
    api = f"{dom}/direct"
    resp = requests.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "streamlare", "url": url})
        res = resp.json()
    except BaseException:
        return "Emily API Unresponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


async def streamtape(url):
    try:
        return Bypass().bypass_streamtape(url)
    except BaseException:
        return "Could not Generate Direct Link for your StreamTape Link :("


async def uploadee(url):
    dom = await api_checker()
    api = f"{dom}/direct"
    resp = requests.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "uploadee", "url": url})
        res = resp.json()
    except BaseException:
        return "Emily API Unresponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


async def uptobox(url):
    if UPTOBOX_TOKEN is None:
        LOGGER(__name__).info("UPTOBOX Error: Token not Provided!")
        return "UptoBox Token not Provided!"
    utb_tok = UPTOBOX_TOKEN
    try:
        link = re.findall(r"\bhttps?://.*uptobox\.com\S+", url)[0]
    except IndexError:
        return "No Uptobox links found"
    if utb_tok is None:
        LOGGER(__name__).error("UPTOBOX_TOKEN not provided!")
        dl_url = link
    else:
        try:
            link = re.findall(r"\bhttp?://.*uptobox\.com/dl\S+", url)[0]
            dl_url = link
        except BaseException:
            file_id = re.findall(r"\bhttps?://.*uptobox\.com/(\w+)", url)[0]
            file_link = (
                f"https://uptobox.com/api/link?token={utb_tok}&file_code={file_id}"
            )
            req = requests.get(file_link)
            result = req.json()
            if result["message"].lower() == "success":
                dl_url = result["data"]["dlLink"]
            elif result["message"].lower() == "waiting needed":
                waiting_time = result["data"]["waiting"] + 1
                waiting_token = result["data"]["waitingToken"]
                sleep(waiting_time)
                req2 = requests.get(f"{file_link}&waitingToken={waiting_token}")
                result2 = req2.json()
                dl_url = result2["data"]["dlLink"]
            elif (
                result["message"].lower()
                == "you need to wait before requesting a new download link"
            ):
                waiting_time = result["data"]["waiting"]
                cooldown = divmod(waiting_time, 60)
                mins = cooldown[0]
                secs = cooldown[1]
                return f"Uptobox is being limited. Please wait {mins} min {secs} sec."
            else:
                err = result["message"]
                LOGGER(__name__).info(f"UPTOBOX Error: {err}")
                return f"{err}"
    return dl_url


async def uservideo(url):
    try:
        return Bypass().bypass_uservideo(url)
    except BaseException:
        return "Could not Generate Direct Link for your UserVideo Link :("


async def wetransfer(url):
    dom = await api_checker()
    api = f"{dom}/direct"
    resp = requests.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "wetransfer", "url": url})
        res = resp.json()
    except BaseException:
        return "Emily API Unresponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


async def yandex_disk(url):
    dom = await api_checker()
    api = f"{dom}/direct"
    resp = requests.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    client = cloudscraper.create_scraper(allow_brotli=False)
    try:
        resp = client.post(api, json={"type": "yandex_disk", "url": url})
        res = resp.json()
    except BaseException:
        return "Emily API Unresponsive / Invalid Link!"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


async def zippyshare(url):
    try:
        return Bypass().bypass_zippyshare(url)
    except BaseException:
        return "Could not Generate Direct Link for your ZippyShare Link :("
