from libs.scanner import ScannerProfile

class BDSProfile(ScannerProfile):
    url = None
    fields = {
        "name": "#fix-body > div.container > div > div > div > div.group-infor-member > div > div > span.member-name-info",
        "mobile": "#fix-body > div.container > div > div > div > div.group-infor-member > div > div > h2 > a"
    }

    def __init__(self, id: int):
        self.url = f"https://bds.com.vn/thanh-vien-{id}.html"

    def check_status(self, page):
        try:
            page.query_selector("#fix-body > div.container > div > div > div > div.group-infor-member > div > div > span.member-name-info").inner_text()
        except Exception as e:
            raise  Exception("No data found")

    def before_select(self):
        pass

class BanNha888Profile(ScannerProfile):
    url = None
    fields = {
        "name": "#divSearchPage",
        "mobile": "#mm-0 > div:nth-child(2) > article > section > div.conten > div.pagewrap.page_conten_page > div.left_conten > div > div > div > div > center > div.trangcanhan-info > p:nth-child(2) > a > span"
    }

    def __init__(self, id: int):
        self.url = f"https://bannha888.com/thanh-vien/{id}"

    def check_status(self, page):
        try:
            page.query_selector("#mm-0 > div:nth-child(2) > article > section > div.conten > div.pagewrap.page_conten_page > div.left_conten > div > div > div > div > center > div.trangcanhan-info > p:nth-child(2) > a > span").inner_text()
        except Exception as e:
            raise  Exception("No data found")
        
    def before_select(self, page):
        page.click("#mm-0 > div:nth-child(2) > article > section > div.conten > div.pagewrap.page_conten_page > div.left_conten > div > div > div > div > center > div.trangcanhan-info > p:nth-child(2) > a")
        pass

def select_profile(site:str, id: int):
    if site == "bds.com.vn":
        return BDSProfile(id)
    elif site == "bannha888":
        return BanNha888Profile(id)
    return None